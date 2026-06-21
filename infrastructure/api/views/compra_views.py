from decimal import Decimal
from django.http import JsonResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

import json

from infrastructure.api.forms.compra_form import CompraForm
from infrastructure.persistence.repositories.django_compra_repository import DjangoCompraRepository
from infrastructure.persistence.repositories.django_producto_repository import DjangoProductoRepository
from infrastructure.persistence.repositories.django_proveedor_repository import DjangoProveedorRepository
from infrastructure.persistence.repositories.django_usuario_repository import DjangoUsuarioRepository
from infrastructure.api.utils.context import base_context

from core.use_cases.compras.crear_compra import CrearCompraUseCase
from core.use_cases.compras.listar_compras import ListarComprasUseCase
from core.use_cases.compras.filtrar_compras import FiltrarComprasUseCase
from core.use_cases.compras.obtener_compra import ObtenerCompraUseCase
from core.use_cases.compras.actualizar_compra import ActualizarCompraUseCase
from core.use_cases.compras.eliminar_compra import EliminarCompraUseCase
from core.use_cases.compras.activar_compra import ActivarCompraUseCase


@csrf_exempt
@require_http_methods(["GET", "POST"])
def api_compras(request):
    repo = DjangoCompraRepository()

    if request.method == "GET":
        compras = ListarComprasUseCase(repo).execute()
        return JsonResponse([c.id for c in compras], safe=False)

    try:
        data = json.loads(request.body)
        usuario_id = data.get("usuario_id")
        compra = CrearCompraUseCase(repo).execute(data, usuario_id)
        return JsonResponse({"id": compra.id}, status=201)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def api_compra_detalle(request, id):
    repo = DjangoCompraRepository()

    try:
        if request.method == "GET":
            compra = ObtenerCompraUseCase(repo).execute(id)
            return JsonResponse({"id": compra.id})

        if request.method == "PUT":
            data = json.loads(request.body)
            compra = ActualizarCompraUseCase(repo).execute(id, data)
            return JsonResponse({"id": compra.id})

        if request.method == "DELETE":
            EliminarCompraUseCase(repo).execute(id)
            return JsonResponse({}, status=204)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def listar_compras_view(request):
    repo = DjangoCompraRepository()
    fecha_desde = request.GET.get("fechaDesde") or None
    fecha_hasta = request.GET.get("fechaHasta") or None
    proveedor_id = request.GET.get("proveedorId") or None

    if fecha_desde or fecha_hasta or proveedor_id:
        compras = FiltrarComprasUseCase(repo).execute(
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta,
            proveedor_id=proveedor_id,
        )
    else:
        compras = ListarComprasUseCase(repo).execute()

    return render(request, "compras/list.html", {
        "comprasList": compras,
        "proveedores": DjangoProveedorRepository().listar(),
        **base_context(request),
    })


def crear_compra_view(request):
    usuario_logueado_id = request.session.get("usuario_id")

    form = CompraForm(
        usuario_logueado_id=usuario_logueado_id,
        usuario_logueado_nombre=request.session.get("usuario_nombre", ""),
        initial={
            "estado": "PENDIENTE",
            "usuario_id": usuario_logueado_id,
        }
    )

    return render(request, "compras/form.html", {
        "form": form,
        "compra_id": None,
        "proveedores": DjangoProveedorRepository().listar(),
        "usuarios": DjangoUsuarioRepository().listar(),
        "productos": DjangoProductoRepository().listar(),
        "detalles": [{}],
        "usuario_logueado_nombre": request.session.get("usuario_nombre", ""),
        **base_context(request),
    })


