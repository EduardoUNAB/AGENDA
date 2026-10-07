# consultar-persona-por-id Specification

## Purpose

Permite al propietario de la agenda consultar toda la información de una persona registrada a partir de su identificador.

## Requirements

### Requirement: Consultar persona existente por identificador

El sistema SHALL exponer `GET /api/personas/{persona_id}`. Cuando exista una persona con ese identificador, el sistema SHALL responder HTTP 200 con la persona representada mediante el modelo `PersonaResponse`, que contiene `id`, `nombre`, `apellidos`, `fecha_nacimiento`, `correo`, `telefono`, `direccion`, `categoria` y `comentarios`. Los campos de texto opcionales no informados SHALL devolverse como cadena vacía y `fecha_nacimiento` como `null`.

#### Scenario: Persona existente

- **GIVEN** existe una persona registrada con identificador 1
- **WHEN** el propietario de la agenda solicita `GET /api/personas/1`
- **THEN** el sistema responde HTTP 200 con todos los campos de `PersonaResponse` de esa persona

#### Scenario: Persona con campos opcionales vacíos

- **GIVEN** existe una persona registrada solo con nombre y apellidos
- **WHEN** el propietario de la agenda solicita su detalle
- **THEN** el sistema responde HTTP 200, los campos de texto opcionales son cadena vacía y `fecha_nacimiento` es `null`

### Requirement: Identificador inexistente

Cuando no exista ninguna persona con el identificador solicitado, el sistema SHALL responder HTTP 404 con la representación de error documentada `{"detail": "Persona no encontrada"}`.

#### Scenario: Persona inexistente

- **GIVEN** no existe ninguna persona con identificador 999
- **WHEN** el propietario de la agenda solicita `GET /api/personas/999`
- **THEN** el sistema responde HTTP 404 con `{"detail": "Persona no encontrada"}`

### Requirement: Identificador entero positivo

El identificador SHALL ser un entero mayor que cero. Cualquier otro valor (cero, negativo o no numérico) SHALL rechazarse con HTTP 422 sin consultar la persistencia.

#### Scenario: Identificador cero o negativo

- **WHEN** el propietario de la agenda solicita `GET /api/personas/0` o `GET /api/personas/-1`
- **THEN** el sistema responde HTTP 422

#### Scenario: Identificador no numérico

- **WHEN** el propietario de la agenda solicita `GET /api/personas/abc`
- **THEN** el sistema responde HTTP 422

### Requirement: Error de persistencia controlado

Ante un fallo de persistencia, el sistema SHALL responder HTTP 500 con el mensaje genérico `No se pudo consultar la persona.` sin exponer trazas internas.

#### Scenario: Fallo de persistencia

- **GIVEN** la persistencia falla al consultar la persona
- **WHEN** el propietario de la agenda solicita `GET /api/personas/1`
- **THEN** el sistema responde HTTP 500 con `{"detail": "No se pudo consultar la persona."}` y sin trazas

### Requirement: Contrato documentado en OpenAPI

El documento OpenAPI SHALL describir el endpoint con summary, description, tag `personas`, el parámetro `persona_id` con su restricción de entero positivo y las respuestas 200 (`PersonaResponse`), 404 y 500 (`ErrorResponse`) y 422.

#### Scenario: Contrato publicado

- **WHEN** se consulta `/openapi.json`
- **THEN** la operación `GET /api/personas/{persona_id}` aparece con las respuestas 200, 404, 422 y 500 documentadas y `persona_id` con `exclusiveMinimum: 0`

### Requirement: Cliente Python independiente

El repositorio SHALL incluir un cliente Python independiente del paquete `app` que consuma la API únicamente a través de HTTP, permita listar, registrar y consultar personas por identificador, y traduzca las respuestas de error en excepciones con el código HTTP y el `detail` recibido.

#### Scenario: Consulta desde el cliente

- **GIVEN** la API está en ejecución y existe la persona con identificador 1
- **WHEN** el cliente invoca la consulta de la persona 1
- **THEN** obtiene un diccionario con los campos de `PersonaResponse`

#### Scenario: Persona inexistente desde el cliente

- **WHEN** el cliente consulta un identificador inexistente
- **THEN** se lanza un error con código 404 y detalle `Persona no encontrada`
