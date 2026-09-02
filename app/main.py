import logging

from fastapi import FastAPI, HTTPException, status
from fastapi.staticfiles import StaticFiles

from . import database
from .schemas import PersonaCreate, PersonaListResponse, PersonaResponse
from .services import (
    DuplicateEmailError,
    PersistenceError,
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


@app.post("/api/personas", response_model=PersonaResponse, status_code=status.HTTP_201_CREATED)
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


@app.get("/api/personas", response_model=list[PersonaListResponse])
def list_personas() -> list[PersonaListResponse]:
    try:
        return PersonaService().list_all()
    except PersistenceError as error:
        logger.exception("Error de persistencia al listar personas")
        raise HTTPException(
            status_code=500,
            detail="No se pudo consultar la agenda.",
        ) from error
