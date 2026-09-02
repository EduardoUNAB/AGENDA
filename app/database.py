import os
import sqlite3
from pathlib import Path
from typing import Any

DATABASE_PATH = Path(os.environ.get("AGENDA_DB_PATH", "agenda.db"))


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database() -> None:
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS personas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                apellidos TEXT NOT NULL,
                fecha_nacimiento TEXT,
                correo TEXT NOT NULL DEFAULT '',
                correo_normalizado TEXT NOT NULL DEFAULT '',
                telefono TEXT NOT NULL DEFAULT '',
                direccion TEXT NOT NULL DEFAULT '',
                categoria TEXT NOT NULL DEFAULT '',
                comentarios TEXT NOT NULL DEFAULT ''
            )
            """
        )
        connection.execute(
            "CREATE UNIQUE INDEX IF NOT EXISTS idx_personas_correo_normalizado "
            "ON personas(correo_normalizado) WHERE correo_normalizado <> ''"
        )


def insert_persona(values: dict[str, Any]) -> sqlite3.Row:
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO personas (
                nombre, apellidos, fecha_nacimiento, correo,
                correo_normalizado, telefono, direccion, categoria, comentarios
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                values["nombre"],
                values["apellidos"],
                values["fecha_nacimiento"],
                values["correo"],
                values["correo_normalizado"],
                values["telefono"],
                values["direccion"],
                values["categoria"],
                values["comentarios"],
            ),
        )
        return connection.execute(
            "SELECT * FROM personas WHERE id = ?", (cursor.lastrowid,)
        ).fetchone()


def find_by_normalized_email(email: str) -> sqlite3.Row | None:
    with get_connection() as connection:
        return connection.execute(
            "SELECT * FROM personas WHERE correo_normalizado = ?", (email,)
        ).fetchone()


def list_personas() -> list[sqlite3.Row]:
    with get_connection() as connection:
        return connection.execute(
            """
            SELECT * FROM personas
            ORDER BY apellidos COLLATE NOCASE ASC, nombre COLLATE NOCASE ASC, id ASC
            """
        ).fetchall()
