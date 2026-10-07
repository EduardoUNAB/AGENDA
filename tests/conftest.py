import os
import tempfile
from pathlib import Path

# app.main inicializa la base de datos al importarse; se redirige a un fichero
# temporal antes de esa importacion para no usar ni crear agenda.db.
os.environ["AGENDA_DB_PATH"] = str(Path(tempfile.mkdtemp()) / "agenda-tests.db")
