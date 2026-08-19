## Purpose

Permite al propietario de la agenda registrar personas completas o con los
únicos datos mínimos requeridos, validando entradas y haciendo visible el alta.

## ADDED Requirements

### Requirement: Registrar una persona válida
El sistema SHALL permitir al propietario registrar una persona con nombre,
apellidos y los atributos opcionales de fecha de nacimiento, correo electrónico,
teléfono, dirección, categoría y comentarios.

#### Scenario: Alta con datos mínimos
- **WHEN** el propietario informa un nombre y apellidos válidos y guarda el formulario
- **THEN** el sistema crea la persona y la muestra en el listado de la agenda

#### Scenario: Alta con todos los atributos
- **WHEN** el propietario informa nombre, apellidos y valores válidos para todos los atributos opcionales
- **THEN** el sistema crea la persona conservando cada valor introducido

### Requirement: Validar campos y formatos
El sistema SHALL exigir nombre y apellidos, aceptar los demás campos vacíos y
rechazar valores no válidos con un mensaje explicativo asociado al campo.

#### Scenario: Correo inválido
- **WHEN** el propietario informa un correo con formato inválido y solicita guardar
- **THEN** el sistema rechaza el registro, no crea la persona y muestra un mensaje explicativo sobre el correo

#### Scenario: Teléfono inválido
- **WHEN** el propietario informa letras o caracteres no permitidos en el teléfono y solicita guardar
- **THEN** el sistema rechaza el registro, no crea la persona y muestra un mensaje explicativo sobre el teléfono

#### Scenario: Nombre o apellidos ausentes
- **WHEN** el propietario solicita guardar sin nombre o sin apellidos
- **THEN** el sistema rechaza el registro, no crea la persona y señala el campo obligatorio ausente

#### Scenario: Fecha futura
- **WHEN** el propietario informa una fecha de nacimiento posterior a la fecha actual
- **THEN** el sistema rechaza el registro, no crea la persona y muestra un mensaje sobre la fecha

#### Scenario: Categoría fuera del catálogo
- **WHEN** el propietario informa una categoría distinta de `familia`, `trabajo`, `amigos` u `otros`
- **THEN** el sistema rechaza el registro, no crea la persona y muestra las categorías válidas

### Requirement: Evitar duplicados por correo
El sistema SHALL rechazar el alta cuando el correo informado, comparado sin
espacios laterales y sin distinguir mayúsculas, coincide con el de una persona
existente. Un alta sin correo no SHALL considerarse duplicada por esta regla.

#### Scenario: Correo duplicado
- **WHEN** el propietario intenta registrar una persona con un correo ya existente ignorando mayúsculas o espacios laterales
- **THEN** el sistema rechaza el registro, no crea una segunda persona y explica que el correo ya está registrado

#### Scenario: Persona sin correo
- **WHEN** el propietario registra dos personas distintas sin informar correo
- **THEN** el sistema permite ambos registros si los demás datos son válidos

### Requirement: Normalizar y presentar datos
El sistema SHALL guardar la fecha de nacimiento en formato `YYYY-MM-DD` y,
tras un alta exitosa, mostrar la persona en el listado con los valores
normalizados y los datos proporcionados.

#### Scenario: Fecha con formato no permitido
- **WHEN** el propietario informa una fecha que no cumple `YYYY-MM-DD`
- **THEN** el sistema rechaza el registro y muestra el formato esperado

#### Scenario: Persona creada visible en listado
- **WHEN** el registro termina correctamente
- **THEN** el listado contiene la nueva persona sin requerir una recarga manual
