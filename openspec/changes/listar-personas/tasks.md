## 1. Contrato y acceso a datos

- [x] 1.1 Definir el esquema de respuesta del listado con `id`, `nombre`, `apellidos` y `telefono`.
- [x] 1.2 Implementar en `app/database.py` la lectura de personas desde SQLite sin paginacion y con orden por apellidos y nombre.
- [x] 1.3 Implementar o adaptar el repositorio para encapsular la consulta y convertir un telefono ausente en cadena vacia.
- [x] 1.4 Añadir pruebas de persistencia y repositorio para agenda vacia, una persona, varias personas, orden, IDs y telefono ausente.

## 2. Servicio y API

- [x] 2.1 Implementar el caso de uso de listado en la capa de servicios, sin dependencias de la interfaz.
- [x] 2.2 Exponer `GET /api/personas` desde la capa API sin sentencias SQL en el endpoint.
- [x] 2.3 Devolver HTTP 200 con el array completo y `[]` cuando no haya personas.
- [x] 2.4 Traducir los fallos de persistencia a HTTP 500 con un mensaje generico sin trazas ni detalles internos.
- [x] 2.5 Añadir pruebas de servicio y API para contrato, orden, ausencia de paginacion, respuesta vacia y error controlado.

## 3. Interfaz y actualizacion

- [x] 3.1 Mostrar en `app/static/index.html` las columnas ID, nombre, apellidos y telefono consumiendo la API.
- [x] 3.2 Mostrar `La agenda esta vacia` cuando la API responda HTTP 200 con `[]`.
- [x] 3.3 Mostrar un error de carga diferenciado de la agenda vacia y ofrecer una accion de reintento.
- [x] 3.4 Actualizar el listado automaticamente despues de un registro exitoso, sin recarga manual.
- [x] 3.5 Añadir pruebas de integracion de listado, estado vacio, error con reintento y actualizacion tras alta.

## 4. Verificacion final

- [x] 4.1 Ejecutar la suite completa con `pytest` y verificar los escenarios de HU-01 y HU-02.
- [x] 4.2 Comprobar que no se han añadido paginacion, filtros, busqueda, edicion, eliminacion, autenticacion ni dependencias nuevas.
- [x] 4.3 Revisar la conformidad con `docs/architecture.md`: capas separadas, interfaz sin SQLite, endpoints sin SQL, servicios sin dependencia de interfaz y errores sin trazas.
- [x] 4.4 Documentar el contrato de `GET /api/personas` y el resultado de las pruebas.