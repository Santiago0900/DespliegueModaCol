from django.http import JsonResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from core.use_cases.clientes.activar_cliente import ActivarClienteUseCase
import json

from core.use_cases.clientes.crear_cliente import CrearClienteUseCase
from core.use_cases.clientes.listar_clientes import ListarClientesUseCase
from core.use_cases.clientes.obtener_cliente import ObtenerClienteUseCase
from core.use_cases.clientes.actualizar_cliente import ActualizarClienteUseCase
from core.use_cases.clientes.eliminar_cliente import EliminarClienteUseCase
from core.use_cases.clientes.filtrar_clientes import FiltrarClientesUseCase
from infrastructure.api.forms.cliente_form import ClienteForm
from infrastructure.persistence.repositories.django_cliente_repository import DjangoClienteRepository
from infrastructure.api.utils.context import base_context

def cliente_to_dict(cliente):
    return {
        "id": cliente.id,
        "empresa": cliente.empresa,
        "nombre": cliente.nombre,
        "identificacion": cliente.identificacion,
        "contacto": cliente.contacto,
        "correo": cliente.correo,
        "activo": cliente.activo,
    }


# -------------------------
# API REST
# -------------------------

@csrf_exempt
@require_http_methods(["GET", "POST"])
def api_clientes(request):
    repo = DjangoClienteRepository()

    if request.method == "GET":
        clientes = ListarClientesUseCase(repo).execute()
        return JsonResponse([cliente_to_dict(c) for c in clientes], safe=False)

    try:
        data = json.loads(request.body)
        cliente = CrearClienteUseCase(repo).execute(data)
        return JsonResponse(cliente_to_dict(cliente), status=201)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def api_cliente_detalle(request, id):
    repo = DjangoClienteRepository()

    try:
        if request.method == "GET":
            cliente = ObtenerClienteUseCase(repo).execute(id)
            return JsonResponse(cliente_to_dict(cliente))

        if request.method == "PUT":
            data = json.loads(request.body)
            cliente = ActualizarClienteUseCase(repo).execute(id, data)
            return JsonResponse(cliente_to_dict(cliente))

        if request.method == "DELETE":
            EliminarClienteUseCase(repo).execute(id)
            return JsonResponse({}, status=204)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


# -------------------------
# VISTAS HTML
# -------------------------

def listar_clientes_view(request):
    repo = DjangoClienteRepository()

    empresa = request.GET.get("empresa") or None
    nombre = request.GET.get("nombre") or None
    identificacion = request.GET.get("identificacion") or None
    correo = request.GET.get("correo") or None

    if empresa or nombre or identificacion or correo:
        clientes = repo.filtrar(
            empresa=empresa,
            nombre=nombre,
            identificacion=identificacion,
            correo=correo
        )
    else:
        clientes = repo.listar()

    return render(request, "clientes/list.html", {
        "clientes": clientes,
        **base_context(request),
    })

def crear_cliente_view(request):
    form = ClienteForm(initial={"activo": True})
    return render(request, "clientes/form.html", {
        "form": form,
        "cliente_id": None,
        "user_role": "ADMIN",
        "user_theme": "admin",
    })


from clientes_app.models import ClienteModel

def editar_cliente_view(request, id):
    try:
        obj = ClienteModel.objects.get(id=id)
    except ClienteModel.DoesNotExist:
        raise RuntimeError("Cliente no encontrado")

    form = ClienteForm(instance=obj, initial={
        "id": obj.id,
        "activo": obj.activo,
    })

    return render(request, "clientes/form.html", {
        "form": form,
        "cliente_id": obj.id,
        "user_role": "ADMIN",
        "user_theme": "admin",
    })


def guardar_cliente_view(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    repo = DjangoClienteRepository()
    cliente_id = request.POST.get("id") or None
    instance = None

    if cliente_id:
        try:
            instance = ClienteModel.objects.get(id=cliente_id)
        except ClienteModel.DoesNotExist:
            instance = None

    form = ClienteForm(request.POST, instance=instance)

    if not form.is_valid():
        return render(request, "clientes/form.html", {
            "form": form,
            "cliente_id": cliente_id,
            "user_role": "ADMIN",
            "user_theme": "admin",
        })

    data = {
        "empresa": form.cleaned_data["empresa"],
        "nombre": form.cleaned_data["nombre"],
        "identificacion": form.cleaned_data["identificacion"],
        "contacto": form.cleaned_data.get("contacto"),
        "correo": form.cleaned_data.get("correo"),
        "activo": form.cleaned_data.get("activo", True),
    }

    try:
        if cliente_id:
            ActualizarClienteUseCase(repo).execute(int(cliente_id), data)
        else:
            CrearClienteUseCase(repo).execute(data)

        return redirect("clientes_list")
    except Exception as e:
        form.add_error(None, str(e))
        return render(request, "clientes/form.html", {
            "form": form,
            "cliente_id": cliente_id,
            "user_role": "ADMIN",
            "user_theme": "admin",
        })


def eliminar_cliente_view(request, id):
    repo = DjangoClienteRepository()
    EliminarClienteUseCase(repo).execute(id)
    return redirect("clientes_list")

def activar_cliente_view(request, id):
    repo = DjangoClienteRepository()
    ActivarClienteUseCase(repo).execute(id)
    return redirect("clientes_list")

