from fastapi import status


class BaseErrorException(Exception):
    def __init__(self, error: str):
        self.error = error


class AuthException(BaseErrorException):
    ...


class CredentialsException(Exception):
    def __init__(self):
        self.status = status.HTTP_401_UNAUTHORIZED
        self.detail = "Could not validate credentials"
        self.headers = {"WWW-Authenticate": "Bearer"}


class FileTypeException(BaseErrorException):
    ...


class JWTTokenException(BaseErrorException):
    ...
