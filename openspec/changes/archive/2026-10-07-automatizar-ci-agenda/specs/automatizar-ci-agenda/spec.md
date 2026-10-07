## Purpose

Verifica automáticamente cada cambio de AGENDA en un runner de GitHub antes y después de integrarlo en `main`, y conserva el informe de pruebas como evidencia.

## ADDED Requirements

### Requirement: Ejecución en Pull Request y en main

El repositorio SHALL incluir el workflow `CI AGENDA` con el job `Pruebas AGENDA`, que se ejecuta en cada Pull Request dirigida a `main`, en cada push a `main` y bajo demanda (`workflow_dispatch`).

#### Scenario: Pull Request hacia main

- **GIVEN** una rama de trabajo con cambios
- **WHEN** se abre o actualiza una Pull Request dirigida a `main`
- **THEN** se ejecuta el job `Pruebas AGENDA` y su resultado aparece como check en la Pull Request

#### Scenario: Push a main

- **WHEN** se integra un cambio en `main`
- **THEN** el job `Pruebas AGENDA` vuelve a ejecutarse sobre el código integrado

### Requirement: Fallo real produce check fallido

El job SHALL instalar las dependencias declaradas en `requirements-dev.txt` y ejecutar `pytest`. Si alguna prueba falla o no se recopilan pruebas, el job SHALL terminar con resultado fallido sin ocultar el error.

#### Scenario: Prueba fallida

- **GIVEN** la suite contiene una prueba que falla
- **WHEN** se ejecuta el pipeline
- **THEN** el paso `Ejecutar pruebas` falla, el log identifica la prueba y la Pull Request muestra el check fallido

#### Scenario: Suite correcta

- **GIVEN** todas las pruebas pasan
- **WHEN** se ejecuta el pipeline
- **THEN** el job termina correctamente

### Requirement: Informe JUnit conservado

El job SHALL generar `reports/junit.xml` y subirlo como artefacto `resultados-pruebas-agenda` aunque las pruebas fallen. Si el informe no existe, SHALL emitirse una advertencia sin alterar el resultado del job.

#### Scenario: Informe tras fallo

- **GIVEN** una prueba falla
- **WHEN** termina el paso `Ejecutar pruebas`
- **THEN** el paso `Conservar informe` se ejecuta y el artefacto contiene el fallo

### Requirement: Datos de prueba aislados

Las pruebas SHALL usar bases de datos SQLite temporales y SHALL NOT leer ni crear la base de datos personal `agenda.db`. El resultado SHALL ser el mismo en ejecuciones repetidas, sin depender del orden ni de datos previos.

#### Scenario: Ejecución repetida

- **WHEN** se ejecuta la suite dos veces seguidas
- **THEN** ambas ejecuciones obtienen el mismo resultado y no se crea `agenda.db` en el repositorio
