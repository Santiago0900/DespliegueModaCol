from django.shortcuts import render, redirect
from infrastructure.api.forms.recuperacion_forms import (
    SolicitarRecuperacionForm,
    RestablecerPasswordForm,
)
from infrastructure.api.forms.login_form import LoginForm
from infrastructure.persistence.repositories.django_usuario_repository import DjangoUsuarioRepository
from core.use_cases.auth.login_usuario import LoginUsuarioUseCase
from infrastructure.persistence.repositories.django_usuario_repository import DjangoUsuarioRepository
from infrastructure.persistence.repositories.django_password_reset_repository import DjangoPasswordResetRepository
from infrastructure.services.email_service import EmailService
from core.use_cases.auth.solicitar_recuperacion_password import SolicitarRecuperacionPasswordUseCase
from core.use_cases.auth.restablecer_password import RestablecerPasswordUseCase

def login_view(request):
    if request.session.get("usuario_id"):
        return redirect("dashboard")

    form = LoginForm()
    error = None
    success = request.GET.get("logout")

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            correo = form.cleaned_data["correo"].strip().lower()
            password = form.cleaned_data["password"]

            resultado = LoginUsuarioUseCase(
                DjangoUsuarioRepository()
            ).execute(correo, password)

            if resultado["success"]:
                usuario = resultado["usuario"]

                request.session.flush()
                request.session["usuario_id"] = usuario.id
                request.session["usuario_nombre"] = usuario.nombre
                request.session["usuario_correo"] = usuario.correo
                request.session["usuario_rol_id"] = usuario.rol_id
                request.session["usuario_rol_tipo"] = usuario.rol_tipo
                request.session.set_expiry(60 * 60 * 8)  # 8 horas

                if usuario.rol_tipo == "FLUJO_DE_CAJA":
                    return redirect("flujo_caja_list")
                if usuario.rol_tipo == "OPERATIVO":
                    return redirect("ventas_list")
                return redirect("dashboard")

            error = resultado["message"]
        else:
            error = "Debes completar correctamente el formulario."

    return render(request, "auth/login.html", {
        "form": form,
        "error": error,
        "success": success,
    })


def logout_view(request):
    request.session.flush()
    return redirect("/login?logout=1")


def home_view(request):
    if request.session.get("usuario_id"):
        return redirect("dashboard")
    return redirect("login")

def forgot_password_view(request):
    form = SolicitarRecuperacionForm()
    enviado = False

    if request.method == "POST":
        form = SolicitarRecuperacionForm(request.POST)
        if form.is_valid():
            correo = form.cleaned_data["correo"]
            base_url = request.build_absolute_uri("/").rstrip("/")

            SolicitarRecuperacionPasswordUseCase(
                DjangoUsuarioRepository(),
                DjangoPasswordResetRepository(),
                EmailService(),
            ).execute(correo, base_url)

            enviado = True

    return render(request, "auth/forgot_password.html", {
        "form": form,
        "enviado": enviado,
    })


def reset_password_view(request, token):
    form = RestablecerPasswordForm()
    exito = False
    token_repo = DjangoPasswordResetRepository()

    token_obj = token_repo.obtener_token_valido(token)
    if not token_obj:
        return render(request, "auth/reset_password.html", {
            "form": None,
            "token_invalido": True,
            "exito": False,
        })

    if request.method == "POST":
        form = RestablecerPasswordForm(request.POST)
        if form.is_valid():
            nueva_password = form.cleaned_data["password"]

            exito = RestablecerPasswordUseCase(
                DjangoUsuarioRepository(),
                DjangoPasswordResetRepository(),
            ).execute(token, nueva_password)

    return render(request, "auth/reset_password.html", {
        "form": form,
        "token_invalido": False,
        "exito": exito,
    })