from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Mensaje:
    id: Optional[int] = None
    remitente_id: Optional[int] = None
    remitente_nombre: Optional[str] = None
    destinatario_id: Optional[int] = None
    destinatario_nombre: Optional[str] = None
    asunto: str = ""
    contenido: str = ""
    fecha_envio: Optional[datetime] = None
    leido: bool = False