from dataclasses import dataclass
from typing import Optional
from datetime import date
from decimal import Decimal


@dataclass
class Producto:
    id: Optional[int] = None
    fecha: Optional[date] = None
    nombre: str = ""
    descripcion: Optional[str] = None
    precio_unitario: Decimal = Decimal("0.00")
    cantidad: int = 0
    proveedor_id: Optional[int] = None
    proveedor_nombre: Optional[str] = None
    categoria_id: Optional[int] = None
    categoria_nombre: Optional[str] = None
    activo: bool = True