"""Cliente Python independiente para la API REST de AGENDA.

Solo conoce el contrato HTTP publicado en docs/openapi.json y no importa
nada del paquete app. Usa unicamente la biblioteca estandar.

Uso desde la linea de comandos (con la API en ejecucion):

    python -m client.agenda_client listar
    python -m client.agenda_client obtener 1
    python -m client.agenda_client registrar Ana Perez --telefono "600 111 222"
"""

import argparse
import json
import sys
from typing import Any
from urllib import error, request

DEFAULT_BASE_URL = "http://127.0.0.1:8000"


class AgendaApiError(Exception):
    def __init__(self, status_code: int, detail: Any):
        self.status_code = status_code
        self.detail = detail
        super().__init__(f"HTTP {status_code}: {detail}")


class AgendaClient:
    def __init__(self, base_url: str = DEFAULT_BASE_URL, timeout: float = 10.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def listar_personas(self) -> list[dict[str, Any]]:
        return self._request("GET", "/api/personas")

    def registrar_persona(self, persona: dict[str, Any]) -> dict[str, Any]:
        return self._request("POST", "/api/personas", persona)

    def obtener_persona(self, persona_id: int) -> dict[str, Any]:
        return self._request("GET", f"/api/personas/{persona_id}")

    def _request(self, method: str, path: str, body: dict[str, Any] | None = None) -> Any:
        data = json.dumps(body).encode("utf-8") if body is not None else None
        req = request.Request(
            self.base_url + path,
            data=data,
            method=method,
            headers={"Accept": "application/json", "Content-Type": "application/json"},
        )
        try:
            with request.urlopen(req, timeout=self.timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except error.HTTPError as http_error:
            raw = http_error.read().decode("utf-8")
            try:
                detail = json.loads(raw).get("detail", raw)
            except (ValueError, AttributeError):
                detail = raw
            raise AgendaApiError(http_error.code, detail) from http_error


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Cliente de la API de AGENDA")
    parser.add_argument("--url", default=DEFAULT_BASE_URL, help="URL base de la API")
    sub = parser.add_subparsers(dest="comando", required=True)
    sub.add_parser("listar", help="Listar personas")
    obtener = sub.add_parser("obtener", help="Consultar una persona por identificador")
    obtener.add_argument("persona_id", type=int)
    registrar = sub.add_parser("registrar", help="Registrar una persona")
    registrar.add_argument("nombre")
    registrar.add_argument("apellidos")
    for campo in ("fecha_nacimiento", "correo", "telefono", "direccion", "categoria", "comentarios"):
        registrar.add_argument(f"--{campo}", default="")
    args = parser.parse_args(argv)

    client = AgendaClient(args.url)
    try:
        if args.comando == "listar":
            resultado = client.listar_personas()
        elif args.comando == "obtener":
            resultado = client.obtener_persona(args.persona_id)
        else:
            campos = ("nombre", "apellidos", "fecha_nacimiento", "correo",
                      "telefono", "direccion", "categoria", "comentarios")
            resultado = client.registrar_persona(
                {c: getattr(args, c) for c in campos if getattr(args, c)}
            )
    except AgendaApiError as api_error:
        print(f"Error {api_error.status_code}: {api_error.detail}", file=sys.stderr)
        return 1
    except error.URLError as url_error:
        print(f"No se pudo conectar con la API: {url_error.reason}", file=sys.stderr)
        return 2
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
