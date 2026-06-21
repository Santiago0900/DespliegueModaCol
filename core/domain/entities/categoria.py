from dataclasses import dataclass
from typing import Optional


@dataclass
class Categoria:
    id: Optional[int] = None
    tipo_categoria: str = ""
    activo: bool = True