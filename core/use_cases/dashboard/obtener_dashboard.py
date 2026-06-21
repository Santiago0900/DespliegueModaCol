from datetime import date, datetime
from decimal import Decimal


class ObtenerDashboardUseCase:
    def __init__(
            self,
            usuario_repository,
            cliente_repository,
            producto_repository,
            proveedor_repository,
            venta_repository,
    ):
        self.usuario_repository = usuario_repository
        self.cliente_repository = cliente_repository
        self.producto_repository = producto_repository
        self.proveedor_repository = proveedor_repository
        self.venta_repository = venta_repository

    def execute(self, fecha_inicio=None, fecha_fin=None):
        hoy = date.today()

        # Parsear fechas si vienen como string
        if isinstance(fecha_inicio, str) and fecha_inicio:
            fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()

        if isinstance(fecha_fin, str) and fecha_fin:
            fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d").date()

        inicio_mes = hoy.replace(day=1)

        usuarios = self.usuario_repository.listar()
        clientes = self.cliente_repository.listar()
        productos = self.producto_repository.listar()
        proveedores = self.proveedor_repository.listar()
        ventas = self.venta_repository.listar()

        # Filtro general de ventas para el dashboard
        ventas_filtradas = ventas

        if fecha_inicio:
            ventas_filtradas = [
                v for v in ventas_filtradas
                if getattr(v, "fecha_venta", None) and v.fecha_venta >= fecha_inicio
            ]

        if fecha_fin:
            ventas_filtradas = [
                v for v in ventas_filtradas
                if getattr(v, "fecha_venta", None) and v.fecha_venta <= fecha_fin
            ]

        ventas_hoy = [
            v for v in ventas
            if getattr(v, "fecha_venta", None) == hoy
        ]

        # Si hay filtros, "ventasMes" pasa a ser ventas del periodo filtrado
        if fecha_inicio or fecha_fin:
            ventas_periodo = ventas_filtradas
        else:
            ventas_periodo = [
                v for v in ventas
                if getattr(v, "fecha_venta", None) is not None
                   and inicio_mes <= v.fecha_venta <= hoy
            ]

        ingresos_mes = sum(
            (getattr(v, "total", Decimal("0")) or Decimal("0"))
            for v in ventas_periodo
        )

        productos_stock_bajo = len([
            p for p in productos
            if getattr(p, "cantidad", 0) is not None and p.cantidad < 10
        ])

        ultimas_ventas = sorted(
            ventas_filtradas if (fecha_inicio or fecha_fin) else ventas,
            key=lambda v: getattr(v, "fecha_venta", None) or date.min,
            reverse=True
        )[:5]

        productos_populares = sorted(
            productos,
            key=lambda p: getattr(p, "cantidad", 0) if getattr(p, "cantidad", None) is not None else 0
        )[:5]

        totales_por_dia = {}
        for venta in ventas_periodo:
            fecha = getattr(venta, "fecha_venta", None)
            total = getattr(venta, "total", Decimal("0")) or Decimal("0")
            if fecha:
                totales_por_dia[fecha] = totales_por_dia.get(fecha, Decimal("0")) + total

        chart_labels = []
        chart_data = []

        for fecha in sorted(totales_por_dia.keys()):
            chart_labels.append(f"{fecha.day}/{fecha.month}")
            chart_data.append(float(totales_por_dia[fecha]))

        return {
            "totalUsuarios": len(usuarios),
            "totalClientes": len(clientes),
            "totalProductos": len(productos),
            "totalProveedores": len(proveedores),
            "ventasHoy": len(ventas_hoy),
            "ventasMes": len(ventas_periodo),
            "ingresosMes": ingresos_mes,
            "productosStockBajo": productos_stock_bajo,
            "ultimasVentas": ultimas_ventas,
            "productosPopulares": productos_populares,
            "chartLabels": chart_labels,
            "chartData": chart_data,
            "fechaInicio": fecha_inicio.strftime("%Y-%m-%d") if fecha_inicio else "",
            "fechaFin": fecha_fin.strftime("%Y-%m-%d") if fecha_fin else "",
        }