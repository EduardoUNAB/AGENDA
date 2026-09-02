from datetime import date
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class PersonaCreate(BaseModel):
    nombre: str = Field(default="")
    apellidos: str = Field(default="")
    fecha_nacimiento: date | None = None
    correo: str = ""
    telefono: str = ""
    direccion: str = ""
    categoria: str = ""
    comentarios: str = ""

    @field_validator(
        "nombre",
        "apellidos",
        "correo",
        "telefono",
        "direccion",
        "categoria",
        "comentarios",
        mode="before",
    )
    @classmethod
    def convert_empty_values(cls, value: Any) -> Any:
        return "" if value is None else value


class PersonaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    apellidos: str
    fecha_nacimiento: date | None
    correo: str
    telefono: str
    direccion: str
    categoria: str
    comentarios: str


class PersonaListResponse(BaseModel):
    id: int
    nombre: str
    apellidos: str
    telefono: str
