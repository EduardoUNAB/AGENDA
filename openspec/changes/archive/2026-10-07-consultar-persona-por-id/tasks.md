## 1. Persistencia y repositorio

- [x] 1.1 Añadir `find_persona_by_id` en `app/database.py`.
- [x] 1.2 Añadir `PersonaRepository.get_by_id` en `app/repositories.py` devolviendo `Persona | None`.
- [x] 1.3 Añadir pruebas del repositorio para persona existente e inexistente.

## 2. Servicio

- [x] 2.1 Añadir `PersonaNotFoundError` y `PersonaService.get_by_id` en `app/services.py`.
- [x] 2.2 Traducir `sqlite3.Error` a `PersistenceError`.
- [x] 2.3 Añadir pruebas del servicio (no encontrada y error de persistencia).

## 3. API y contrato OpenAPI

- [x] 3.1 Añadir el esquema `ErrorResponse` en `app/schemas.py`.
- [x] 3.2 Exponer `GET /api/personas/{persona_id}` en `app/main.py` con `Path(gt=0)`, `response_model`, summary, description, tags y respuestas 404/500 documentadas.
- [x] 3.3 Añadir pruebas de API: 200, 404, 422 (0, -1, `abc`, `1.5`), 500 y contrato OpenAPI.
- [x] 3.4 Exportar el contrato a `docs/openapi.json`.

## 4. Cliente independiente

- [x] 4.1 Crear `client/agenda_client.py` con `AgendaClient` y `AgendaApiError`, solo biblioteca estándar y sin importar `app`.
- [x] 4.2 Añadir pruebas del cliente contra un servidor uvicorn real (registrar, listar, obtener y 404).

## 5. Verificación final

- [x] 5.1 Actualizar la sección de API de `docs/architecture.md` y el README.
- [x] 5.2 Ejecutar la suite completa con `pytest`.
- [x] 5.3 Comprobar la conformidad con `docs/architecture.md`: endpoint sin SQL, SQL solo en `app/database.py`, capas separadas y errores sin trazas.
