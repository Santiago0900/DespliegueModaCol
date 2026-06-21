import json

from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.hashers import make_password

from clientes_app.models import UsuarioModel
from infrastructure.api.forms.usuario_form import UsuarioForm
from infrastructure.persistence.repositories.django_usuario_repository import DjangoUsuarioRepository
from infrastructure.persistence.repositories.django_rol_repository import DjangoRolRepository

from core.use_cases.usuarios.crear_usuario import CrearUsuarioUseCase
from core.use_cases.usuarios.listar_usuarios import ListarUsuariosUseCase
from core.use_cases.usuarios.filtrar_usuarios import FiltrarUsuariosUseCase
from core.use_cases.usuarios.obtener_usuario import ObtenerUsuarioUseCase
from core.use_cases.usuarios.actualizar_usuario import ActualizarUsuarioUseCase
from core.use_cases.usuarios.eliminar_usuario import EliminarUsuarioUseCase
from core.use_cases.usuarios.activar_usuario import ActivarUsuarioUseCase

from infrastructure.services.token_service import generar_token_usuario, validar_token_usuario
from infrastructure.services.user_email_service import enviar_correo_bienvenida_html
from infrastructure.api.utils.context import base_context

def usuario_to_dict(usuario):
    return {
        "id": usuario.id,
        "nombre": usuario.nombre,
        "correo": usuario.correo,
        "rolId": usuario.rol_id,
        "rolTipo": usuario.rol_tipo,
        "activo": usuario.activo,
    }


# =========================
# API
# =========================

@csrf_exempt
@require_http_methods(["GET", "POST"])
def api_usuarios(request):
    repo = DjangoUsuarioRepository()

    if request.method == "GET":
        usuarios = ListarUsuariosUseCase(repo).execute()
        return JsonResponse([usuario_to_dict(u) for u in usuarios], safe=False)

    try:
        data = json.loads(request.body)
        usuario = CrearUsuarioUseCase(repo).execute({
            "nombre": data.get("nombre"),
            "correo": data.get("correo"),
            "password": data.get("password"),
            "rol_id": data.get("rolId"),
            "activo": data.get("activo", True),
        })
        return JsonResponse(usuario_to_dict(usuario), status=201)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def api_usuario_detalle(request, id):
    repo = DjangoUsuarioRepository()

    try:
        if request.method == "GET":
            usuario = ObtenerUsuarioUseCase(repo).execute(id)
            return JsonResponse(usuario_to_dict(usuario))

        if request.method == "PUT":
            data = json.loads(request.body)
            usuario = ActualizarUsuarioUseCase(repo).execute(id, {
                "nombre": data.get("nombre"),
                "correo": data.get("correo"),
                "password": data.get("password"),
                "rol_id": data.get("rolId"),
                "activo": data.get("activo", True),
            })
            return JsonResponse(usuario_to_dict(usuario))

        if request.method == "DELETE":
            EliminarUsuarioUseCase(repo).execute(id)
            return JsonResponse({}, status=204)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


# =========================
# VISTAS WEB
# =========================

def listar_usuarios_view(request):
    repo = DjangoUsuarioRepository()
    rol_repo = DjangoRolRepository()

    nombre = request.GET.get("nombre")
    correo = request.GET.get("correo")
    rol_id = request.GET.get("rolId")

    if nombre or correo or rol_id:
        usuarios = FiltrarUsuariosUseCase(repo).execute(
            nombre=nombre,
            correo=correo,
            rol_id=rol_id if rol_id else None,
        )
    else:
        usuarios = ListarUsuariosUseCase(repo).execute()

    return render(request, "usuarios/list.html", {
        "usuarios": usuarios,
        "roles": rol_repo.listar(),
        **base_context(request),
    })


def crear_usuario_view(request):
    form = UsuarioForm(initial={"activo": True})
    rol_repo = DjangoRolRepository()

    return render(request, "usuarios/form.html", {
        "form": form,
        "roles": rol_repo.listar(),
        "usuario_id": None,
        **base_context(request),
    })


def editar_usuario_view(request, id):
    repo = DjangoUsuarioRepository()
    rol_repo = DjangoRolRepository()
    usuario = ObtenerUsuarioUseCase(repo).execute(id)

    form = UsuarioForm(initial={
        "id": usuario.id,
        "nombre": usuario.nombre,
        "correo": usuario.correo,
        "rol_id": usuario.rol_id,
        "activo": usuario.activo,
    })

    return render(request, "usuarios/form.html", {
        "form": form,
        "roles": rol_repo.listar(),
        "usuario_id": usuario.id,
        **base_context(request),
    })


def guardar_usuario_view(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    form = UsuarioForm(request.POST)
    repo = DjangoUsuarioRepository()
    rol_repo = DjangoRolRepository()

    if not form.is_valid():
        return render(request, "usuarios/form.html", {
            "form": form,
            "roles": rol_repo.listar(),
            "usuario_id": request.POST.get("id") or None,
            **base_context(request),
        })

    data = {
        "nombre": form.cleaned_data["nombre"].strip(),
        "correo": form.cleaned_data["correo"].strip().lower(),
        "password": form.cleaned_data.get("password"),
        "rol_id": int(form.cleaned_data["rol_id"]),
        "activo": form.cleaned_data.get("activo", True),
    }

    try:
        usuario_id = form.cleaned_data.get("id")

        if usuario_id:
            ActualizarUsuarioUseCase(repo).execute(usuario_id, data)
        else:
            nuevo_usuario = CrearUsuarioUseCase(repo).execute(data)

            try:
                token = generar_token_usuario(nuevo_usuario.id)
                link = f"http://127.0.0.1:8000/usuarios/set-password/{token}"

                enviar_correo_bienvenida_html(
                    nombre=nuevo_usuario.nombre,
                    correo=nuevo_usuario.correo,
                    rol=nuevo_usuario.rol_tipo,
                    link=link,
                )
            except Exception as email_error:
                print("ERROR ENVIANDO CORREO DE BIENVENIDA:", email_error)

        return redirect("usuarios_list")

    except Exception as e:
        print("ERROR CREANDO/EDITANDO USUARIO:", e)
        form.add_error(None, str(e))
        return render(request, "usuarios/form.html", {
            "form": form,
            "roles": rol_repo.listar(),
            "usuario_id": request.POST.get("id") or None,
            **base_context(request),
        })


def eliminar_usuario_view(request, id):
    repo = DjangoUsuarioRepository()
    EliminarUsuarioUseCase(repo).execute(id)
    return redirect("usuarios_list")


def activar_usuario_view(request, id):
    repo = DjangoUsuarioRepository()
    ActivarUsuarioUseCase(repo).execute(id)
    return redirect("usuarios_list")


# =========================
# SET PASSWORD DESDE EMAIL
# =========================

def set_password_view(request, token):
    usuario_id = validar_token_usuario(token)

    if not usuario_id:
        return HttpResponse("Link inválido o expirado")

    if request.method == "POST":
        password = request.POST.get("password")

        if not password or len(password) < 8:
            return HttpResponse("Contraseña inválida")

        from django.contrib.auth.hashers import make_password
        from clientes_app.models import UsuarioModel

        usuario = UsuarioModel.objects.get(id=usuario_id)
        usuario.password_hash = make_password(password)
        usuario.save()

        return HttpResponse("Contraseña creada correctamente")

    return render(request, "usuarios/set_password.html", {
        "token": token
    })

