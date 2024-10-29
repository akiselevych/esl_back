import re

from .dataclasses import PasswordValidationData


class PasswordValidator:
    def __init__(self, value: str):
        self.password = value

    def check_length(self):
        if len(self.password) < 8:
            return PasswordValidationData(error="Password length must be more than 7 symbols!")

    def check_all(self):
        check_funcs = [
            self.check_length,
        ]

        for func in check_funcs:
            func_res = func()
            if func_res is not None:
                return func_res

        return None

    def validate_password(self):
        result = self.check_all()
        if result is None:
            return PasswordValidationData(success=True)
        return result


def validate_password(password: str) -> PasswordValidationData:
    validator = PasswordValidator(value=password)
    return validator.validate_password()
