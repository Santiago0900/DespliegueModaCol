from decimal import Decimal
from datetime import datetime
from clientes_app.models import FlujoCajaModel
from core.domain.entities.flujo_caja import FlujoCaja


class DjangoFlujoCajaRepository:
    def _parse_date(self, value):
        if not value:
            return None
        if hasattr(value, "year"):
            return value
        try:
            return datetime.strptime(str(value), "%Y-%m-%d").date()
        except Exception:
            return None

    def _to_domain(self, obj: FlujoCajaModel) -> FlujoCaja:
        return FlujoCaja(
            id=obj.id,
            fecha=obj.fecha,
            tipo_movimiento=obj.tipo_movimiento,
            descripcion=obj.descripcion,
            monto=obj.monto,
            venta_id=obj.venta_id,
            compra_id=obj.compra_id,
        )

    def crear(self, flujo: FlujoCaja):
        obj = FlujoCajaModel.objects.create(
            fecha=flujo.fecha,
            tipo_movimiento=flujo.tipo_movimiento,
            descripcion=flujo.descripcion,
            monto=flujo.monto if flujo.monto is not None else Decimal("0.00"),
            venta_id=flujo.venta_id,
            compra_id=flujo.compra_id,
        )
        return self._to_domain(obj)

    def listar(self):
        qs = FlujoCajaModel.objects.all().order_by("-fecha", "-id")
        return [self._to_domain(obj) for obj in qs]

    def filtrar(self, desde=None, hasta=None, tipo=None):
        desde = self._parse_date(desde)
        hasta = self._parse_date(hasta)

        qs = FlujoCajaModel.objects.all().order_by("-fecha", "-id")

        if desde:
            qs = qs.filter(fecha__gte=desde)
        if hasta:
            qs = qs.filter(fecha__lte=hasta)
        if tipo:
            qs = qs.filter(tipo_movimiento=tipo)

        return [self._to_domain(obj) for obj in qs]

    def calcular_ingresos(self, desde=None, hasta=None):
        movimientos = self.filtrar(desde, hasta, "INGRESO")
        total = Decimal("0.00")
        for m in movimientos:
            total += m.monto or Decimal("0.00")
        return total

    def calcular_egresos(self, desde=None, hasta=None):
        movimientos = self.filtrar(desde, hasta, "EGRESO")
        total = Decimal("0.00")
        for m in movimientos:
            total += m.monto or Decimal("0.00")
        return total

    def calcular_saldo(self, desde=None, hasta=None):
        return self.calcular_ingresos(desde, hasta) - self.calcular_egresos(desde, hasta)

    def existe_ingreso_venta(self, venta_id: int) -> bool:
        return FlujoCajaModel.objects.filter(venta_id=venta_id, tipo_movimiento="INGRESO").exists()

    def existe_egreso_compra(self, compra_id: int) -> bool:
        return FlujoCajaModel.objects.filter(compra_id=compra_id, tipo_movimiento="EGRESO").exists()

    def registrar_egreso_por_compra(self, compra):
        if self.existe_egreso_compra(compra.id):
            return None

        descripcion = f"Compra {compra.numero_compra}"
        return self.crear(
            FlujoCaja(
                fecha=compra.fecha_compra,
                tipo_movimiento="EGRESO",
                descripcion=descripcion,
                monto=compra.total,
                venta_id=None,
                compra_id=compra.id,
            )
        )