# P10 – Pipelines en GitHub: evidencias de CI AGENDA

- **Issue:** #9 – P10 – Automatizar la integración de AGENDA
- **Pull Request:** #10 (`feature/p10-pipeline` → `main`)
- **Workflow:** `CI AGENDA` (`.github/workflows/ci-agenda.yml`), job `Pruebas AGENDA`, `ubuntu-latest`, Python 3.11

## Qué verifica el pipeline

| Paso | Qué hace |
|---|---|
| Descargar el repositorio | `actions/checkout@v6`. En una PR, prueba la combinación temporal rama + `main`. |
| Configurar Python | `actions/setup-python@v6`, Python 3.11 con caché de pip. No usa el `.venv` local. |
| Instalar dependencias | `pip install -r requirements-dev.txt` (incluye `requirements.txt`, `pytest` y `httpx2`). |
| Ejecutar pruebas | `pytest -q --junitxml=reports/junit.xml`. Un fallo o la ausencia de pruebas hace fallar el job. |
| Conservar informe | Sube `reports/junit.xml` como artefacto `resultados-pruebas-agenda` con `if: always()` (7 días). |

Las pruebas usan TestClient y SQLite temporal por prueba (`tests/conftest.py` + fixture `isolated_database`); no dependen de `agenda.db`. La prueba del cliente independiente levanta uvicorn en un hilo y puerto libre y lo detiene al terminar.

## Ejecuciones registradas

### 1. Ejecución inicial

| Campo | Valor |
|---|---|
| Enlace | https://github.com/EduardoUNAB/AGENDA/actions/runs/37633341937 |
| Commit | `ab71d0a4adfdcf4d32b69409de28ab4ae5cb3c4e` – ci: automatizar pruebas de AGENDA |
| Evento | `pull_request` (PR #10 → `main`) |
| Duración | 16 s (job) |
| Resultado | ✅ Correcto |
| Pruebas | 29 passed, 0 failed, 0 errors |
| Informe | Artefacto `resultados-pruebas-agenda` descargado; `junit.xml` con `tests="29" failures="0"` |
| Observaciones | Ninguna. |

### 2. Fallo controlado

| Campo | Valor |
|---|---|
| Enlace | https://github.com/EduardoUNAB/AGENDA/actions/runs/37633476626 |
| Commit | `bd381238851fdf323599ad44faa8e3e9bee85cfc` – test: introducir fallo controlado para comprobar CI |
| Evento | `pull_request` (PR #10 → `main`) |
| Duración | 19 s (job) |
| Resultado | ❌ Fallido (esperado) |
| Pruebas | 1 failed, 29 passed |
| Informe | Artefacto descargado; `junit.xml` con `tests="30" failures="1"` y `<failure message="AssertionError: Fallo deliberado para comprobar CI">` |
| Observaciones | Falla el paso **Ejecutar pruebas**: `FAILED tests/test_pipeline_control.py::test_fallo_controlado_pipeline - AssertionError: Fallo deliberado para comprobar CI` (`exit code 1`). El paso **Conservar informe** se ejecuta igualmente gracias a `if: always()`. La PR muestra el check `Pruebas AGENDA` fallido. |

### 3. Corrección del fallo controlado

| Campo | Valor |
|---|---|
| Enlace | https://github.com/EduardoUNAB/AGENDA/actions/runs/37633692499 |
| Commit | `5072deab89481cc4e7c3956e12ad1a90fb825f86` – test: retirar fallo controlado de CI |
| Evento | `pull_request` (PR #10 → `main`) |
| Duración | 17 s (job) |
| Resultado | ✅ Correcto |
| Pruebas | 29 passed, 0 failed, 0 errors |
| Informe | Artefacto `resultados-pruebas-agenda` subido |
| Observaciones | Se retira `tests/test_pipeline_control.py`; el pipeline vuelve a verde. |

### 4. Push a `main`

| Campo | Valor |
|---|---|
| Enlace | https://github.com/EduardoUNAB/AGENDA/actions/runs/37636564123 |
| Commit | `dffdd675ecad168dfa87dd08b9c63897ecf318c6` – Merge pull request #10 from EduardoUNAB/feature/p10-pipeline |
| Evento | `push` a `main` |
| Duración | 16 s (job) |
| Resultado | ✅ Correcto |
| Pruebas | 29 passed, 0 failed, 0 errors |
| Informe | Artefacto `resultados-pruebas-agenda` subido |
| Observaciones | Verificación del código integrado tras fusionar las PR #8 (P8) y #10 (P10). |

## Comprobación obligatoria antes de integrar

Configurar en GitHub **Settings → Branches → Branch protection rules** (o *Rulesets*) para `main`: *Require status checks to pass before merging* con el check **Pruebas AGENDA**, y *Require a pull request before merging* con al menos una aprobación.
