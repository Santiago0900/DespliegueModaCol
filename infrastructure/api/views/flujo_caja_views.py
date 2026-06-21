from django.shortcuts import render
from infrastructure.persistence.repositories.django_flujo_caja_repository import DjangoFlujoCajaRepository
from core.use_cases.flujo_caja.filtrar_flujo_caja import FiltrarFlujoCajaUseCase
from core.use_cases.flujo_caja.calcular_ingresos import CalcularIngresosUseCase
from core.use_cases.flujo_caja.calcular_egresos import CalcularEgresosUseCase
from core.use_cases.flujo_caja.calcular_saldo import CalcularSaldoUseCase
from infrastructure.api.utils.context import base_context


def listar_flujo_caja_view(request):
    repo = DjangoFlujoCajaRepository()

    desde = request.GET.get("desde") or None
    hasta = request.GET.get("hasta") or None
    tipo = request.GET.get("tipo") or None

    movimientos = repo.filtrar(desde, hasta, tipo)
    ingresos = CalcularIngresosUseCase(repo).execute(desde, hasta)
    egresos = CalcularEgresosUseCase(repo).execute(desde, hasta)
    saldo = CalcularSaldoUseCase(repo).execute(desde, hasta)

    conteo_ingresos = len([m for m in movimientos if m.tipo_movimiento == "INGRESO"])
    conteo_egresos = len([m for m in movimientos if m.tipo_movimiento == "EGRESO"])

    return render(request, "flujo-caja/list.html", {
        "movimientos": movimientos,
        "desde": desde,
        "hasta": hasta,
        "tipo": tipo,
        "ingresos": ingresos,
        "egresos": egresos,
        "saldo": saldo,
        "conteoIngresos": conteo_ingresos,
        "conteoEgresos": conteo_egresos,
        **base_context(request),
    })