from django.shortcuts import render, redirect
from django.contrib import messages

from infrastructure.persistence.repositories.django_mensaje_repository import DjangoMensajeRepository
from infrastructure.api.utils.context import base_context
from core.use_cases.mensajes.enviar_mensaje import EnviarMensajeUseCase
from core.use_cases.mensajes.obtener_mensajes import ObtenerMensajesUseCase
from core.use_cases.mensajes.marcar_leido import MarcarLeidoUseCase

from clientes_app.models import UsuarioModel


def obtener_user_id(request):
    return request.session.get("usuario_id")


def mensajes_view(request):
    repo = DjangoMensajeRepository()
    user_id = obtener_user_id(request)

    use_case = ObtenerMensajesUseCase(repo)

    usuarios = UsuarioModel.objects.filter(activo=True).exclude(id=user_id)

    return render(request, "mensajes/index.html", {
        "recibidos": use_case.recibidos(user_id),
        "enviados": use_case.enviados(user_id),
        "usuarios": usuarios,
        **base_context(request),
    })


def enviar_mensaje_view(request):
    if request.method == "POST":
        repo = DjangoMensajeRepository()
        user_id = obtener_user_id(request)

        if not user_id:
            messages.error(request, "Sesión inválida")
            return redirect("/login")

        data = {
            "remitente_id": user_id,
            "destinatario_id": request.POST.get("destinatarioId"),
            "asunto": request.POST.get("asunto"),
            "contenido": request.POST.get("contenido"),
        }

        try:
            EnviarMensajeUseCase(repo).execute(data)
            messages.success(request, "Mensaje enviado")
        except:
            messages.error(request, "Error al enviar mensaje")

    return redirect("/mensajes")


def marcar_leido_view(request, id):
    repo = DjangoMensajeRepository()
    MarcarLeidoUseCase(repo).execute(id)
    return redirect("/mensajes")