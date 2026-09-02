## Why

HU-02 necesita convertir la consulta de personas registradas en un contrato verificable para que el propietario de la agenda pueda conocer los registros disponibles y su información básica.

## What Changes

- Añadir el listado de personas mediante `GET /api/personas`.
- Devolver para cada persona su `id`, `nombre`, `apellidos` y `telefono`.
- Ordenar los resultados por apellidos y, en caso de coincidencia, por nombre.
- Devolver todas las personas, sin paginación.
- Responder con HTTP 200 y `[]` cuando no haya personas.
- Mostrar `La agenda esta vacia` en la interfaz cuando el listado esté vacío.
- Actualizar el listado después de registrar una persona correctamente.
- Tratar los errores de persistencia con HTTP 500 y un mensaje genérico, sin exponer trazas internas.

## Capabilities

### New Capabilities

- `listar-personas`: Consulta y presentación de las personas registradas de la agenda.

### Modified Capabilities

Ninguna.

## Impact

- API: nuevo endpoint `GET /api/personas`.
- Servicios y repositorios: consulta ordenada de personas.
- Persistencia: lectura de personas desde SQLite mediante la capa correspondiente.
- Interfaz web: listado, estado de agenda vacía, estado de error y actualización tras un alta.
- Pruebas automatizadas de API, servicio, persistencia e interfaz.
- No afecta a `docs/architecture.md` ni añade tecnologías o dependencias.

## Fuera de alcance

- Paginación, búsqueda, filtros o exportación.
- Edición o eliminación de personas.
- Autenticación y autorización.
- Consulta de detalles adicionales fuera de los cuatro campos acordados.