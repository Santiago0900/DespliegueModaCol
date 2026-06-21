from infrastructure.api.utils.permisos import tiene_permiso

def base_context(request):
    # Recuperamos el rol directamente de la sesión que se debió setear al hacer login
    rol_nombre = request.session.get("usuario_rol_tipo", "INVITADO")

    return {
        "user_role": rol_nombre,
        "user_theme": "admin" if rol_nombre == "ADMIN" else "user",
        # Esta función es la que usaremos en el template para validar permisos reales
        "permisos_check": {
            "puedo_editar": tiene_permiso(request, "ROLES", "editar"),
            "puedo_eliminar": tiene_permiso(request, "ROLES", "eliminar"),
            "puedo_crear": tiene_permiso(request, "ROLES", "crear"),
            "puedo_ver": tiene_permiso(request, "ROLES", "ver"),
        }
    }