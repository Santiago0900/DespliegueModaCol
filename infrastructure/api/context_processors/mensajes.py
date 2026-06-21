from infrastructure.persistence.repositories.django_mensaje_repository import DjangoMensajeRepository


def mensajes_no_leidos(request):
    user_id = request.session.get("usuario_id")

    if not user_id:
        return {"mensajesNoLeidos": 0}

    repo = DjangoMensajeRepository()
    return {
        "mensajesNoLeidos": repo.contar_no_leidos(user_id)
    }