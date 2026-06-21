from dataclasses import dataclass
from typing import Optional


@dataclass
class Usuario:
    id: Optional[int] = None
    nombre: str = ""
    correo: str = ""
    password_hash: str = ""
    rol_id: Optional[int] = None
    rol_tipo: Optional[str] = None
    activo: bool = True