import socket
import sqlite3
import threading
import time

import pytest
import uvicorn
from fastapi.testclient import TestClient

from app import database
from app.main import app
from app.repositories import PersonaRepository
from app.services import PersistenceError, PersonaNotFoundError, PersonaService
from client.agenda_client import AgendaApiError, AgendaClient


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


# --- API ---------------------------------------------------------------


def test_get_existing_person_returns_200_with_full_data(api_client):
    created = api_client.post("/api/personas", json=valid_person()).json()

    response = api_client.get(f"/api/personas/{created['id']}")

    assert response.status_code == 200
    assert response.json() == created
    assert set(response.json()) == {
        "id", "nombre", "apellidos", "fecha_nacimiento", "correo",
        "telefono", "direccion", "categoria", "comentarios",
    }


def test_get_person_with_empty_optional_fields(api_client):
    created = api_client.post(
        "/api/personas", json={"nombre": "Luis", "apellidos": "Gomez"}
    ).json()

    body = api_client.get(f"/api/personas/{created['id']}").json()

    assert body["fecha_nacimiento"] is None
    assert body["correo"] == ""
    assert body["telefono"] == ""
    assert body["comentarios"] == ""


def test_get_nonexistent_person_returns_404(api_client):
    response = api_client.get("/api/personas/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Persona no encontrada"}


@pytest.mark.parametrize("invalid_id", ["0", "-1", "abc", "1.5"])
def test_get_person_rejects_non_positive_or_non_integer_id(api_client, monkeypatch, invalid_id):
    def must_not_be_called(_):
        raise AssertionError("La persistencia no debe consultarse")

    monkeypatch.setattr(database, "find_persona_by_id", must_not_be_called)

    response = api_client.get(f"/api/personas/{invalid_id}")

    assert response.status_code == 422


def test_get_person_persistence_error_is_controlled(api_client, monkeypatch):
    def fail(_):
        raise sqlite3.OperationalError("internal database detail")

    monkeypatch.setattr(database, "find_persona_by_id", fail)
    response = api_client.get("/api/personas/1")

    assert response.status_code == 500
    assert response.json() == {"detail": "No se pudo consultar la persona."}
    assert "internal database detail" not in response.text


def test_openapi_documents_get_person_contract(api_client):
    schema = api_client.get("/openapi.json").json()
    operation = schema["paths"]["/api/personas/{persona_id}"]["get"]

    assert operation["summary"] == "Consultar una persona"
    assert operation["description"]
    assert operation["tags"] == ["personas"]
    assert {"200", "404", "422", "500"} <= set(operation["responses"])
    assert operation["responses"]["200"]["content"]["application/json"]["schema"]["$ref"].endswith(
        "/PersonaResponse"
    )
    assert operation["responses"]["404"]["content"]["application/json"]["schema"]["$ref"].endswith(
        "/ErrorResponse"
    )
    parameter = operation["parameters"][0]
    assert parameter["name"] == "persona_id"
    assert parameter["in"] == "path"
    assert parameter["schema"]["type"] == "integer"
    assert parameter["schema"]["exclusiveMinimum"] == 0


# --- Servicio y repositorio ---------------------------------------------


def test_repository_get_by_id_returns_person_or_none(api_client):
    created = api_client.post("/api/personas", json=valid_person()).json()
    repository = PersonaRepository()

    persona = repository.get_by_id(created["id"])

    assert persona is not None
    assert persona.nombre == "Ana"
    assert repository.get_by_id(999) is None


def test_service_get_by_id_raises_not_found():
    with pytest.raises(PersonaNotFoundError):
        PersonaService().get_by_id(999)


def test_service_get_by_id_translates_persistence_errors():
    class FailingRepository(PersonaRepository):
        def get_by_id(self, persona_id):
            raise sqlite3.OperationalError("boom")

    with pytest.raises(PersistenceError):
        PersonaService(FailingRepository()).get_by_id(1)


# --- Cliente independiente ----------------------------------------------


@pytest.fixture(name="live_server_url")
def live_server_fixture():
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
    server = uvicorn.Server(uvicorn.Config(app, host="127.0.0.1", port=port, log_level="warning"))
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()
    deadline = time.time() + 10
    while not server.started:
        if time.time() > deadline:
            raise RuntimeError("El servidor de pruebas no arranco")
        time.sleep(0.05)
    yield f"http://127.0.0.1:{port}"
    server.should_exit = True
    thread.join(timeout=5)


def test_client_registers_lists_and_gets_person(live_server_url):
    client = AgendaClient(live_server_url)

    created = client.registrar_persona(valid_person())
    assert client.obtener_persona(created["id"]) == created
    assert [p["id"] for p in client.listar_personas()] == [created["id"]]


def test_client_raises_api_error_for_missing_person(live_server_url):
    client = AgendaClient(live_server_url)

    with pytest.raises(AgendaApiError) as exc_info:
        client.obtener_persona(999)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Persona no encontrada"
