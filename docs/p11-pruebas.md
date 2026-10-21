# P11 – Pruebas automáticas de AGENDA

- **Issue:** #12 – P11 – Ampliar las pruebas automáticas de AGENDA
- **Rama:** `feature/p11-pruebas-automaticas`
- **Workflow:** `CI AGENDA` (`.github/workflows/ci-agenda.yml`), ahora con cobertura y artefacto `informes-pruebas` (`junit.xml` + `coverage.xml`)

## Casos de la práctica (PA-01 … PA-07)

Ya existían desde P6 y P8, derivados de los escenarios OpenSpec. Se reutilizan sin cambios.

| ID | Caso | Resultado esperado | Tipo | Requisito | Prueba |
|---|---|---|---|---|---|
| PA-01 | Registrar persona válida | 201 | API | HU-01 `registrar-persona` | `test_agenda.py::test_register_valid_person_returns_created` |
| PA-02 | Correo inválido | 422 | API | HU-01 | `test_agenda.py::test_rejects_invalid_email` |
| PA-03 | Listar agenda vacía | 200 y `[]` | API | HU-02 `listar-personas` | `test_agenda.py::test_empty_agenda_returns_200_and_empty_list` |
| PA-04 | Listar varias personas | Orden por apellidos y nombre | API | HU-02 | `test_agenda.py::test_lists_several_people_with_agreed_fields_and_order` |
| PA-05 | Consultar ID existente | 200 y datos correctos | API | HU-03 `consultar-persona-por-id` | `test_consultar_persona.py::test_get_existing_person_returns_200_with_full_data` |
| PA-06 | Consultar ID inexistente | 404 | API | HU-03 | `test_consultar_persona.py::test_get_nonexistent_person_returns_404` |
| PA-07 | Consultar ID no positivo | 422 | API | HU-03 | `test_consultar_persona.py::test_get_person_rejects_non_positive_or_non_integer_id` |

## Casos nuevos (`tests/test_p11_pruebas.py`)

Las **unitarias** sustituyen el repositorio por un doble en memoria (`InMemoryRepository`, `FailingRepository`): no abren SQLite ni pasan por HTTP. Las de **API** usan `TestClient`, recorren todas las capas y usan una base de datos temporal por prueba (`tmp_path` + `monkeypatch`).

| ID | Caso | Tipo | Clase | Requisito | Dependencia aislada |
|---|---|---|---|---|---|
| PA-08 | Recorta espacios y normaliza el correo a minúsculas | Unitaria | Positivo | HU-01 | Repositorio (doble en memoria) |
| PA-09 | Fecha de nacimiento igual a hoy se acepta | Unitaria | Límite | HU-01 | Repositorio |
| PA-10 | Se informan todos los campos inválidos a la vez y no se guarda nada | Unitaria | Negativo | HU-01 | Repositorio |
| PA-11 | El correo duplicado se detecta sin distinguir mayúsculas | Unitaria | Negativo | HU-01 | Repositorio |
| PA-12 | Los errores de SQLite se traducen: comprobación → 500, `IntegrityError` en una carrera → duplicado, fallo al insertar → 500 (3 variantes) | Unitaria | Negativo | HU-01 | Repositorio que falla a propósito |
| PA-13 | Un error de SQLite al listar se traduce a `PersistenceError` | Unitaria | Negativo | HU-02 | Repositorio que falla a propósito |
| PA-14 | Un error de persistencia al registrar devuelve un 500 controlado | API | Negativo | HU-01 | `database.insert_persona` sustituido |
| PA-15 | El listado no distingue mayúsculas y, a igualdad, ordena por `id` | API | Límite | HU-02 | SQLite temporal |
| PA-16 | `nombre`/`apellidos` a `null` → 422 y la agenda sigue vacía | API | Negativo | HU-01 | SQLite temporal |
| PA-17 | `/` sirve la interfaz web | API | Positivo | Interfaz P6 | SQLite temporal |

Son 10 casos (12 ejecuciones), seis de ellos unitarios aislados. Los casos se propusieron con ayuda de IA y se descartaron los que solo repetían PA-01…PA-07. El equipo los revisa en la Pull Request.

## Cobertura

```bash
python -m pip install -r requirements-dev.txt   # añade pytest-cov
python -m pytest --cov=app --cov-report=term-missing
python -m pytest --cov=app --cov-fail-under=80
```

| Momento | Pruebas | Cobertura | Líneas sin cubrir |
|---|---|---|---|
| Antes de P11 | 29 passed | 95 % | `main.py` 27-29, 54-56 · `services.py` 43, 46-49 |
| Después de P11 | 41 passed | 100 % | — |

Las dos zonas sin cubrir que se encontraron, y los casos que las cubren:

1. **Traducción de errores de SQLite al registrar** (`services.py` 43, 46-49; `main.py` 54-56). Se cubre con PA-12 y PA-14. Incluye la carrera en la que dos altas pasan la comprobación previa y la unicidad la impone el índice.
2. **Ruta `/` de la interfaz** (`main.py` 27-29). Se cubre con PA-17.

El 100 % de líneas **no** demuestra que se cumplan todos los requisitos: mide qué líneas se ejecutaron, no si las aserciones son correctas.

## Ejecuciones en GitHub Actions

Se rellena con las ejecuciones de la PR.
