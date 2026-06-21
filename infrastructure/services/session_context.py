def session_user(request):
    return {
        "session_user": {
            "id": request.session.get("usuario_id"),
            "nombre": request.session.get("usuario_nombre"),
            "correo": request.session.get("usuario_correo"),
            "rol_id": request.session.get("usuario_rol_id"),
            "rol_tipo": request.session.get("usuario_rol_tipo"),
        }
    }