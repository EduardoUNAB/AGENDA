## Why

HU-03 necesita que el propietario de la agenda pueda consultar toda la información de una persona concreta a partir de su identificador. Hasta ahora la API solo permite registrar (`POST /api/personas`) y listar (`GET /api/personas`) con información básica, por lo que no existe forma de acceder al detalle completo de una persona.

## What Changes

- Añadir `GET /api/personas/{persona_id}` para consultar una persona por su identificador.
- Responder HTTP 200 con la persona completa usando el modelo `PersonaResponse`.
- Responder HTTP 404 con la representación de error documentada `{"detail": "Persona no encontrada"}` cuando el identificador no exista.
- Validar que `persona_id` es un entero positivo (`> 0`); en otro caso responder HTTP 422.
- Tratar los errores de persistencia con HTTP 500 y un mensaje genérico, sin exponer trazas internas.
- Documentar el endpoint en OpenAPI (summary, description, tags, parámetros y respuestas 200, 404, 422 y 500) y exportar el contrato a `docs/openapi.json`.
- Añadir un cliente Python independiente (`client/agenda_client.py`) que consuma la API usando solo la biblioteca estándar.

## Capabilities

### New Capabilities

- `consultar-persona-por-id`: Consulta del detalle completo de una persona mediante su identificador.

### Modified Capabilities

Ninguna.

## Impact

- API: nuevo endpoint `GET /api/personas/{persona_id}` y esquema `ErrorResponse` documentado.
- Servicios: nuevo caso de uso de consulta por identificador.
- Repositorios y persistencia: lectura de una persona por `id` en `app/database.py`.
- Documentación: `docs/architecture.md` (API) y `docs/openapi.json`.
- Cliente independiente: `client/agenda_client.py`, fuera del paquete `app`, sin dependencias nuevas.
- Pruebas automatizadas de API, servicio, repositorio y cliente.
- No añade tecnologías ni dependencias.

## Fuera de alcance

- Modificación o eliminación de personas.
- Cambios en la interfaz web.
- Búsqueda por otros campos, filtros o paginación.
- Autenticación y autorización.
