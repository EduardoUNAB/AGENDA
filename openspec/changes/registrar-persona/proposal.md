## Why

HU-01 define el alta de personas, pero deja ambiguos varios comportamientos que
afectan directamente al usuario y hacen difícil verificar la funcionalidad. Este
cambio convierte la historia en un contrato ejecutable para el primer flujo CRUD.

## What Changes

- Añadir el registro de una persona con nombre, apellidos, fecha de nacimiento,
  correo, teléfono, dirección, categoría y comentarios.
- Hacer obligatorios nombre y apellidos; mantener opcionales los demás campos.
- Validar correo, fecha de nacimiento y categoría con mensajes observables.
- Usar fecha de nacimiento en formato `YYYY-MM-DD` y rechazar fechas futuras.
- Restringir categoría a `familia`, `trabajo`, `amigos` u `otros`.
- Rechazar un registro duplicado cuando coincide el correo normalizado de una
  persona existente; si no se informa correo, no se aplica esta regla.
- Mostrar la persona creada en el listado tras guardar correctamente.

## Capabilities

### New Capabilities

- `registrar-persona`: Alta y validación de personas desde el formulario y la API.

### Modified Capabilities

Ninguna.

## Impact

- Modelo de datos `contact` y persistencia.
- Endpoint `POST /api/v1/contacts`.
- Formulario de alta y listado de agenda.
- Validaciones y pruebas del servicio de creación.
