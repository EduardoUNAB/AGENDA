## Context

`docs/architecture.md` aprueba GitHub Actions para integración continua y pytest para pruebas. Existía un workflow previo `.github/workflows/ci.yml` (también llamado "CI AGENDA") que instalaba `requirements.txt` y ejecutaba pytest sin conservar informes. El contrato observable se define en `specs/automatizar-ci-agenda/spec.md`.

## Goals / Non-Goals

**Goals:**

- Un único workflow versionado, `ci-agenda.yml`, con un único job para facilitar el diagnóstico.
- Dependencias de pruebas declaradas explícitamente y fijadas.
- Informe JUnit conservado incluso ante fallos.
- Pruebas aisladas de la base de datos personal.

**Non-Goals:**

- No modificar la aplicación ni el contrato de la API.
- No añadir entrega/despliegue continuos ni nuevas tecnologías.

## Decisions

### Sustitución de `ci.yml`

Se elimina `ci.yml` y se crea `ci-agenda.yml`. Mantener ambos produciría dos workflows con el mismo nombre ejecutando las mismas pruebas, lo que duplica checks y confunde la revisión.

### Workflow `ci-agenda.yml`

- Eventos: `pull_request` y `push` filtrados a `main`, más `workflow_dispatch`.
- `permissions: contents: read` (mínimo privilegio).
- Job `pruebas` (`Pruebas AGENDA`) en `ubuntu-latest`, `timeout-minutes: 10`.
- Steps: `actions/checkout@v6`, `actions/setup-python@v6` con Python `3.11` (versión mínima de `docs/architecture.md`) y caché de pip, instalación de `requirements-dev.txt`, `pytest -q --junitxml=reports/junit.xml`, y `actions/upload-artifact@v4` con `if: ${{ always() }}`, `if-no-files-found: warn` y `retention-days: 7`.

### `requirements-dev.txt`

Incluye `-r requirements.txt` y declara las herramientas de prueba con versión fijada: `pytest` y `httpx2`. En la versión de Starlette usada, `TestClient` importa `httpx2` (con `httpx` solo como alternativa), por lo que se declara `httpx2` en lugar de `httpx`.

### Aislamiento de datos

`app/main.py` llama a `database.initialize_database()` al importarse, antes de que actúe el fixture que redirige `DATABASE_PATH`, lo que creaba `agenda.db` en la raíz. `tests/conftest.py` fija `AGENDA_DB_PATH` a un fichero temporal antes de importar la aplicación. El fixture `autouse` existente sigue creando una base de datos nueva por prueba, lo que garantiza independencia de orden y de datos previos. La prueba del cliente independiente arranca uvicorn en un hilo y puerto libre y lo detiene al terminar, por lo que es válida en el runner.

### Evidencias

`docs/p10-pipelines.md` registra, por ejecución: enlace, SHA, evento, duración, resultado, número de pruebas, disponibilidad del artefacto y observaciones, incluido el fallo controlado.

## Risks / Trade-offs

- [Riesgo] Las actions referenciadas por versión mayor pueden cambiar. -> Aceptado para la práctica; se puede fijar a SHA en el futuro.
- [Riesgo] La rama P7 pendiente modifica `ci.yml`. -> Al integrarla se resolverá el conflicto conservando `ci-agenda.yml`.
