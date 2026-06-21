from clientes_app.models import RolPermisoModel

def tiene_permiso(request, codigo_modulo, accion="ver"):
    rol_id = request.session.get("usuario_rol_id")

    if not rol_id: return False

    # Buscamos directamente en la DB para que el cambio sea instantáneo
    return RolPermisoModel.objects.filter(
        rol_id=rol_id,
        modulo__codigo=codigo_modulo.upper()
    ).exists()

