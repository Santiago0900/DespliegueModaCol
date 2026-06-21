from dataclasses import dataclass, field
from typing import Optional
from datetime import date
from decimal import Decimal
from core.domain.entities.detalle_compra import DetalleCompra


@dataclass
class Compra:
    id: Optional[int] = None
    numero_compra: str = ""
    fecha_compra: Optional[date] = None
    fecha_estimada_entrega: Optional[date] = None
    proveedor_id: Optional[int] = None
    proveedor_nombre: Optional[str] = None
    usuario_id: Optional[int] = None
    usuario_nombre: Optional[str] = None
    estado: str = "PENDIENTE"
    observaciones: Optional[str] = None
    total: Decimal = Decimal("0.00")
    detalles: list[DetalleCompra] = field(default_factory=list)
    activo: bool = True