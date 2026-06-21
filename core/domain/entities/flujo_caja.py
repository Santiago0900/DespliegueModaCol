from dataclasses import dataclass
from typing import Optional
from datetime import date
from decimal import Decimal


@dataclass
class FlujoCaja:
    id: Optional[int] = None
    fecha: Optional[date] = None
    tipo_movimiento: str = ""
    descripcion: Optional[str] = None
    monto: Decimal = Decimal("0.00")
    venta_id: Optional[int] = None
    compra_id: Optional[int] = None