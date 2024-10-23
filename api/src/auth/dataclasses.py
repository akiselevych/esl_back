from typing import Optional
from typing import NamedTuple

from dataclasses import dataclass


@dataclass
class PasswordValidationData:
    error: Optional[str] = None
    success: Optional[bool] = None


@dataclass
class UserAuthData:
    tokens: Optional[dict] = None
    error: Optional[str] = None


class CoverImageSetData(NamedTuple):
    success: Optional[bool] = None
    error: Optional[str] = None
