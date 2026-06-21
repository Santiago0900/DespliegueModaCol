from dataclasses import dataclass, field
from typing import Optional
from datetime import date
from decimal import Decimal
from core.domain.entities.detalle_venta import DetalleVenta


@dataclass
class Venta:
    id: Optional[int] = None
    numero_venta: str = ""
    fecha_venta: Optional[date] = None
    cliente_id: Optional[int] = None
    usuario_id: Optional[int] = None
    cliente_nombre: Optional[str] = None
    usuario_nombre: Optional[str] = None
    tipo_documento: str = ""
    forma_pago: str = ""
    estado: str = ""
    observaciones: Optional[str] = None
    total: Decimal = Decimal("0.00")
    detalles: list[DetalleVenta] = field(default_factory=list)
    activo: bool = True