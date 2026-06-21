from clientes_app.models import UsuarioModel, RolPermisoModel

def permisos_sidebar(request):
    user_id = request.session.get("usuario_id")

    # Si no hay usuario en sesión, devolvemos un diccionario vacío
    if not user_id:
        return {'permisos_modulos': {}}

    try:
        usuario = UsuarioModel.objects.get(id=user_id)
        # Buscamos solo los permisos que tengan 'puede_ver' en True para este rol
        permisos = RolPermisoModel.objects.filter(rol=usuario.rol, puede_ver=True)

        # Creamos un diccionario: {'USUARIOS': True, 'VENTAS': True, ...}
        # Usamos el código del módulo en mayúsculas para evitar errores
        permisos_dict = {p.modulo.codigo.upper(): True for p in permisos}

        return {'permisos_modulos': permisos_dict}
    except Exception:
        return {'permisos_modulos': {}}