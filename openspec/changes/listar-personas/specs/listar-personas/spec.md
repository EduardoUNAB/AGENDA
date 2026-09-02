## Purpose

Permite al propietario de la agenda consultar todas las personas registradas y acceder a su informacion basica de forma ordenada.

## ADDED Requirements

### Requirement: Listar personas registradas

El sistema SHALL exponer `GET /api/personas` y devolver todas las personas registradas. Cada elemento SHALL contener exactamente la informacion basica acordada: `id`, `nombre`, `apellidos` y `telefono`. Cuando una persona no tenga telefono, el valor de `telefono` SHALL ser una cadena vacia. La respuesta SHALL estar ordenada por `apellidos` y, en caso de coincidencia, por `nombre`, ambos en orden ascendente. El sistema SHALL devolver todos los resultados sin paginacion.

#### Scenario: Listado con personas registradas

- **WHEN** el propietario de la agenda solicita `GET /api/personas` y existen personas registradas
- **THEN** el sistema responde HTTP 200 con todas las personas y cada elemento contiene `id`, `nombre`, `apellidos` y `telefono`

#### Scenario: Orden por apellidos y nombre

- **WHEN** el propietario de la agenda solicita el listado con personas cuyos apellidos o nombres estan en distinto orden de registro
- **THEN** el sistema devuelve las personas ordenadas ascendentemente por apellidos y despues por nombre

#### Scenario: Persona sin telefono

- **WHEN** el listado contiene una persona sin telefono registrado
- **THEN** el sistema devuelve `telefono` como cadena vacia

#### Scenario: Agenda vacia

- **WHEN** el propietario de la agenda solicita el listado y no existen personas registradas
- **THEN** el sistema responde HTTP 200 con la lista JSON vacia `[]`

### Requirement: Mostrar el listado en la interfaz

La interfaz SHALL consumir el endpoint de listado y SHALL mostrar para cada persona su ID, nombre, apellidos y telefono. Cuando no existan personas, SHALL mostrar el mensaje `La agenda esta vacia`.Process SpawnProcess-1:
Traceback (most recent call last):
  File "C:\Users\Hp\AppData\Local\Programs\Python\Python311\Lib\multiprocessing\process.py", line 314, in _bootstrap
    self.run()
  File "C:\Users\Hp\AppData\Local\Programs\Python\Python311\Lib\multiprocessing\process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
  File "C:\Users\Hp\AGENDA\.venv\Lib\site-packages\uvicorn\_subprocess.py", line 80, in subprocess_started
    target(sockets=sockets)
  File "C:\Users\Hp\AGENDA\.venv\Lib\site-packages\uvicorn\server.py", line 77, in run
    return asyncio_run(self.serve(sockets=sockets), loop_factory=self.config.get_loop_factory())
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Hp\AGENDA\.venv\Lib\site-packages\uvicorn\_compat.py", line 30, in asyncio_run
    return runner.run(main)
           ^^^^^^^^^^^^^^^^
  File "C:\Users\Hp\AppData\Local\Programs\Python\Python311\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Hp\AppData\Local\Programs\Python\Python311\Lib\asyncio\base_events.py", line 653, in run_until_complete
    return future.result()
           ^^^^^^^^^^^^^^^
  File "C:\Users\Hp\AGENDA\.venv\Lib\site-packages\uvicorn\server.py", line 81, in serve
    await self._serve(sockets)
  File "C:\Users\Hp\AGENDA\.venv\Lib\site-packages\uvicorn\server.py", line 88, in _serve
    config.load()
  File "C:\Users\Hp\AGENDA\.venv\Lib\site-packages\uvicorn\config.py", line 494, in load
    self.loaded_app = self.load_app()
                      ^^^^^^^^^^^^^^^
  File "C:\Users\Hp\AGENDA\.venv\Lib\site-packages\uvicorn\config.py", line 428, in load_app
    return import_from_string(self.app)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Hp\AGENDA\.venv\Lib\site-packages\uvicorn\importer.py", line 22, in import_from_string
    raise exc from None
  File "C:\Users\Hp\AGENDA\.venv\Lib\site-packages\uvicorn\importer.py", line 19, in import_from_string
    module = importlib.import_module(module_str)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Hp\AppData\Local\Programs\Python\Python311\Lib\importlib\__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1206, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1178, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1128, in _find_and_load_unlockedwith_frames_removed
  File "<frozen importlib._bootstrap>", line 1206, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1178, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1142, in _find_and_load_unlocked
