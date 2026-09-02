import re
from datetime import date
import sqlite3

from .models import Persona
from .repositories import PersonaRepository
from .schemas import PersonaCreate

CATEGORIES = {"familia", "trabajo", "amigos", "otros"}
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PHONE_PATTERN = re.compile(r"^[0-9+() .-]*$")


class PersonaValidationError(Exception):
    def __init__(self, errors: dict[str, str]):
        self.errors = errors
        super().__init__("Validation failed")


class DuplicateEmailError(Exception):
    pass


class PersistenceError(Exception):
    pass


class PersonaService:
    def __init__(self, repository: PersonaRepository | None = None):
        self.repository = repository or PersonaRepository()

    def create(self, data: PersonaCreate) -> Persona:
        values = self._validate(data)
        if values["correo_normalizado"]:
            try:
                if self.repository.exists_by_normalized_email(values["correo_normalizado"]):
                    raise DuplicateEmailError
            except sqlite3.Error as error:
                raise PersistenceError from error
        try:
            return self.repository.create(values)
        except sqlite3.IntegrityError as error:
            raise DuplicateEmailError from error
        except sqlite3.Error as error:
            raise PersistenceError from error

    def list_all(self) -> list[Persona]:
        try:
            return self.repository.list_all()
        except sqlite3.Error as error:
            raise PersistenceError from error

    @staticmethod
    def _validate(data: PersonaCreate) -> dict[str, str | None]:
        errors: dict[str, str] = {}
        nombre = data.nombre.strip()
        apellidos = data.apellidos.strip()
        correo = data.correo.strip()
        telefono = data.telefono.strip()
        categoria = data.categoria.strip()

        if not nombre:
            errors["nombre"] = "El nombre es obligatorio."
        if not apellidos:
            errors["apellidos"] = "Los apellidos son obligatorios."
        if correo and not EMAIL_PATTERN.fullmatch(correo):
            errors["correo"] = "El correo no tiene un formato valido."
        if telefono and not PHONE_PATTERN.fullmatch(telefono):
            errors["telefono"] = "El telefono contiene caracteres no permitidos."
        if data.fecha_nacimiento and data.fecha_nacimiento > date.today():
            errors["fecha_nacimiento"] = "La fecha de nacimiento no puede ser futura."
        if categoria and categoria not in CATEGORIES:
            errors["categoria"] = "La categoria debe ser familia, trabajo, amigos u otros."
        if errors:
            raise PersonaValidationError(errors)

        normalized_email = correo.casefold()
        return {
            "nombre": nombre,
            "apellidos": apellidos,
            "fecha_nacimiento": data.fecha_nacimiento.isoformat() if data.fecha_nacimiento else None,
            "correo": correo,
            "correo_normalizado": normalized_email,
            "telefono": telefono,
            "direccion": data.direccion.strip(),
            "categoria": categoria,
            "comentarios": data.comentarios.strip(),
        }
