# AGENDA
# Proyecto AGENDA - Equipo 04

## Miembros: 
- Vicente Díaz
- Fernando Chávez
- Fabiola Oses
- Eduardo Zepeda

## Objetivo

Aplicación de gestión de agenda personal. Mantenimiento CRUD de la entidad
`contact`. Repositorio de prácticas de la asignatura Inteligencia Artificial
aplicada a la Ingeniería de Software (UNAB, 2026-27).

## Estado
Fase inicial. Práctica P4: configuración de la fábrica de software
(repositorio, backlog, Sprint 1 y primer pipeline de CI).

## Integración continua
El workflow `.github/workflows/ci.yml` se ejecuta en cada `push` y cada
`pull request` sobre `main`, y verifica la presencia de la documentación
mínima del repositorio.

## Estructura prevista
- `/docs` — documentación funcional y técnica
- `/opsx` — contratos y especificaciones OpenSpec
- `.github/workflows` — pipelines de integración continua

## API REST (P8)
Con la aplicación en marcha (`uvicorn app.main:app --reload`):

| Método | URI | Descripción |
|---|---|---|
| POST | `/api/personas` | Registrar una persona (201) |
| GET | `/api/personas` | Listar personas (200) |
| GET | `/api/personas/{persona_id}` | Consultar una persona (200, 404, 422) |

- Swagger UI: http://127.0.0.1:8000/docs · ReDoc: http://127.0.0.1:8000/redoc
- Contrato OpenAPI exportado: `docs/openapi.json`
- Cliente Python independiente (solo biblioteca estándar):

```bash
python -m client.agenda_client listar
python -m client.agenda_client obtener 1
python -m client.agenda_client registrar Ana Perez --telefono "600 111 222"
```
