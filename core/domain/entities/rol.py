from dataclasses import dataclass
from typing import Optional


@dataclass
class Rol:
    id: Optional[int] = None
    tipo: str = ""
    activo: bool = True