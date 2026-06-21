from django.http import JsonResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

from infrastructure.api.forms.proveedor_form import ProveedorForm
from infrastructure.persistence.repositories.django_proveedor_repository import DjangoProveedorRepository
from infrastructure.api.utils.context import base_context

from core.use_cases.proveedores.crear_proveedor import CrearProveedorUseCase
from core.use_cases.proveedores.listar_proveedores import ListarProveedoresUseCase
from core.use_cases.proveedores.filtrar_proveedores import FiltrarProveedoresUseCase
from core.use_cases.proveedores.obtener_proveedor import ObtenerProveedorUseCase
from core.use_cases.proveedores.actualizar_proveedor import ActualizarProveedorUseCase
from core.use_cases.proveedores.eliminar_proveedor import EliminarProveedorUseCase
from core.use_cases.proveedores.activar_proveedor import ActivarProveedorUseCase


def proveedor_to_dict(proveedor):
    return {
        "id": proveedor.id,
        "razonSocial": proveedor.razon_social,
        "identificacion": proveedor.identificacion,
        "direccion": proveedor.direccion,
        "correo": proveedor.correo,
        "contacto": proveedor.contacto,
        "activo": proveedor.activo,
    }


@csrf_exempt
@require_http_methods(["GET", "POST"])
def api_proveedores(request):
    repo = DjangoProveedorRepository()

    if request.method == "GET":
        proveedores = ListarProveedoresUseCase(repo).execute()
        return JsonResponse([proveedor_to_dict(p) for p in proveedores], safe=False)

    try:
        data = json.loads(request.body)
        proveedor = CrearProveedorUseCase(repo).execute({
            "razon_social": data.get("razonSocial"),
            "identificacion": data.get("identificacion"),
            "direccion": data.get("direccion"),
            "correo": data.get("correo"),
            "contacto": data.get("contacto"),
            "activo": data.get("activo", True),
        })
        return JsonResponse(proveedor_to_dict(proveedor), status=201)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def api_proveedor_detalle(request, id):
    repo = DjangoProveedorRepository()

    try:
        if request.method == "GET":
            proveedor = ObtenerProveedorUseCase(repo).execute(id)
            return JsonResponse(proveedor_to_dict(proveedor))

        if request.method == "PUT":
            data = json.loads(request.body)
            proveedor = ActualizarProveedorUseCase(repo).execute(id, {
                "razon_social": data.get("razonSocial"),
                "identificacion": data.get("identificacion"),
                "direccion": data.get("direccion"),
                "correo": data.get("correo"),
                "contacto": data.get("contacto"),
                "activo": data.get("activo", True),
            })
            return JsonResponse(proveedor_to_dict(proveedor))

        if request.method == "DELETE":
            EliminarProveedorUseCase(repo).execute(id)
            return JsonResponse({}, status=204)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def listar_proveedores_view(request):
    repo = DjangoProveedorRepository()

    razon_social = request.GET.get("razonSocial")
    identificacion = request.GET.get("identificacion")
    correo = request.GET.get("correo")

    if razon_social or identificacion or correo:
        proveedores = FiltrarProveedoresUseCase(repo).execute(
            razon_social=razon_social,
            identificacion=identificacion,
            correo=correo,
        )
    else:
        proveedores = ListarProveedoresUseCase(repo).execute()

    return render(request, "proveedores/list.html", {
        "proveedoresList": proveedores,
        **base_context(request),
    })


def crear_proveedor_view(request):
    form = ProveedorForm()
    return render(request, "proveedores/form.html", {
        "form": form,
        "proveedor_id": None,
        **base_context(request),
    })


def editar_proveedor_view(request, id):
    repo = DjangoProveedorRepository()
    proveedor = ObtenerProveedorUseCase(repo).execute(id)

    form = ProveedorForm(initial={
        "id": proveedor.id,
        "razon_social": proveedor.razon_social,
        "identificacion": proveedor.identificacion,
        "direccion": proveedor.direccion,
        "correo": proveedor.correo,
        "contacto": proveedor.contacto,
        "activo": proveedor.activo,
    })

    return render(request, "proveedores/form.html", {
        "form": form,
        "proveedor_id": proveedor.id,
        **base_context(request),
    })


def guardar_proveedor_view(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    form = ProveedorForm(request.POST)
    repo = DjangoProveedorRepository()

    if not form.is_valid():
        return render(request, "proveedores/form.html", {
            "form": form,
            "proveedor_id": request.POST.get("id") or None,
            **base_context(request),
        })

    data = {
        "razon_social": form.cleaned_data["razon_social"],
        "identificacion": form.cleaned_data["identificacion"],
        "direccion": form.cleaned_data.get("direccion"),
        "correo": form.cleaned_data.get("correo"),
        "contacto": form.cleaned_data.get("contacto"),
        "activo": form.cleaned_data.get("activo", True),
    }

    try:
        proveedor_id = form.cleaned_data.get("id")
        if proveedor_id:
            ActualizarProveedorUseCase(repo).execute(proveedor_id, data)
        else:
            CrearProveedorUseCase(repo).execute(data)
        return redirect("proveedores_list")
    except Exception as e:
        form.add_error(None, str(e))
        return render(request, "proveedores/form.html", {
            "form": form,
            "proveedor_id": request.POST.get("id") or None,
            **base_context(request),
        })


def eliminar_proveedor_view(request, id):
    repo = DjangoProveedorRepository()
    EliminarProveedorUseCase(repo).execute(id)
    return redirect("proveedores_list")


def activar_proveedor_view(request, id):
    repo = DjangoProveedorRepository()
    ActivarProveedorUseCase(repo).execute(id)
    return redirect("proveedores_list")