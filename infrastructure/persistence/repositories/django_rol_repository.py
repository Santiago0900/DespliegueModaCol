from core.domain.entities.rol import Rol
from clientes_app.models import RolModel


class DjangoRolRepository:
    def _to_domain(self, obj: RolModel) -> Rol:
        return Rol(
            id=obj.id,
            tipo=obj.tipo,
            activo=obj.activo,
        )

    def crear(self, rol: Rol):
        obj = RolModel.objects.create(
            tipo=rol.tipo,
            activo=rol.activo if rol.activo is not None else True,
        )
        return self._to_domain(obj)

    def listar(self):
        return [self._to_domain(obj) for obj in RolModel.objects.all().order_by("id")]

    def filtrar(self, tipo=None):
        qs = RolModel.objects.all().order_by("id")
        if tipo:
            qs = qs.filter(tipo__icontains=tipo)
        return [self._to_domain(obj) for obj in qs]

    def obtener_por_id(self, rol_id: int):
        try:
            obj = RolModel.objects.get(id=rol_id)
            return self._to_domain(obj)
        except RolModel.DoesNotExist:
            raise RuntimeError("Rol no encontrado")

    def actualizar(self, rol_id: int, rol: Rol):
        try:
            obj = RolModel.objects.get(id=rol_id)
        except RolModel.DoesNotExist:
            raise RuntimeError("Rol no encontrado")

        obj.tipo = rol.tipo
        obj.activo = rol.activo
        obj.save()
        return self._to_domain(obj)

    def eliminar(self, rol_id: int):
        try:
            obj = RolModel.objects.get(id=rol_id)
        except RolModel.DoesNotExist:
            raise RuntimeError("Rol no encontrado")

        obj.activo = False
        obj.save()

    def activar(self, rol_id: int):
        try:
            obj = RolModel.objects.get(id=rol_id)
        except RolModel.DoesNotExist:
            raise RuntimeError("Rol no encontrado")

        obj.activo = True
        obj.save()