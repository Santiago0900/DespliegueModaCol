from core.domain.entities.usuario import Usuario
from clientes_app.models import UsuarioModel, RolModel


class DjangoUsuarioRepository:
    def _to_domain(self, obj: UsuarioModel) -> Usuario:
        return Usuario(
            id=obj.id,
            nombre=obj.nombre,
            correo=obj.correo,
            password_hash=obj.password_hash,
            rol_id=obj.rol.id if obj.rol else None,
            rol_tipo=obj.rol.tipo if obj.rol else None,
            activo=obj.activo,
        )

    def crear(self, usuario: Usuario):
        try:
            rol = RolModel.objects.get(id=usuario.rol_id)
        except RolModel.DoesNotExist:
            raise RuntimeError("Rol no encontrado")

        obj = UsuarioModel.objects.create(
            nombre=usuario.nombre,
            correo=usuario.correo,
            password_hash=usuario.password_hash,
            rol=rol,
            activo=usuario.activo if usuario.activo is not None else True,
        )
        return self._to_domain(obj)

    def listar(self):
        return [
            self._to_domain(obj)
            for obj in UsuarioModel.objects.select_related("rol").all().order_by("id")
        ]

    def filtrar(self, nombre=None, correo=None, rol_id=None):
        qs = UsuarioModel.objects.select_related("rol").all().order_by("id")

        if nombre:
            qs = qs.filter(nombre__icontains=nombre)
        if correo:
            qs = qs.filter(correo__icontains=correo)
        if rol_id:
            qs = qs.filter(rol_id=rol_id)

        return [self._to_domain(obj) for obj in qs]

    def obtener_por_id(self, usuario_id: int):
        try:
            obj = UsuarioModel.objects.select_related("rol").get(id=usuario_id)
            return self._to_domain(obj)
        except UsuarioModel.DoesNotExist:
            raise RuntimeError("Usuario no encontrado")

    def obtener_por_correo(self, correo: str):
        try:
            obj = UsuarioModel.objects.select_related("rol").get(correo=correo)
            return self._to_domain(obj)
        except UsuarioModel.DoesNotExist:
            return None

    def actualizar(self, usuario_id: int, usuario: Usuario):
        try:
            obj = UsuarioModel.objects.get(id=usuario_id)
        except UsuarioModel.DoesNotExist:
            raise RuntimeError("Usuario no encontrado")

        try:
            rol = RolModel.objects.get(id=usuario.rol_id)
        except RolModel.DoesNotExist:
            raise RuntimeError("Rol no encontrado")

        obj.nombre = usuario.nombre
        obj.correo = usuario.correo
        obj.rol = rol
        obj.activo = usuario.activo

        if usuario.password_hash:
            obj.password_hash = usuario.password_hash

        obj.save()
        return self._to_domain(obj)

    def eliminar(self, usuario_id: int):
        try:
            obj = UsuarioModel.objects.get(id=usuario_id)
        except UsuarioModel.DoesNotExist:
            raise RuntimeError("Usuario no encontrado")

        obj.activo = False
        obj.save()

    def activar(self, usuario_id: int):
        try:
            obj = UsuarioModel.objects.get(id=usuario_id)
        except UsuarioModel.DoesNotExist:
            raise RuntimeError("Usuario no encontrado")

        obj.activo = True
        obj.save()