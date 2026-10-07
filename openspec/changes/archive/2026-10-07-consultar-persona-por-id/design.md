## Context

La arquitectura aprobada (`docs/architecture.md`) separa interfaz, API, servicios, repositorios y persistencia. Las sentencias SQL permanecen en `app/database.py`. HU-03 añade una operación de lectura sobre el recurso Persona ya existente. El contrato observable se define en `specs/consultar-persona-por-id/spec.md`.

## Goals / Non-Goals

**Goals:**

- Exponer `GET /api/personas/{persona_id}` respetando la semántica REST (recurso identificable por URI, método GET, 200/404/422/500).
- Reutilizar `PersonaResponse` como representación de la persona.
- Documentar el contrato en OpenAPI y exportarlo a `docs/openapi.json`.
- Ofrecer un cliente Python independiente que consuma el contrato.

**Non-Goals:**

- No modificar la interfaz web.
- No añadir modificación, eliminación, búsqueda ni paginación.
- No introducir tecnologías ni dependencias nuevas.

## Decisions

### Participación de las capas

- **Interfaz:** sin cambios. El endpoint queda disponible para Swagger UI y otros consumidores.
- **API (`app/main.py`):** nuevo endpoint con `Path(gt=0)` para validar el identificador, `response_model=PersonaResponse`, `summary`, `description`, `tags=["personas"]` y `responses` para 404 y 500. Traduce `PersonaNotFoundError` a 404 y `PersistenceError` a 500. No contiene SQL. Se añaden también summary y tag a los endpoints existentes para un contrato homogéneo.
- **Servicios (`app/services.py`):** `PersonaService.get_by_id(persona_id)` devuelve la `Persona` o lanza `PersonaNotFoundError`; traduce `sqlite3.Error` a `PersistenceError`.
- **Repositorios (`app/repositories.py`):** `PersonaRepository.get_by_id(persona_id)` devuelve `Persona | None` reutilizando `_to_persona`.
- **Persistencia (`app/database.py`):** `find_persona_by_id(persona_id)` ejecuta `SELECT * FROM personas WHERE id = ?`.
- **Esquemas (`app/schemas.py`):** nuevo `ErrorResponse` con el campo `detail: str` para documentar los errores 404 y 500.

### Representación del error

Se mantiene el formato estándar de FastAPI `{"detail": "..."}` para no introducir un formato distinto al de los endpoints existentes. Se documenta mediante el esquema `ErrorResponse`.

### Validación del identificador

La restricción de entero positivo se declara en la capa API con `Path(gt=0)`. FastAPI responde 422 sin invocar al servicio y la restricción queda reflejada en OpenAPI (`exclusiveMinimum: 0`).

### Cliente independiente

`client/agenda_client.py` usa `urllib.request` y `json` de la biblioteca estándar, por lo que no añade dependencias. No importa nada de `app`: solo conoce el contrato HTTP. Expone `AgendaClient` con `listar_personas`, `registrar_persona` y `obtener_persona`, y `AgendaApiError(status_code, detail)` para errores. Incluye una pequeña CLI (`python -m client.agenda_client obtener 1`).

### Estrategia de pruebas

- **API:** 200 con persona completa, 200 con campos opcionales vacíos, 404 inexistente, 422 para 0, -1 y `abc`, 500 controlado ante fallo de persistencia, contrato OpenAPI documentado.
- **Servicio:** devuelve la persona, lanza `PersonaNotFoundError` y traduce `sqlite3.Error`.
- **Repositorio:** devuelve `Persona` o `None`.
- **Cliente:** prueba contra un servidor uvicorn real en un hilo y puerto libre (registrar, obtener, 404).
- **Regresión:** ejecución completa de `pytest`.

## Risks / Trade-offs

- [Riesgo] Exponer el ID secuencial permite enumerar personas. -> Aceptado: la autenticación está fuera de alcance según la arquitectura.
