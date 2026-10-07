import logging
from typing import Annotated

from fastapi import FastAPI, HTTPException, Path, status
from fastapi.staticfiles import StaticFiles

from . import database
from .schemas import ErrorResponse, PersonaCreate, PersonaListResponse, PersonaResponse
from .services import (
    DuplicateEmailError,
    PersistenceError,
    PersonaNotFoundError,
    PersonaService,
    PersonaValidationError,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

database.initialize_database()
app = FastAPI(title="AGENDA")
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/", include_in_schema=False)
def index() -> object:
    from fastapi.responses import FileResponse

    return FileResponse("app/static/index.html")


@app.post(
    "/api/personas",
    response_model=PersonaResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["personas"],
    summary="Registrar una persona",
    description="Registra una nueva persona en la agenda y devuelve la persona creada con su identificador.",
    responses={
        409: {"description": "El correo ya esta registrado."},
        500: {"model": ErrorResponse, "description": "Error de persistencia."},
    },
)
def create_persona(persona: PersonaCreate) -> PersonaResponse:
    try:
        return PersonaService().create(persona)
    except PersonaValidationError as error:
        raise HTTPException(status_code=422, detail=error.errors) from error
    except DuplicateEmailError as error:
        raise HTTPException(
            status_code=409,
            detail={"correo": "El correo ya esta registrado."},
        ) from error
    except PersistenceError as error:
        logger.exception("Error de persistencia al registrar persona")
        raise HTTPException(
            status_code=500,
            detail="No se pudo guardar la persona.",
        ) from error


@app.get(
    "/api/personas",
    response_model=list[PersonaListResponse],
    tags=["personas"],
    summary="Listar personas",
    description="Devuelve todas las personas registradas ordenadas por apellidos y nombre.",
    responses={500: {"model": ErrorResponse, "description": "Error de persistencia."}},
)
def list_personas() -> list[PersonaListResponse]:
    try:
        return PersonaService().list_all()
    except PersistenceError as error:
        logger.exception("Error de persistencia al listar personas")
        raise HTTPException(
            status_code=500,
            detail="No se pudo consultar la agenda.",
        ) from error


@app.get(
    "/api/personas/{persona_id}",
    response_model=PersonaResponse,
    tags=["personas"],
    summary="Consultar una persona",
    description=(
        "Obtiene todos los datos de una persona registrada en la agenda "
        "a partir de su identificador. El identificador debe ser un entero positivo."
    ),
    responses={
        404: {"model": ErrorResponse, "description": "Persona no encontrada."},
        500: {"model": ErrorResponse, "description": "Error de persistencia."},
    },
)
def get_persona(
    persona_id: Annotated[
        int,
        Path(
            gt=0,
            description="Identificador numerico de la persona. Solo admite enteros positivos.",
            examples=[1],
        ),
    ],
) -> PersonaResponse:
    try:
        return PersonaService().get_by_id(persona_id)
    except PersonaNotFoundError as error:
        raise HTTPException(status_code=404, detail="Persona no encontrada") from error
    except PersistenceError as error:
        logger.exception("Error de persistencia al consultar persona")
        raise HTTPException(
            status_code=500,
            detail="No se pudo consultar la persona.",
        ) from error
