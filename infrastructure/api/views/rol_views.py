from django.http import JsonResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseForbidden
from clientes_app.models import RolModel, RolPermisoModel
from clientes_app.models import ModuloModel
import json

from infrastructure.api.forms.rol_form import RolForm
from infrastructure.persistence.repositories.django_rol_repository import DjangoRolRepository
from infrastructure.api.utils.context import base_context
from infrastructure.api.utils.permisos import tiene_permiso

from core.use_cases.roles.crear_rol import CrearRolUseCase
from core.use_cases.roles.listar_roles import ListarRolesUseCase
from core.use_cases.roles.obtener_rol import ObtenerRolUseCase
from core.use_cases.roles.actualizar_rol import ActualizarRolUseCase
from core.use_cases.roles.eliminar_rol import EliminarRolUseCase
from core.use_cases.roles.activar_rol import ActivarRolUseCase

def rol_to_dict(rol):
    return {
        "id": rol.id,
        "tipo": rol.tipo,
        "activo": rol.activo,
    }


# ---------------- API ----------------

@csrf_exempt
@require_http_methods(["GET", "POST"])
def api_roles(request):
    repo = DjangoRolRepository()

    if request.method == "GET":
        roles = ListarRolesUseCase(repo).execute()
        return JsonResponse([rol_to_dict(r) for r in roles], safe=False)

    try:
        data = json.loads(request.body)
        rol = CrearRolUseCase(repo).execute(data)
        return JsonResponse(rol_to_dict(rol), status=201)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def api_rol_detalle(request, id):
    repo = DjangoRolRepository()

    try:
        if request.method == "GET":
            rol = ObtenerRolUseCase(repo).execute(id)
            return JsonResponse(rol_to_dict(rol))

        if request.method == "PUT":
            data = json.loads(request.body)
            rol = ActualizarRolUseCase(repo).execute(id, data)
            return JsonResponse(rol_to_dict(rol))

        if request.method == "DELETE":
            EliminarRolUseCase(repo).execute(id)
            return JsonResponse({}, status=204)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


# ---------------- VISTAS ----------------

def listar_roles_view(request):
    if not tiene_permiso(request, "ROLES", "ver"):
        return HttpResponseForbidden("No tienes permisos para acceder a este módulo.")

    repo = DjangoRolRepository()
    roles = ListarRolesUseCase(repo).execute()

    return render(request, "roles/list.html", {
        "rolesList": roles,
        **base_context(request),
    })


def crear_rol_view(request):
    form = RolForm()
    modulos = ModuloModel.objects.all()

    return render(request, "roles/form.html", {
        "form": form,
        "rol_id": None,
        "modulos": modulos,
        "permisos": {},  # vacío
        **base_context(request),
    })


def editar_rol_view(request, id):
    repo = DjangoRolRepository()
    rol = ObtenerRolUseCase(repo).execute(id)

    # Buscamos los registros de permisos actuales
    permisos = RolPermisoModel.objects.filter(rol_id=id)

    # Creamos un diccionario donde la llave es el ID del módulo
    permisos_dict = { p.modulo_id: True for p in permisos }

    modulos = ModuloModel.objects.all()

    form = RolForm(initial={
        "id": rol.id,
        "tipo": rol.tipo,
        "activo": rol.activo,
    })

    return render(request, "roles/form.html", {
        "form": form,
        "rol_id": rol.id,
        "modulos": modulos,
        "permisos": permisos_dict,
        **base_context(request),
    })

def guardar_rol_view(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    form = RolForm(request.POST)
    repo = DjangoRolRepository()
    modulos = ModuloModel.objects.all()

    if not form.is_valid():
        return render(request, "roles/form.html", {
            "form": form,
            "rol_id": request.POST.get("id") or None,
            "modulos": modulos,
            "permisos": {},
            **base_context(request),
        })

    try:
        rol_id = request.POST.get("id")
        tipo_nombre = form.cleaned_data["tipo"].upper()

        # 1. Obtener o Crear el Rol
        if rol_id:
            rol_db = RolModel.objects.get(id=rol_id)
            rol_db.tipo = tipo_nombre
            rol_db.save()
        else:
            rol_db = RolModel.objects.create(tipo=tipo_nombre)

        # 2. LIMPIAR permisos anteriores para este rol específico
        RolPermisoModel.objects.filter(rol=rol_db).delete()

        # 3. Guardar NUEVOS permisos (Si el switch está ON, damos TODO)
        for modulo in modulos:
            field_name = f"modulo_{modulo.id}_full"
            if request.POST.get(field_name) == "on":
                RolPermisoModel.objects.create(
                    rol=rol_db,
                    modulo=modulo,
                    puede_ver=True,
                    puede_crear=True,
                    puede_editar=True,
                    puede_eliminar=True
                )

        # Actualizar sesión si el usuario actual cambió su propio rol
        if str(request.session.get("usuario_rol_id")) == str(rol_db.id):
            request.session["usuario_rol_tipo"] = rol_db.tipo
            request.session.modified = True

        return redirect("roles_list")

    except Exception as e:
        form.add_error(None, f"Error crítico al guardar: {str(e)}")
        return render(request, "roles/form.html", {
            "form": form,
            "rol_id": request.POST.get("id") or None,
            "modulos": modulos,
            **base_context(request),
        })


def eliminar_rol_view(request, id):
    repo = DjangoRolRepository()
    EliminarRolUseCase(repo).execute(id)
    return redirect("roles_list")


def activar_rol_view(request, id):
    repo = DjangoRolRepository()
    ActivarRolUseCase(repo).execute(id)
    return redirect("roles_list")