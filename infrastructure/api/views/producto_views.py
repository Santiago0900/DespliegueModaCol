from django.http import JsonResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

from infrastructure.api.forms.producto_form import ProductoForm
from infrastructure.persistence.repositories.django_producto_repository import DjangoProductoRepository
from infrastructure.persistence.repositories.django_proveedor_repository import DjangoProveedorRepository
from infrastructure.api.utils.context import base_context

from core.use_cases.productos.crear_producto import CrearProductoUseCase
from core.use_cases.productos.listar_productos import ListarProductosUseCase
from core.use_cases.productos.filtrar_productos import FiltrarProductosUseCase
from core.use_cases.productos.obtener_producto import ObtenerProductoUseCase
from core.use_cases.productos.actualizar_producto import ActualizarProductoUseCase
from core.use_cases.productos.eliminar_producto import EliminarProductoUseCase
from core.use_cases.productos.activar_producto import ActivarProductoUseCase



def producto_to_dict(producto):
    return {
        "id": producto.id,
        "fecha": str(producto.fecha) if producto.fecha else None,
        "nombre": producto.nombre,
        "descripcion": producto.descripcion,
        "precioUnitario": float(producto.precio_unitario),
        "cantidad": producto.cantidad,
        "proveedorId": producto.proveedor_id,
        "proveedorNombre": producto.proveedor_nombre,
        "activo": producto.activo,
    }


@csrf_exempt
@require_http_methods(["GET", "POST"])
def api_productos(request):
    repo = DjangoProductoRepository()

    if request.method == "GET":
        productos = ListarProductosUseCase(repo).execute()
        return JsonResponse([producto_to_dict(p) for p in productos], safe=False)

    try:
        data = json.loads(request.body)
        producto = CrearProductoUseCase(repo).execute({
            "fecha": data.get("fecha"),
            "nombre": data.get("nombre"),
            "descripcion": data.get("descripcion"),
            "precio_unitario": data.get("precioUnitario"),
            "cantidad": data.get("cantidad"),
            "proveedor_id": data.get("proveedorId") or None,
            "activo": data.get("activo", True),
        })
        return JsonResponse(producto_to_dict(producto), status=201)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def api_producto_detalle(request, id):
    repo = DjangoProductoRepository()

    try:
        if request.method == "GET":
            producto = ObtenerProductoUseCase(repo).execute(id)
            return JsonResponse(producto_to_dict(producto))

        if request.method == "PUT":
            data = json.loads(request.body)
            producto = ActualizarProductoUseCase(repo).execute(id, {
                "fecha": data.get("fecha"),
                "nombre": data.get("nombre"),
                "descripcion": data.get("descripcion"),
                "precio_unitario": data.get("precioUnitario"),
                "cantidad": data.get("cantidad"),
                "proveedor_id": data.get("proveedorId") or None,
                "activo": data.get("activo", True),
            })
            return JsonResponse(producto_to_dict(producto))

        if request.method == "DELETE":
            EliminarProductoUseCase(repo).execute(id)
            return JsonResponse({}, status=204)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def listar_productos_view(request):
    repo = DjangoProductoRepository()
    prov_repo = DjangoProveedorRepository()

    nombre = request.GET.get("nombre")
    descripcion = request.GET.get("descripcion")
    proveedor_id = request.GET.get("proveedorId")

    if nombre or descripcion or proveedor_id:
        productos = FiltrarProductosUseCase(repo).execute(
            nombre=nombre,
            descripcion=descripcion,
            proveedor_id=proveedor_id if proveedor_id else None,
        )
    else:
        productos = ListarProductosUseCase(repo).execute()

    return render(request, "productos/list.html", {
        "productos": productos,
        "proveedores": prov_repo.listar(),
        **base_context(request),
    })


def crear_producto_view(request):
    form = ProductoForm()
    prov_repo = DjangoProveedorRepository()

    return render(request, "productos/form.html", {
        "form": form,
        "proveedores": prov_repo.listar(),
        "producto_id": None,
        **base_context(request),
    })


def editar_producto_view(request, id):
    repo = DjangoProductoRepository()
    prov_repo = DjangoProveedorRepository()
    producto = ObtenerProductoUseCase(repo).execute(id)

    form = ProductoForm(initial={
        "id": producto.id,
        "fecha": producto.fecha,
        "nombre": producto.nombre,
        "descripcion": producto.descripcion,
        "precio_unitario": producto.precio_unitario,
        "cantidad": producto.cantidad,
        "proveedor_id": producto.proveedor_id,
        "categoria_id": producto.categoria_id,
        "activo": producto.activo,
    })

    return render(request, "productos/form.html", {
        "form": form,
        "proveedores": prov_repo.listar(),
        "producto_id": producto.id,
        **base_context(request),
    })


def guardar_producto_view(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    form = ProductoForm(request.POST)
    prov_repo = DjangoProveedorRepository()
    repo = DjangoProductoRepository()

    if not form.is_valid():
        return render(request, "productos/form.html", {
            "form": form,
            "proveedores": prov_repo.listar(),
            "producto_id": request.POST.get("id") or None,
            **base_context(request),
        })

    data = {
        "fecha": form.cleaned_data["fecha"],
        "nombre": form.cleaned_data["nombre"],
        "descripcion": form.cleaned_data.get("descripcion"),
        "precio_unitario": form.cleaned_data["precio_unitario"],
        "cantidad": form.cleaned_data["cantidad"],
        "proveedor_id": int(form.cleaned_data["proveedor_id"]) if form.cleaned_data.get("proveedor_id") else None,
        "categoria_id": int(form.cleaned_data["categoria_id"]) if form.cleaned_data.get("categoria_id") else None,
        "activo": form.cleaned_data.get("activo", True),
    }

    try:
        producto_id = form.cleaned_data.get("id")
        if producto_id:
            ActualizarProductoUseCase(repo).execute(producto_id, data)
        else:
            CrearProductoUseCase(repo).execute(data)
        return redirect("productos_list")
    except Exception as e:
        form.add_error(None, str(e))
        return render(request, "productos/form.html", {
            "form": form,
            "proveedores": prov_repo.listar(),
            "producto_id": request.POST.get("id") or None,
            **base_context(request),
        })


def eliminar_producto_view(request, id):
    repo = DjangoProductoRepository()
    EliminarProductoUseCase(repo).execute(id)
    return redirect("productos_list")


def activar_producto_view(request, id):
    repo = DjangoProductoRepository()
    ActivarProductoUseCase(repo).execute(id)
    return redirect("productos_list")