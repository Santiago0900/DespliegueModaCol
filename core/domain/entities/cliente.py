from dataclasses import dataclass
from typing import Optional


@dataclass
class Cliente:
    id: Optional[int] = None
    empresa: str = ""
    nombre: str = ""
    identificacion: str = ""
    contacto: Optional[str] = None
    correo: Optional[str] = None
    activo: bool = True