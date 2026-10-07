## 1. Dependencias y aislamiento

- [x] 1.1 Crear `requirements-dev.txt` con `-r requirements.txt`, `pytest` y `httpx2` fijados.
- [x] 1.2 Verificar en local `pip install -r requirements-dev.txt` y `python -m pytest -q`.
- [x] 1.3 Crear `tests/conftest.py` para que las pruebas no usen ni creen `agenda.db`.
- [x] 1.4 Ignorar `reports/` en `.gitignore`.

## 2. Workflow

- [x] 2.1 Crear `.github/workflows/ci-agenda.yml` (CI AGENDA / Pruebas AGENDA) con informe JUnit y artefacto.
- [x] 2.2 Eliminar el workflow previo `.github/workflows/ci.yml`.

## 3. Ejecución y evidencias

- [x] 3.1 Publicar la rama y abrir la Pull Request hacia `main` enlazando la Issue #9.
- [x] 3.2 Revisar la ejecución en Actions y descargar el artefacto.
- [x] 3.3 Introducir el fallo controlado `tests/test_pipeline_control.py`, comprobar el check fallido y el informe.
- [x] 3.4 Retirar el fallo controlado y comprobar que el pipeline vuelve a verde.
- [x] 3.5 Registrar las evidencias en `docs/p10-pipelines.md` y actualizar el README.

## 4. Verificación final

- [x] 4.1 Ejecutar la suite completa con `pytest`.
- [x] 4.2 Comprobar la conformidad con `docs/architecture.md`: sin cambios en la aplicación ni en el contrato de la API, sin tecnologías nuevas.
