from decimal import Decimal
from django.http import JsonResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from clientes_app.models import DetalleCompraModel
import json

from infrastructure.api.forms.venta_form import VentaForm
from infrastructure.persistence.repositories.django_venta_repository import DjangoVentaRepository
from infrastructure.persistence.repositories.django_producto_repository import DjangoProductoRepository
from infrastructure.persistence.repositories.django_cliente_repository import DjangoClienteRepository
from infrastructure.persistence.repositories.django_usuario_repository import DjangoUsuarioRepository
from infrastructure.persistence.repositories.django_flujo_caja_repository import DjangoFlujoCajaRepository
from infrastructure.api.utils.context import base_context

from core.use_cases.ventas.crear_venta import CrearVentaUseCase
from core.use_cases.ventas.listar_ventas import ListarVentasUseCase
from core.use_cases.ventas.filtrar_ventas import FiltrarVentasUseCase
from core.use_cases.ventas.obtener_venta import ObtenerVentaUseCase
from core.use_cases.ventas.actualizar_venta import ActualizarVentaUseCase
from core.use_cases.ventas.eliminar_venta import EliminarVentaUseCase
from core.use_cases.ventas.activar_venta import ActivarVentaUseCase
from core.domain.entities.flujo_caja import FlujoCaja


def obtener_costo_minimo_producto(producto_id: int) -> Decimal:
    detalles = DetalleCompraModel.objects.filter(producto_id=producto_id).order_by("-id")
    detalle = detalles.first()

    if detalle and detalle.precio_unitario is not None:
        return Decimal(str(detalle.precio_unitario))

    return Decimal("0.00")


def venta_to_dict(venta):
    return {
        "id": venta.id,
        "numeroVenta": venta.numero_venta,
        "fechaVenta": str(venta.fecha_venta) if venta.fecha_venta else None,
        "clienteId": venta.cliente_id,
        "usuarioId": venta.usuario_id,
        "clienteNombre": venta.cliente_nombre,
        "usuarioNombre": venta.usuario_nombre,
        "tipoDocumento": venta.tipo_documento,
        "formaPago": venta.forma_pago,
        "estado": venta.estado,
        "observaciones": venta.observaciones,
        "total": float(venta.total),
        "activo": venta.activo,
        "detalles": [
            {
                "productoId": d.producto_id,
                "productoNombre": d.producto_nombre,
                "cantidad": d.cantidad,
                "precioUnitario": float(d.precio_unitario),
                "subtotal": float(d.subtotal),
            }
            for d in venta.detalles
        ],
    }


@csrf_exempt
@require_http_methods(["GET", "POST"])
def api_ventas(request):
    repo = DjangoVentaRepository()

    if request.method == "GET":
        ventas = ListarVentasUseCase(repo).execute()
        return JsonResponse([venta_to_dict(v) for v in ventas], safe=False)

    try:
        data = json.loads(request.body)
        venta = CrearVentaUseCase(repo).execute(data)
        return JsonResponse(venta_to_dict(venta), status=201)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def api_venta_detalle(request, id):
    repo = DjangoVentaRepository()

    try:
        if request.method == "GET":
            venta = ObtenerVentaUseCase(repo).execute(id)
            return JsonResponse(venta_to_dict(venta))

        if request.method == "PUT":
            data = json.loads(request.body)
            venta = ActualizarVentaUseCase(repo).execute(id, data)
            return JsonResponse(venta_to_dict(venta))

        if request.method == "DELETE":
            EliminarVentaUseCase(repo).execute(id)
            return JsonResponse({}, status=204)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def listar_ventas_view(request):
    repo = DjangoVentaRepository()
    fecha_inicio = request.GET.get("fechaInicio") or None
    fecha_fin = request.GET.get("fechaFin") or None
    cliente_id = request.GET.get("clienteId") or None

    if fecha_inicio or fecha_fin or cliente_id:
        ventas = FiltrarVentasUseCase(repo).execute(fecha_inicio, fecha_fin, cliente_id)
    else:
        ventas = ListarVentasUseCase(repo).execute()

    return render(request, "ventas/list.html", {
        "ventas": ventas,
        "clientes": DjangoClienteRepository().listar(),
        **base_context(request),
    })


def crear_venta_view(request):
    usuario_logueado_id = request.session.get("usuario_id")

    form = VentaForm(
        usuario_logueado_id=usuario_logueado_id,
        initial={
            "tipo_documento": "FACTURA_VENTA",
            "forma_pago": "CONTADO",
            "estado": "CONFIRMADA",
            "usuario_id": usuario_logueado_id,
        }
    )

    productos_base = DjangoProductoRepository().listar()
    productos = []
    for p in productos_base:
        productos.append({
            "id": p.id,
            "nombre": p.nombre,
            "precio_unitario": p.precio_unitario,
            "costo_minimo": obtener_costo_minimo_producto(p.id),
        })

    return render(request, "ventas/form.html", {
        "form": form,
        "venta_id": None,
        "clientes": DjangoClienteRepository().listar(),
        "usuarios": DjangoUsuarioRepository().listar(),
        "productos": productos,
        "detalles": [{}],
        "usuario_logueado_nombre": request.session.get("usuario_nombre", ""),
        **base_context(request),
    })


