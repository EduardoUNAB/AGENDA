from datetime import date, timedelta

import pytest
from fastapi.testclient import TestClient

from app import database
from app.main import app


@pytest.fixture(autouse=True)
def isolated_database(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DATABASE_PATH", tmp_path / "test.db")
    database.initialize_database()


@pytest.fixture(name="api_client")
def client_fixture():
    return TestClient(app)


def valid_person(**overrides):
    person = {
        "nombre": "Ana",
        "apellidos": "Perez",
        "fecha_nacimiento": "1990-01-02",
        "correo": "ana@example.com",
        "telefono": "+34 600 111 222",
        "direccion": "Calle 1",
        "categoria": "familia",
        "comentarios": "Nota",
    }
    person.update(overrides)
    return person


def test_register_valid_person_returns_created(api_client):
    response = api_client.post("/api/personas", json=valid_person())
    assert response.status_code == 201
    assert response.json()["nombre"] == "Ana"
    assert response.json()["fecha_nacimiento"] == "1990-01-02"


def test_rejects_missing_required_fields(api_client):
    response = api_client.post("/api/personas", json={})
    assert response.status_code == 422
    assert "nombre" in response.json()["detail"]
    assert "apellidos" in response.json()["detail"]


def test_rejects_invalid_email(api_client):
    response = api_client.post("/api/personas", json=valid_person(correo="invalido"))
    assert response.status_code == 422
    assert "correo" in response.json()["detail"]


def test_rejects_future_birth_date(api_client):
    future = (date.today() + timedelta(days=1)).isoformat()
    response = api_client.post("/api/personas", json=valid_person(fecha_nacimiento=future))
    assert response.status_code == 422
    assert "fecha_nacimiento" in response.json()["detail"]


def test_rejects_malformed_birth_date(api_client):
    response = api_client.post("/api/personas", json=valid_person(fecha_nacimiento="02-01-1990"))
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"][-1] == "fecha_nacimiento"


def test_rejects_invalid_category(api_client):
    response = api_client.post("/api/personas", json=valid_person(categoria="colegio"))
    assert response.status_code == 422
    assert "categoria" in response.json()["detail"]


def test_rejects_duplicate_normalized_email(api_client):
    assert api_client.post("/api/personas", json=valid_person()).status_code == 201
    response = api_client.post(
        "/api/personas", json=valid_person(correo=" ANA@EXAMPLE.COM ")
    )
    assert response.status_code == 409
    assert "correo" in response.json()["detail"]


def test_allows_multiple_people_without_email(api_client):
    assert api_client.post("/api/personas", json=valid_person(correo="")).status_code == 201
    assert api_client.post("/api/personas", json=valid_person(correo="", nombre="Luis")).status_code == 201


def test_rejects_invalid_phone(api_client):
    response = api_client.post("/api/personas", json=valid_person(telefono="abc"))
    assert response.status_code == 422
    assert "telefono" in response.json()["detail"]


def test_lists_several_people_with_agreed_fields_and_order(api_client):
    api_client.post("/api/personas", json=valid_person(nombre="Zoe", apellidos="Bravo"))
    api_client.post("/api/personas", json=valid_person(nombre="Ana", apellidos="Bravo", correo="ana2@example.com"))
    api_client.post("/api/personas", json=valid_person(nombre="Luis", apellidos="Alvarez", correo="luis@example.com"))

    response = api_client.get("/api/personas")

    assert response.status_code == 200
    assert response.json() == [
        {"id": 3, "nombre": "Luis", "apellidos": "Alvarez", "telefono": "+34 600 111 222"},
        {"id": 2, "nombre": "Ana", "apellidos": "Bravo", "telefono": "+34 600 111 222"},
        {"id": 1, "nombre": "Zoe", "apellidos": "Bravo", "telefono": "+34 600 111 222"},
    ]


def test_empty_agenda_returns_200_and_empty_list(api_client):
    response = api_client.get("/api/personas")
    assert response.status_code == 200
    assert response.json() == []


def test_listing_uses_empty_string_for_missing_phone(api_client):
    api_client.post("/api/personas", json=valid_person(telefono=""))
    response = api_client.get("/api/personas")
    assert response.json()[0]["telefono"] == ""


def test_new_person_appears_in_listing(api_client):
    api_client.post("/api/personas", json=valid_person())
    response = api_client.get("/api/personas")
    assert response.json()[0]["nombre"] == "Ana"


def test_static_interface_contains_empty_state_and_retry_behavior():
    content = open("app/static/index.html", encoding="utf-8").read()
    assert "La agenda esta vacia" in content
    assert "Reintentar" in content
    assert "loadPersonas" in content


def test_listing_persistence_error_is_controlled(api_client, monkeypatch):
    def fail_listing():
        raise database.sqlite3.OperationalError("internal database detail")

    monkeypatch.setattr(database, "list_personas", fail_listing)
    response = api_client.get("/api/personas")

    assert response.status_code == 500
    assert response.json()["detail"] == "No se pudo consultar la agenda."
    assert "internal database detail" not in response.text
