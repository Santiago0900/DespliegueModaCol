from dataclasses import dataclass
from typing import Optional
from decimal import Decimal


@dataclass
class DetalleVenta:
    id: Optional[int] = None
    venta_id: Optional[int] = None
    producto_id: Optional[int] = None
    producto_nombre: Optional[str] = None
    cantidad: int = 0
    precio_unitario: Decimal = Decimal("0.00")
    subtotal: Decimal = Decimal("0.00")