def editar_venta_view(request, id):
    usuario_logueado_id = request.session.get("usuario_id")
    repo = DjangoVentaRepository()
    venta = ObtenerVentaUseCase(repo).execute(id)

    form = VentaForm(
        usuario_logueado_id=usuario_logueado_id,
        initial={
            "id": venta.id,
            "numero_venta": venta.numero_venta,
            "fecha_venta": venta.fecha_venta,
            "cliente_id": venta.cliente_id,
            "usuario_id": usuario_logueado_id or venta.usuario_id,
            "tipo_documento": venta.tipo_documento,
            "forma_pago": venta.forma_pago,
            "estado": venta.estado,
            "observaciones": venta.observaciones,
            "activo": venta.activo,
        }
    )

    productos_base = DjangoProductoRepository().listar()
    productos = []
    for p in productos_base:
        productos.append({
            "id": p.id,
            "nombre": p.nombre,
            "precio_unitario": p.precio_unitario,
            "costo_minimo": obtener_costo_minimo_producto(p.id),
        })

    return render(request, "ventas/form.html", {
        "form": form,
        "venta_id": venta.id,
        "clientes": DjangoClienteRepository().listar(),
        "usuarios": DjangoUsuarioRepository().listar(),
        "productos": productos,
        "detalles": venta.detalles if venta.detalles else [{}],
        "usuario_logueado_nombre": request.session.get("usuario_nombre", ""),
        **base_context(request),
    })


def guardar_venta_view(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    usuario_logueado_id = request.session.get("usuario_id")

    form = VentaForm(request.POST, usuario_logueado_id=usuario_logueado_id)
    clientes = DjangoClienteRepository().listar()
    usuarios = DjangoUsuarioRepository().listar()

    productos_base = DjangoProductoRepository().listar()
    productos = []
    for p in productos_base:
        productos.append({
            "id": p.id,
            "nombre": p.nombre,
            "precio_unitario": p.precio_unitario,
            "costo_minimo": obtener_costo_minimo_producto(p.id),
        })

    detalles = []
    index = 0

    while True:
        producto_id = request.POST.get(f"detalles[{index}].productoId")
        cantidad = request.POST.get(f"detalles[{index}].cantidad")
        precio = request.POST.get(f"detalles[{index}].precioUnitario")

        if producto_id is None and cantidad is None and precio is None:
            break

        if producto_id:
            try:
                producto_id_int = int(producto_id)
                precio_decimal = Decimal(precio or "0")
                costo_minimo = obtener_costo_minimo_producto(producto_id_int)

                if costo_minimo <= Decimal("0.00"):
                    form.add_error(
                        None,
                        f"El producto #{producto_id_int} no tiene costo de compra registrado. No se puede vender."
                    )
                elif precio_decimal < costo_minimo:
                    form.add_error(
                        None,
                        f"El precio del producto #{producto_id_int} no puede ser menor al costo de compra (${costo_minimo})."
                    )

                detalles.append({
                    "producto_id": producto_id_int,
                    "cantidad": int(cantidad or 0),
                    "precio_unitario": precio_decimal,
                })
            except Exception:
                form.add_error(None, f"Error leyendo el detalle de la fila {index + 1}")

        index += 1

    if not detalles:
        form.add_error(None, "La venta debe tener al menos un producto.")

    if not form.is_valid():
        return render(request, "ventas/form.html", {
            "form": form,
            "venta_id": request.POST.get("id") or None,
            "clientes": clientes,
            "usuarios": usuarios,
            "productos": productos,
            "detalles": detalles if detalles else [{}],
            "usuario_logueado_nombre": request.session.get("usuario_nombre", ""),
            **base_context(request),
        })

    data = {
        "fecha_venta": form.cleaned_data["fecha_venta"],
        "cliente_id": int(form.cleaned_data["cliente_id"]),
        "usuario_id": int(usuario_logueado_id) if usuario_logueado_id else int(form.cleaned_data["usuario_id"]),
        "tipo_documento": form.cleaned_data["tipo_documento"],
        "forma_pago": form.cleaned_data["forma_pago"],
        "estado": form.cleaned_data["estado"],
        "observaciones": form.cleaned_data.get("observaciones"),
        "detalles": detalles,
        "activo": form.cleaned_data.get("activo", True),
    }

    repo = DjangoVentaRepository()

    try:
        venta_id = form.cleaned_data.get("id")

        if venta_id:
            venta = ActualizarVentaUseCase(repo).execute(venta_id, data)
        else:
            venta = CrearVentaUseCase(repo).execute(data)

        if venta.estado in ["CONFIRMADA", "PAGADA"]:
            flujo_repo = DjangoFlujoCajaRepository()

            if not flujo_repo.existe_ingreso_venta(venta.id):
                flujo_repo.crear(
                    FlujoCaja(
                        fecha=venta.fecha_venta,
                        tipo_movimiento="INGRESO",
                        descripcion=f"Venta {venta.numero_venta}",
                        monto=venta.total,
                        venta_id=venta.id,
                        compra_id=None,
                    )
                )

        return redirect("ventas_list")

    except Exception as e:
        form.add_error(None, str(e))
        return render(request, "ventas/form.html", {
            "form": form,
            "venta_id": request.POST.get("id") or None,
            "clientes": clientes,
            "usuarios": usuarios,
            "productos": productos,
            "detalles": detalles if detalles else [{}],
            "usuario_logueado_nombre": request.session.get("usuario_nombre", ""),
            **base_context(request),
        })


def eliminar_venta_view(request, id):
    repo = DjangoVentaRepository()
    EliminarVentaUseCase(repo).execute(id)
    return redirect("ventas_list")


def activar_venta_view(request, id):
    repo = DjangoVentaRepository()
    ActivarVentaUseCase(repo).execute(id)
    return redirect("ventas_list")