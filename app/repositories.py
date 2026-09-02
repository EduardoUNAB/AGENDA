import sqlite3

from . import database
from .models import Persona


class PersonaRepository:
    def exists_by_normalized_email(self, email: str) -> bool:
        return database.find_by_normalized_email(email) is not None

    def create(self, values: dict[str, str | None]) -> Persona:
        row = database.insert_persona(values)
        return self._to_persona(row)

    def list_all(self) -> list[Persona]:
        return [self._to_persona(row) for row in database.list_personas()]

    @staticmethod
    def _to_persona(row: sqlite3.Row) -> Persona:
        from datetime import date

        birth_date = date.fromisoformat(row["fecha_nacimiento"]) if row["fecha_nacimiento"] else None
        return Persona(
            id=row["id"],
            nombre=row["nombre"],
            apellidos=row["apellidos"],
            fecha_nacimiento=birth_date,
            correo=row["correo"],
            telefono=row["telefono"],
            direccion=row["direccion"],
            categoria=row["categoria"],
            comentarios=row["comentarios"],
        )
