from typing import Callable

from fastapi.responses import JSONResponse
from fastapi import HTTPException
from fastapi import status

from .auth.exceptions import AuthException
from .auth.exceptions import CredentialsException
from .auth.exceptions import FileTypeException
from .auth.exceptions import JWTTokenException


class JSONResponseConstructor:
    def __init__(self, default_status_code: int):
        self.default_status_code = default_status_code

    def __call__(self, content: dict, status_code: int = None) -> JSONResponse:
        return JSONResponse(
            status_code=status_code if status_code else self.default_status_code,
            content=content,
        )


json_response_constructor = JSONResponseConstructor(status.HTTP_400_BAD_REQUEST)


def auth_exception_handler(request, exc: AuthException):
    return json_response_constructor({"error": exc.error})


def credentials_exception_handler(request, exc: CredentialsException):
    raise HTTPException(status_code=exc.status, detail=exc.detail, headers=exc.headers)


def file_type_exception_handler(request, exc: FileTypeException):
    return json_response_constructor(
        {"error": exc.error}, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )


def jwt_token_exception_handler(request, exc: JWTTokenException):
    return json_response_constructor({"error": exc.error})


def exception_handlers() -> tuple[type[Exception], Callable]:
    mapping = {
        AuthException: auth_exception_handler,
        CredentialsException: credentials_exception_handler,
        FileTypeException: file_type_exception_handler,
        JWTTokenException: jwt_token_exception_handler,
    }

    for exc_cls, handler in mapping.items():
        yield exc_cls, handler
