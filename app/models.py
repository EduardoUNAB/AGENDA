from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Persona:
    id: int | None
    nombre: str
    apellidos: str
    fecha_nacimiento: date | None
    correo: str
    telefono: str
    direccion: str
    categoria: str
    comentarios: str
