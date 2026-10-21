"""Pruebas añadidas en P11. Cada caso lleva su ID de docs/p11-pruebas.md.

Las unitarias usan un repositorio en memoria y no tocan SQLite; las de API
atraviesan FastAPI, servicio, repositorio y una base de datos temporal.
"""

import sqlite3
from datetime import date

import pytest
from fastapi.testclient import TestClient

from app import database
from app.main import app
from app.schemas import PersonaCreate
from app.services import (
    DuplicateEmailError,
    PersistenceError,
    PersonaService,
    PersonaValidationError,
)


class InMemoryRepository:
    """Doble del repositorio: guarda en una lista y no abre conexiones."""

    def __init__(self):
        self.created = []

    def exists_by_normalized_email(self, email):
        return any(values["correo_normalizado"] == email for values in self.created)

    def create(self, values):
        self.created.append(values)
        return values

    def list_all(self):
        return list(self.created)


class FailingRepository(InMemoryRepository):
    def __init__(self, on, error):
        super().__init__()
        self.on = on
        self.error = error

    def exists_by_normalized_email(self, email):
        if self.on == "exists":
            raise self.error
        return super().exists_by_normalized_email(email)

    def create(self, values):
        if self.on == "create":
            raise self.error
        return super().create(values)

    def list_all(self):
        if self.on == "list":
            raise self.error
        return super().list_all()


# --- Unitarias aisladas -------------------------------------------------


def test_pa08_service_trims_fields_and_normalizes_email():
    repository = InMemoryRepository()

    PersonaService(repository).create(
        PersonaCreate(nombre="  Ana ", apellidos=" Perez  ", correo="  Ana@Example.COM ")
    )

    stored = repository.created[0]
    assert stored["nombre"] == "Ana"
    assert stored["apellidos"] == "Perez"
    assert stored["correo"] == "Ana@Example.COM"
    assert stored["correo_normalizado"] == "ana@example.com"


def test_pa09_service_accepts_birth_date_today_as_limit():
    repository = InMemoryRepository()

    PersonaService(repository).create(
        PersonaCreate(nombre="Ana", apellidos="Perez", fecha_nacimiento=date.today())
    )

    assert repository.created[0]["fecha_nacimiento"] == date.today().isoformat()


def test_pa10_service_reports_every_invalid_field_at_once():
    repository = InMemoryRepository()
    data = PersonaCreate(
        nombre=" ", apellidos="", correo="sin-arroba", telefono="abc", categoria="vecinos"
    )

    with pytest.raises(PersonaValidationError) as exc_info:
        PersonaService(repository).create(data)

    assert set(exc_info.value.errors) == {"nombre", "apellidos", "correo", "telefono", "categoria"}
    assert repository.created == []


def test_pa11_service_rejects_duplicate_email_ignoring_case():
    repository = InMemoryRepository()
    service = PersonaService(repository)
    service.create(PersonaCreate(nombre="Ana", apellidos="Perez", correo="ana@example.com"))

    with pytest.raises(DuplicateEmailError):
        service.create(PersonaCreate(nombre="Eva", apellidos="Ruiz", correo="ANA@example.com"))

    assert len(repository.created) == 1


@pytest.mark.parametrize(
    ("on", "error", "expected"),
    [
        ("exists", sqlite3.OperationalError("bloqueada"), PersistenceError),
        ("create", sqlite3.IntegrityError("UNIQUE"), DuplicateEmailError),
        ("create", sqlite3.OperationalError("disco lleno"), PersistenceError),
    ],
)
def test_pa12_service_translates_sqlite_errors_on_create(on, error, expected):
    service = PersonaService(FailingRepository(on, error))

    with pytest.raises(expected):
        service.create(PersonaCreate(nombre="Ana", apellidos="Perez", correo="ana@example.com"))


def test_pa13_service_translates_sqlite_errors_on_list():
    service = PersonaService(FailingRepository("list", sqlite3.OperationalError("boom")))

    with pytest.raises(PersistenceError):
        service.list_all()


# --- API ----------------------------------------------------------------


@pytest.fixture(name="api_client")
def client_fixture(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DATABASE_PATH", tmp_path / "test.db")
    database.initialize_database()
    return TestClient(app)


def test_pa14_register_persistence_error_returns_controlled_500(api_client, monkeypatch):
    def fail(values):
        raise sqlite3.OperationalError("disco lleno")

    monkeypatch.setattr(database, "insert_persona", fail)

    response = api_client.post("/api/personas", json={"nombre": "Ana", "apellidos": "Perez"})

    assert response.status_code == 500
    assert response.json() == {"detail": "No se pudo guardar la persona."}


def test_pa15_listing_ignores_case_and_breaks_ties_by_id(api_client):
    for nombre, apellidos in [("ana", "perez"), ("Ana", "Perez"), ("Bea", "alonso")]:
        api_client.post("/api/personas", json={"nombre": nombre, "apellidos": apellidos})

    listing = api_client.get("/api/personas").json()

    assert [(p["nombre"], p["apellidos"]) for p in listing] == [
        ("Bea", "alonso"),
        ("ana", "perez"),
        ("Ana", "Perez"),
    ]
    assert listing[1]["id"] < listing[2]["id"]


def test_pa16_null_required_fields_are_rejected_with_422(api_client):
    response = api_client.post("/api/personas", json={"nombre": None, "apellidos": None})

    assert response.status_code == 422
    assert set(response.json()["detail"]) == {"nombre", "apellidos"}
    assert api_client.get("/api/personas").json() == []


def test_pa17_index_serves_web_interface(api_client):
    response = api_client.get("/")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
