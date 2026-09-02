## Context

La arquitectura aprobada separa interfaz, API, servicios, repositorios y persistencia. La aplicacion usa FastAPI, SQLite, HTML, CSS, JavaScript y pytest, sin incorporar dependencias nuevas. La interfaz solo se comunica con la API; las sentencias SQL deben permanecer en la capa de acceso a datos. La motivacion y el alcance funcional se detallan en `proposal.md`; el contrato observable se define en `specs/listar-personas/spec.md`.

## Goals / Non-Goals

**Goals:**

- Implementar la lectura ordenada de personas respetando la separacion de capas.
- Mantener un contrato estable con los campos `id`, `nombre`, `apellidos` y `telefono`.
- Hacer visible el estado vacio y permitir reintentar ante un error de carga.
- Actualizar la fuente del listado despues de un alta exitosa.
- Verificar el comportamiento mediante pruebas automatizadas de API, servicio, persistencia e interfaz.

**Non-Goals:**

- No anadir paginacion, filtros, busqueda, exportacion, edicion o eliminacion.
- No introducir autenticacion, autorizacion, nuevas tecnologias ni dependencias.
- No trasladar SQL, reglas de negocio ni acceso a SQLite a la interfaz o al endpoint.

## Decisions

### Participacion de las capas

- **Interfaz:** `app/static/index.html` consumira `GET /api/personas`, renderizara las columnas acordadas, mostrara `La agenda esta vacia` para `[]` y mostrara un error con una accion de reintento cuando la carga falle. Despues de un alta exitosa solicitara de nuevo el listado o actualizara su fuente mediante la respuesta de la API, sin acceder a SQLite.
- **API:** `app/main.py` o el modulo de rutas existente expondra `GET /api/personas`, validara la solicitud, invocara el servicio y transformara el resultado en una respuesta HTTP. No contendra sentencias SQL ni coordinara directamente la base de datos.
- **Servicios:** el servicio de listado coordinara la consulta del repositorio y aplicara las reglas de caso de uso que deban ser comunes a los canales de presentacion, incluido el contrato de datos y el tratamiento controlado de errores.
- **Repositorios:** el repositorio encapsulara la operacion de lectura y solicitara los registros ya ordenados por apellidos y nombre. No expondra conexiones ni detalles de SQLite a la API o a la interfaz.
- **Persistencia:** `app/database.py` concentrara la conexion y las sentencias SQL sobre SQLite, devolviendo los datos necesarios al repositorio y propagando errores tipificados para que puedan traducirse a una respuesta controlada.

### Contrato y orden

Se usara `GET /api/personas` y una respuesta JSON de tipo array. El repositorio ordenara por apellidos y nombre ascendentes para que el mismo criterio se aplique de forma consistente y para evitar depender del orden fisico de SQLite. No se anadiran parametros de paginacion, filtros ni busqueda.

### Campos ausentes y errores

El adaptador de salida representara un telefono ausente como cadena vacia. Los errores de persistencia se registraran internamente segun las capacidades existentes, pero la API devolvera HTTP 500 y un mensaje generico sin trazas. La interfaz diferenciara el estado vacio del estado de error y permitira reintentar.

### Estrategia de pruebas

- **Persistencia/repositorio:** comprobar lectura de cero, una y varias personas, orden por apellidos y nombre, conservacion del ID y telefono ausente como cadena vacia.
- **Servicio/API:** comprobar HTTP 200 con resultados, HTTP 200 con `[]`, ausencia de paginacion, forma exacta de los campos y HTTP 500 controlado ante un fallo de persistencia.
- **Interfaz/integracion:** comprobar renderizado del listado, mensaje `La agenda esta vacia`, mensaje y reintento ante error, y actualizacion del listado despues de registrar.
- **Regresion:** ejecutar la suite completa con pytest y verificar que los escenarios de HU-01 siguen funcionando.

## Risks / Trade-offs

- [Riesgo] Un listado grande puede aumentar el tiempo de respuesta al devolver todos los registros. -> La ausencia de paginacion es una decision explicita de HU-02; se deja la optimizacion para un cambio posterior.
- [Riesgo] Los valores con distinta capitalizacion o acentos pueden producir un orden percibido diferente al esperado. -> El criterio y la comparacion se probaran con nombres representativos y cualquier cambio de ordenacion se tratara como decision funcional.
- [Riesgo] Un error de persistencia puede dejar la interfaz sin datos visibles. -> Se mostrara un estado de error diferenciado y se ofrecera reintentar, sin convertir el fallo en una agenda vacia.

## Migration Plan

No se requiere migracion de datos ni cambio de esquema. Se anadira la lectura reutilizando la persistencia existente y se verificara primero con pruebas aisladas y despues con la suite completa. El rollback consiste en retirar la ruta de listado y los controles de interfaz asociados, sin modificar los registros almacenados.

## Open Questions

No quedan preguntas funcionales abiertas para este cambio.