from core.domain.entities.proveedor import Proveedor
from clientes_app.models import ProveedorModel


class DjangoProveedorRepository:
    def _to_domain(self, obj: ProveedorModel) -> Proveedor:
        return Proveedor(
            id=obj.id,
            razon_social=obj.razon_social,
            identificacion=obj.identificacion,
            direccion=obj.direccion,
            correo=obj.correo,
            contacto=obj.contacto,
            activo=obj.activo,
        )

    def crear(self, proveedor: Proveedor):
        obj = ProveedorModel.objects.create(
            razon_social=proveedor.razon_social,
            identificacion=proveedor.identificacion,
            direccion=proveedor.direccion,
            correo=proveedor.correo,
            contacto=proveedor.contacto,
            activo=proveedor.activo if proveedor.activo is not None else True,
        )
        return self._to_domain(obj)

    def listar(self):
        return [self._to_domain(obj) for obj in ProveedorModel.objects.all().order_by("id")]

    def filtrar(self, razon_social=None, identificacion=None, correo=None):
        qs = ProveedorModel.objects.all().order_by("id")

        if razon_social:
            qs = qs.filter(razon_social__icontains=razon_social)
        if identificacion:
            qs = qs.filter(identificacion__icontains=identificacion)
        if correo:
            qs = qs.filter(correo__icontains=correo)

        return [self._to_domain(obj) for obj in qs]

    def obtener_por_id(self, proveedor_id: int):
        try:
            obj = ProveedorModel.objects.get(id=proveedor_id)
            return self._to_domain(obj)
        except ProveedorModel.DoesNotExist:
            raise RuntimeError("Proveedor no encontrado")

    def actualizar(self, proveedor_id: int, proveedor: Proveedor):
        try:
            obj = ProveedorModel.objects.get(id=proveedor_id)
        except ProveedorModel.DoesNotExist:
            raise RuntimeError("Proveedor no encontrado")

        obj.razon_social = proveedor.razon_social
        obj.identificacion = proveedor.identificacion
        obj.direccion = proveedor.direccion
        obj.correo = proveedor.correo
        obj.contacto = proveedor.contacto
        obj.activo = proveedor.activo
        obj.save()

        return self._to_domain(obj)

    def eliminar(self, proveedor_id: int):
        try:
            obj = ProveedorModel.objects.get(id=proveedor_id)
        except ProveedorModel.DoesNotExist:
            raise RuntimeError("Proveedor no encontrado")

        obj.activo = False
        obj.save()

    def activar(self, proveedor_id: int):
        try:
            obj = ProveedorModel.objects.get(id=proveedor_id)
        except ProveedorModel.DoesNotExist:
            raise RuntimeError("Proveedor no encontrado")

        obj.activo = True
        obj.save()