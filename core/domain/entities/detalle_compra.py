from dataclasses import dataclass
from typing import Optional
from decimal import Decimal


@dataclass
class DetalleCompra:
    id: Optional[int] = None
    compra_id: Optional[int] = None
    producto_id: Optional[int] = None
    producto_nombre: Optional[str] = None
    precio_unitario: Decimal = Decimal("0.00")
    cantidad: int = 0
    subtotal: Decimal = Decimal("0.00")