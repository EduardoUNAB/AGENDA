## 1. Modelo y persistencia

- [ ] 1.1 Definir el modelo `contact` con los ocho atributos de HU-01 y sus campos opcionales.
- [ ] 1.2 Implementar persistencia de contactos y consulta por correo normalizado.
- [ ] 1.3 Añadir la normalización de correo y fecha sin alterar los valores visibles válidos.

## 2. Validación y API

- [ ] 2.1 Implementar validaciones de nombre y apellidos obligatorios, correo, fecha y categoría.
- [ ] 2.2 Implementar la regla de duplicados por correo y permitir múltiples contactos sin correo.
- [ ] 2.3 Implementar `POST /api/v1/contacts` con respuesta de creación y errores estructurados por campo.
- [ ] 2.4 Cubrir con pruebas unitarias los escenarios de alta válida, campos ausentes, correo inválido, fecha futura, fecha mal formada, categoría inválida y duplicado.

## 3. Presentación y listado

- [ ] 3.1 Construir el formulario con los ocho atributos y categoría como lista cerrada.
- [ ] 3.2 Mostrar mensajes de validación asociados al campo sin borrar los valores introducidos.
- [ ] 3.3 Actualizar el listado inmediatamente después de una creación exitosa.
- [ ] 3.4 Añadir pruebas de integración del formulario, alta y aparición en el listado.

## 4. Verificación

- [ ] 4.1 Ejecutar la suite completa y verificar todos los escenarios de `spec.md`.
- [ ] 4.2 Documentar el contrato de `POST /api/v1/contacts` y los valores permitidos de categoría.
