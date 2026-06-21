from datetime import date, datetime
from decimal import Decimal
from django.shortcuts import render

from infrastructure.persistence.repositories.django_usuario_repository import DjangoUsuarioRepository
from infrastructure.persistence.repositories.django_cliente_repository import DjangoClienteRepository
from infrastructure.persistence.repositories.django_producto_repository import DjangoProductoRepository
from infrastructure.persistence.repositories.django_proveedor_repository import DjangoProveedorRepository
from infrastructure.persistence.repositories.django_venta_repository import DjangoVentaRepository
from infrastructure.persistence.repositories.django_flujo_caja_repository import DjangoFlujoCajaRepository
from infrastructure.api.utils.context import base_context


def parse_date(value):
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


def dashboard_view(request):
    usuario_repo = DjangoUsuarioRepository()
    cliente_repo = DjangoClienteRepository()
    producto_repo = DjangoProductoRepository()
    proveedor_repo = DjangoProveedorRepository()
    venta_repo = DjangoVentaRepository()
    flujo_repo = DjangoFlujoCajaRepository()

    hoy = date.today()
    inicio_mes = hoy.replace(day=1)

    fecha_inicio = parse_date(request.GET.get("fechaInicio")) or inicio_mes
    fecha_fin = parse_date(request.GET.get("fechaFin")) or hoy

    usuarios = usuario_repo.listar()
    clientes = cliente_repo.listar()
    productos = producto_repo.listar()
    proveedores = proveedor_repo.listar()

    # Ventas del periodo filtrado
    ventas = venta_repo.filtrar(fecha_inicio, fecha_fin, None)

    # Movimientos del periodo filtrado
    movimientos = flujo_repo.filtrar(fecha_inicio, fecha_fin)

    # Ventas de HOY reales, no afectadas por el filtro
    ventas_hoy = venta_repo.filtrar(hoy, hoy, None)

    # Ventas del mes actual real
    ventas_mes = venta_repo.filtrar(inicio_mes, hoy, None)

    ingresos_mes = sum((v.total or Decimal("0.00")) for v in ventas_mes)

    productos_stock_bajo = len([
        p for p in productos
        if (p.cantidad or 0) < 10 and getattr(p, "activo", True)
    ])

    # Últimas ventas del periodo filtrado
    ultimas_ventas = sorted(
        ventas,
        key=lambda v: (v.fecha_venta or date.min, v.id or 0),
        reverse=True
    )[:5]

    productos_populares = sorted(
        [p for p in productos if getattr(p, "activo", True)],
        key=lambda p: (p.cantidad if p.cantidad is not None else 0)
    )[:5]

    totales_por_dia = {}
    for venta in ventas:
        if venta.fecha_venta:
            totales_por_dia.setdefault(venta.fecha_venta, Decimal("0.00"))
            totales_por_dia[venta.fecha_venta] += (venta.total or Decimal("0.00"))

    fechas_ordenadas = sorted(totales_por_dia.keys())
    chart_labels = [f"{f.day}/{f.month}" for f in fechas_ordenadas]
    chart_data = [float(totales_por_dia[f]) for f in fechas_ordenadas]

    ingresos_periodo = sum(
        (m.monto or Decimal("0.00"))
        for m in movimientos
        if m.tipo_movimiento == "INGRESO"
    )

    egresos_periodo = sum(
        (m.monto or Decimal("0.00"))
        for m in movimientos
        if m.tipo_movimiento == "EGRESO"
    )

    saldo_periodo = ingresos_periodo - egresos_periodo

    return render(request, "dashboard/index.html", {
        "totalUsuarios": len([u for u in usuarios if getattr(u, "activo", True)]),
        "totalClientes": len([c for c in clientes if getattr(c, "activo", True)]),
        "totalProductos": len([p for p in productos if getattr(p, "activo", True)]),
        "totalProveedores": len([p for p in proveedores if getattr(p, "activo", True)]),

        "ventasHoy": len(ventas_hoy),
        "ventasMes": len(ventas_mes),
        "ingresosMes": ingresos_mes,

        "productosStockBajo": productos_stock_bajo,
        "ultimasVentas": ultimas_ventas,
        "productosPopulares": productos_populares,

        "chartLabels": chart_labels,
        "chartData": chart_data,

        "fechaInicio": fecha_inicio.strftime("%Y-%m-%d"),
        "fechaFin": fecha_fin.strftime("%Y-%m-%d"),

        "ingresosPeriodo": ingresos_periodo,
        "egresosPeriodo": egresos_periodo,
        "saldoPeriodo": saldo_periodo,

        **base_context(request),
    })