def editar_compra_view(request, id):
    usuario_logueado_id = request.session.get("usuario_id")
    repo = DjangoCompraRepository()
    compra = ObtenerCompraUseCase(repo).execute(id)

    form = CompraForm(
        usuario_logueado_id=usuario_logueado_id,
        usuario_logueado_nombre=request.session.get("usuario_nombre", ""),
        initial={
            "id": compra.id,
            "numero_compra": compra.numero_compra,
            "fecha_compra": compra.fecha_compra,
            "fecha_estimada_entrega": compra.fecha_estimada_entrega,
            "proveedor_id": compra.proveedor_id,
            "usuario_id": usuario_logueado_id or compra.usuario_id,
            "usuario_nombre": request.session.get("usuario_nombre", ""),
            "estado": compra.estado,
            "observaciones": compra.observaciones,
            "activo": compra.activo,
        }
    )

    return render(request, "compras/form.html", {
        "form": form,
        "compra_id": compra.id,
        "proveedores": DjangoProveedorRepository().listar(),
        "usuarios": DjangoUsuarioRepository().listar(),
        "productos": DjangoProductoRepository().listar(),
        "detalles": compra.detalles if compra.detalles else [{}],
        "usuario_logueado_nombre": request.session.get("usuario_nombre", ""),
        **base_context(request),
    })


def guardar_compra_view(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    usuario_logueado_id = request.session.get("usuario_id")

    form = CompraForm(
        request.POST,
        usuario_logueado_id=usuario_logueado_id,
        usuario_logueado_nombre=request.session.get("usuario_nombre", "")
    )

    proveedores = DjangoProveedorRepository().listar()
    usuarios = DjangoUsuarioRepository().listar()
    productos = DjangoProductoRepository().listar()

    detalles = []

    indices = sorted({
        key.replace("detalle_producto_", "")
        for key in request.POST.keys()
        if key.startswith("detalle_producto_")
    })

    for raw_index in indices:
        producto_id = request.POST.get(f"detalle_producto_{raw_index}")
        cantidad = request.POST.get(f"detalle_cantidad_{raw_index}")
        precio = request.POST.get(f"detalle_precio_{raw_index}")

        if not producto_id and not cantidad and not precio:
            continue

        if not producto_id:
            form.add_error(None, f"Falta seleccionar el producto en la fila {int(raw_index) + 1}")
            continue

        try:
            detalles.append({
                "producto_id": int(producto_id),
                "cantidad": int(cantidad or 0),
                "precio_unitario": Decimal(precio or "0"),
            })
        except Exception:
            form.add_error(None, f"Error leyendo el detalle de la fila {int(raw_index) + 1}")

    if not detalles:
        form.add_error(None, "La compra debe tener al menos un producto.")

    if not form.is_valid():
        return render(request, "compras/form.html", {
            "form": form,
            "compra_id": request.POST.get("id") or None,
            "proveedores": proveedores,
            "usuarios": usuarios,
            "productos": productos,
            "detalles": detalles if detalles else [{}],
            "usuario_logueado_nombre": request.session.get("usuario_nombre", ""),
            **base_context(request),
        })

    data = {
        "fecha_compra": form.cleaned_data["fecha_compra"],
        "fecha_estimada_entrega": form.cleaned_data.get("fecha_estimada_entrega"),
        "proveedor_id": int(form.cleaned_data["proveedor_id"]),
        "estado": form.cleaned_data["estado"],
        "observaciones": form.cleaned_data.get("observaciones"),
        "detalles": detalles,
        "activo": form.cleaned_data.get("activo", True),
    }

    repo = DjangoCompraRepository()

    try:
        compra_id = form.cleaned_data.get("id")

        if compra_id:
            ActualizarCompraUseCase(repo).execute(compra_id, data)
        else:
            CrearCompraUseCase(repo).execute(data, usuario_logueado_id)

        return redirect("compras_list")

    except Exception as e:
        form.add_error(None, str(e))
        return render(request, "compras/form.html", {
            "form": form,
            "compra_id": request.POST.get("id") or None,
            "proveedores": proveedores,
            "usuarios": usuarios,
            "productos": productos,
            "detalles": detalles if detalles else [{}],
            "usuario_logueado_nombre": request.session.get("usuario_nombre", ""),
            **base_context(request),
        })


def eliminar_compra_view(request, id):
    repo = DjangoCompraRepository()
    EliminarCompraUseCase(repo).execute(id)
    return redirect("compras_list")


def activar_compra_view(request, id):
    repo = DjangoCompraRepository()
    ActivarCompraUseCase(repo).execute(id)
    return redirect("compras_list")