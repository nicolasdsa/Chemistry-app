from fastapi import FastAPI, status
from fastapi.responses import HTMLResponse

from core.exceptions import BadRequestError, ConflictError, NotFoundError


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(NotFoundError)
    async def not_found_handler(_: FastAPI, exc: NotFoundError):
        message = str(exc) or "Recurso não encontrado."
        return HTMLResponse(content=message, status_code=status.HTTP_404_NOT_FOUND)

    @app.exception_handler(ConflictError)
    async def conflict_handler(_: FastAPI, exc: ConflictError):
        message = str(exc) or "Conflito ao processar a requisição."
        return HTMLResponse(content=message, status_code=status.HTTP_409_CONFLICT)

    @app.exception_handler(BadRequestError)
    async def bad_request_handler(_: FastAPI, exc: BadRequestError):
        message = str(exc) or "Dados inválidos na requisição."
        return HTMLResponse(content=message, status_code=status.HTTP_400_BAD_REQUEST)
