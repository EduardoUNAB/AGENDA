# Arquitectura de la aplicación AGENDA
## 1. Objetivo
AGENDA es una aplicación web para registrar y consultar personas. Esta
arquitectura establece restricciones obligatorias para todos los
cambios.
## 2. Tecnologías aprobadas
- Python 3.11 o superior.
- FastAPI para la API REST.
- SQLite como persistencia.
- HTML, CSS y JavaScript para la interfaz.
- pytest para pruebas.
- OpenAPI/Swagger para documentación de la API.
- GitHub Actions para integración continua.
No se añadirán tecnologías sin una decisión explícita y documentada.

## 3. Estilo arquitectónico
Arquitectura en capas: interfaz, API, servicios, repositorioS y
persistencia.
## 4. Responsabilidades de cada capa
- Capa Interfaz: captura acciones, muestra información y consume la
API. No accede a SQLite ni contiene reglas de negocio.
- API: expone endpoints, recibe y valida peticiones, invoca Servicios
y construye respuestas HTTP. No contiene SQL.
- Capa Servicios: implementa casos de uso y coordina repositorios. No
depende de la interfaz.
- Capa Repositorios: encapsula las consultas y el acceso a datos .
- Capa Persistencia: utiliza SQLite y mantiene los datos tras
reiniciar la aplicación.
## 5. Modelo inicial Persona
id, nombre, apellidos, fecha de nacimiento, correo electrónico,
teléfono, dirección, categoría y comentarios. El ID lo genera el
sistema. Las validaciones exactas se definen en HU-01.
## 6. API inicial
- POST /api/personas: registrar una persona.
- GET /api/personas: listar las personas.
## 7. Organización orientativa
app/main.py, app/api/, app/models/, app/schemas/, app/services/,
app/repositories/, app/static/, app/templates/ y tests/.
## 8. Reglas
- No concentrar toda la aplicación en un fichero.
- No acceder a SQLite desde la interfaz o los endpoints.
- No colocar reglas de negocio en JavaScript.
- Cada historia debe incluir pruebas.
- Todo cambio debe corresponder a una especificación OpenSpec.
- Los cambios arquitectónicos requieren revisión humana.
## 9. Errores
No exponer trazas internas. Utilizar códigos HTTP coherentes y tratar
los errores de persistencia de forma controlada.
## 10. Fuera de alcance
Autenticación, autorización, microservicios, contenedores, base de
datos distribuida, paginación, búsqueda avanzada, modificación y
eliminación de personas..