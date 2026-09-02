# Instrucciones de desarrollo para AGENDA
Antes de proponer, diseñar, implementar o revisar:
1. Lee docs/architecture.md.
2. Lee los artefactos OpenSpec del cambio.
3. Comprueba que la petición no contradice la arquitectura.
4. Si existe una contradicción, detente e informa antes de modificar
código.
## Arquitectura obligatoria
- Python 3.11+, FastAPI, SQLite y pytest.
- Separar interfaz, API, servicios, repositorios y persistencia.
- La interfaz consume la API y no accede a SQLite.
- Los endpoints no contienen consultas SQL.
- Los servicios no dependen de la interfaz.
- No añadir tecnologías sin aprobación humana.
## Terminología
- La entidad se denomina Persona.
- No utilizar Usuario para representar un contacto de la agenda.
- El actor se denomina propietario de la agenda.
## Desarrollo con OpenSpec
- No implementar sin especificación revisada.
- Seguir proposal.md, spec.md, design.md y tasks.md.
- No añadir funcionalidades fuera de alcance.
- No cambiar la especificación sin informar.
- Marcar tareas solo después de verificarlas.
## Calidad
- Generar pruebas para cada historia y ejecutar pytest.
- Utilizar códigos HTTP coherentes.
- No exponer trazas internas al usuario.