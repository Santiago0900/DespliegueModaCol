from dataclasses import dataclass
from typing import Optional


@dataclass
class Proveedor:
    id: Optional[int] = None
    razon_social: str = ""
    identificacion: str = ""
    direccion: Optional[str] = None
    correo: Optional[str] = None
    contacto: Optional[str] = None
    activo: bool = True