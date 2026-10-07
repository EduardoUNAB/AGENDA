## Why

Una ejecución local correcta no garantiza que AGENDA funcione en otra máquina. El equipo necesita verificar automáticamente cada Pull Request en un entorno independiente del desarrollador (runner de GitHub) antes de integrar cambios en `main`, y conservar evidencias de cada ejecución (P10, Issue #9).

## What Changes

- Sustituir `.github/workflows/ci.yml` por `.github/workflows/ci-agenda.yml` (workflow **CI AGENDA**, job **Pruebas AGENDA**).
- Ejecutar el workflow en `pull_request` y `push` hacia `main` y manualmente con `workflow_dispatch`.
- Ejecutar `pytest` y generar un informe JUnit en `reports/junit.xml`, que se sube como artefacto `resultados-pruebas-agenda` incluso cuando fallan las pruebas.
- Añadir `requirements-dev.txt` con las dependencias de pruebas declaradas y fijadas.
- Garantizar que las pruebas no usan ni crean la base de datos personal `agenda.db` (`tests/conftest.py`).
- Documentar el pipeline y las evidencias de ejecución en `docs/p10-pipelines.md`.

## Capabilities

### New Capabilities

- `automatizar-ci-agenda`: Verificación automática de AGENDA en GitHub Actions.

### Modified Capabilities

Ninguna.

## Impact

- `.github/workflows/`: se elimina `ci.yml` y se crea `ci-agenda.yml`.
- `requirements-dev.txt`, `tests/conftest.py`, `.gitignore` (`reports/`).
- Documentación: `docs/p10-pipelines.md`, README.
- No añade endpoints ni altera el contrato de la API.

## Fuera de alcance

- Entrega o despliegue continuos.
- Matrices de versiones de Python o sistemas operativos.
- Análisis estático, cobertura obligatoria u otros jobs.