ModuleNotFoundError: No module named 'app'
INFO:     Stopping reloader process [13528]
(.venv) PS C:\Users\Hp\AGENDA> python -m pip install "uvicorn[standard]"
Requirement already satisfied: uvicorn[standard] in .\.venv\Lib\site-packages (0.52.4)
Requirement already satisfied: click>=7.0 in .\.venv\Lib\site-packages (from uvicorn[standard]) (8.5.0)
Requirement already satisfied: h11>=0.8 in .\.venv\Lib\site-packages (from uvicorn[standard]) (0.16.0)
Requirement already satisfied: httptools>=0.8.0 in .\.venv\Lib\site-packages (from uvicorn[standard]) (0.8.0)
Requirement already satisfied: python-dotenv>=0.13 in .\.venv\Lib\site-packages (from uvicorn[standard]) (1.2.3)
Requirement already satisfied: pyyaml>=5.1 in .\.venv\Lib\site-packages (from uvicorn[standard]) (6.0.3)om uvicorn[standard]) (1.2.0)
Requirement already satisfied: websockets>=13.0 in .\.venv\Lib\site-packages (from uvicorn[standard]) (17.1)
Requirement already satisfied: anyio>=3.0.0 in .\.venv\Lib\site-packages (from watchfiles>=0.20->uvicorn[standard]) (4.14.2)
Requirement already satisfied: idna>=2.8 in .\.venv\Lib\site-packages (from anyio>=3.0.0->watchfiles>=0.20->uvicorn[standard]) (3.19)
Requirement already satisfied: typing_extensions>=4.5 in .\.venv\Lib\site-packages (from anyio>=3.0.0->watchfiles>=0.20->uvicorn[standard]) (4.16.0)
(.venv) PS C:\Users\Hp\AGENDA> python -m uvicorn app.main:app --reload
INFO:     Will watch for changes in these directories: ['C:\\Users\\Hp\\AGENDA']INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [15908] using WatchFiles
Process SpawnProcess-1:
Traceback (most recent call last):
  File "C:\Users\Hp\AppData\Local\Programs\Python\Python311\Lib\multiprocessing\process.py", line 314, in _bootstrap
    self.run()
  File "C:\Users\Hp\AppData\Local\Programs\Python\Python311\Lib\multiprocessing\process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
  File "C:\Users\Hp\AGENDA\.venv\Lib\site-packages\uvicorn\_subprocess.py", line 80, in subprocess_started
    target(sockets=sockets)
  File "C:\Users\Hp\AGENDA\.venv\Lib\site-packages\uvicorn\server.py", line 77, in run
    return asyncio_run(self.serve(sockets=sockets), loop_factory=self.config.get_loop_factory())
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Hp\AGENDA\.venv\Lib\site-packages\uvicorn\_compat.py", line 30, in asyncio_run
    return runner.run(main)
           ^^^^^^^^^^^^^^^^
  File "C:\Users\Hp\AppData\Local\Programs\Python\Python311\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Hp\AppData\Local\Programs\Python\Python311\Lib\asyncio\base_events.py", line 653, in run_until_complete
    return future.result()
           ^^^^^^^^^^^^^^^
  File "C:\Users\Hp\AGENDA\.venv\Lib\site-packages\uvicorn\server.py", line 81, in serve
    await self._serve(sockets)
  File "C:\Users\Hp\AGENDA\.venv\Lib\site-packages\uvicorn\server.py", line 88, in _serve
    config.load()
  File "C:\Users\Hp\AGENDA\.venv\Lib\site-packages\uvicorn\config.py", line 494, in load
    self.loaded_app = self.load_app()
                      ^^^^^^^^^^^^^^^
  File "C:\Users\Hp\AGENDA\.venv\Lib\site-packages\uvicorn\config.py", line 428, in load_app
    return import_from_string(self.app)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Hp\AGENDA\.venv\Lib\site-packages\uvicorn\importer.py", line 22, in import_from_string
    raise exc from None
  File "C:\Users\Hp\AGENDA\.venv\Lib\site-packages\uvicorn\importer.py", line 19, in import_from_string
    module = importlib.import_module(module_str)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Hp\AppData\Local\Programs\Python\Python311\Lib\importlib\__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1206, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1178, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1128, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "<frozen importlib._bootstrap>", line 1206, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1178, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1142, in _find_and_load_unlocked
ModuleNotFoundError: No module named 'app'

#### Scenario: Mostrar personas en la interfaz

- **WHEN** la interfaz recibe correctamente un listado con personas
- **THEN** muestra sus cuatro campos acordados en el orden recibido

#### Scenario: Mostrar agenda vacia

- **WHEN** la interfaz recibe HTTP 200 con `[]`
- **THEN** muestra el mensaje `La agenda esta vacia`

### Requirement: Actualizar el listado despues de registrar

Tras registrar correctamente una persona, la interfaz SHALL actualizar el listado y SHALL mostrar la persona creada sin requerir una recarga manual de la pagina.

#### Scenario: Nueva persona visible tras el alta

- **WHEN** el propietario de la agenda registra correctamente una persona
- **THEN** el listado se actualiza y contiene la persona recien registrada

### Requirement: Tratar errores de persistencia de forma controlada

Si se produce un error al consultar la persistencia, el sistema SHALL responder HTTP 500 con un mensaje generico, sin exponer trazas ni detalles internos. La interfaz SHALL mostrar un mensaje de error y ofrecer una accion para reintentar la carga.

#### Scenario: Error de persistencia al listar

- **WHEN** la consulta de personas falla por un error de persistencia
- **THEN** el sistema responde HTTP 500 con un error controlado que no contiene detalles internos

#### Scenario: Reintento tras error de listado

- **WHEN** la interfaz recibe un error al cargar el listado y el propietario solicita reintentar
- **THEN** la interfaz vuelve a solicitar `GET /api/personas`