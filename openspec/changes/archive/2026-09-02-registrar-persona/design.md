## Context

El repositorio contiene la historia HU-01, el modelo conceptual `persona` y el
contrato inicial del endpoint `POST /api/personas`, pero todavía no tiene una
implementación de aplicación. La propuesta fija las decisiones funcionales que
no estaban explícitas en la historia.

## Goals / Non-Goals

**Goals:**

- Mantener una única regla de validación compartida entre API y formulario.
- Persistir personas válidas y devolver errores de campo consistentes.
- Hacer que el listado refleje el alta exitosa inmediatamente.
- Cubrir los escenarios de la especificación con pruebas automatizadas.

**Non-Goals:**

- Modificar las operaciones de consulta, edición o eliminación.
- Incorporar autenticación o autorización nueva.
- Definir límites de longitud no acordados para teléfono, dirección o comentarios.

## Decisions

- **Contrato HTTP:** implementar `POST /api/personas` para recibir el objeto
  de persona y devolver la entidad creada con respuesta exitosa; los errores de
  validación usarán una respuesta estructurada por campo. Se mantiene el
  endpoint indicado por HU-01 en lugar de introducir una versión alternativa.
- **Validación centralizada:** ubicar las reglas de campos obligatorios, correo,
  fecha, catálogo y duplicados en una capa de dominio/servicio reutilizable por
  API y presentación. Así se evita que ambos canales acepten datos distintos.
- **Fecha:** transportar y persistir `YYYY-MM-DD` como fecha civil, sin convertir
  a zona horaria. Se descarta guardar un timestamp porque puede cambiar el día
  observado por el usuario.
- **Duplicados:** normalizar correo con recorte de espacios y comparación sin
  distinguir mayúsculas antes de consultar persistencia. No se inventa una clave
  para personas sin correo.
- **Categoría:** representar el catálogo como valores enumerados en la validación
  y ofrecer esos cuatro valores en el formulario. El texto libre se descarta
  porque haría imposible garantizar búsquedas y consistencia.
- **Listado:** invalidar o refrescar la fuente de datos del listado después de un
  alta exitosa, conservando el resultado normalizado devuelto por el servicio.

## Risks / Trade-offs

- [Riesgo] Datos existentes pueden contener correos con espacios o mayúsculas.
  -> La comparación normalizada evita nuevos duplicados, pero requiere revisar
  esos datos durante la primera carga o migración.
- [Riesgo] No existe todavía una base tecnológica de aplicación en el repositorio.
  -> Las tareas separan contrato, dominio, persistencia y presentación para
  permitir implementar cada capa cuando se defina el stack.
- [Riesgo] La fecha actual depende del reloj del servidor.
  -> El servicio debe obtener la fecha actual de forma inyectable en pruebas.

## Migration Plan

Crear el modelo y la validación, añadir el endpoint y conectar el formulario al
listado. Probar primero contra almacenamiento de prueba; desplegar después la
persistencia definitiva. El rollback consiste en retirar la ruta y la pantalla
de alta sin modificar los datos ya existentes.
