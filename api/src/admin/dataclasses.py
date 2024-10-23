from typing import Optional

from dataclasses import dataclass


@dataclass
class AdminCreateData:
    error: Optional[str] = None
    created: bool = False
