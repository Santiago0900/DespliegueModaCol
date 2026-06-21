from django.db.models import Q

from core.domain.entities.cliente import Cliente
from core.domain.ports.cliente_repository_port import ClienteRepositoryPort
from clientes_app.models import ClienteModel

class DjangoClienteRepository(ClienteRepositoryPort):
    def _to_domain(self, obj: ClienteModel) -> Cliente:
        return Cliente(
            id=obj.id,
            empresa=obj.empresa,
            nombre=obj.nombre,
            identificacion=obj.identificacion,
            contacto=obj.contacto,
            correo=obj.correo,
            activo=obj.activo,
        )

    def crear(self, cliente: Cliente) -> Cliente:
        obj = ClienteModel.objects.create(
            empresa=cliente.empresa,
            nombre=cliente.nombre,
            identificacion=cliente.identificacion,
            contacto=cliente.contacto,
            correo=cliente.correo,
            activo=cliente.activo if cliente.activo is not None else True,
        )
        return self._to_domain(obj)

    def listar(self):
        return [self._to_domain(obj) for obj in ClienteModel.objects.all().order_by("id")]

    def filtrar(self, empresa=None, nombre=None, identificacion=None, correo=None):
        qs = ClienteModel.objects.all().order_by("id")

        if empresa:
            qs = qs.filter(empresa__icontains=empresa)
        if nombre:
            qs = qs.filter(nombre__icontains=nombre)
        if identificacion:
            qs = qs.filter(identificacion__icontains=identificacion)
        if correo:
            qs = qs.filter(correo__icontains=correo)

        return [self._to_domain(obj) for obj in qs]

    def obtener_por_id(self, cliente_id: int):
        try:
            obj = ClienteModel.objects.get(id=cliente_id)
            return self._to_domain(obj)
        except ClienteModel.DoesNotExist:
            raise RuntimeError(f"Cliente no encontrado con id: {cliente_id}")

    def actualizar(self, cliente_id: int, cliente: Cliente):
        try:
            obj = ClienteModel.objects.get(id=cliente_id)
        except ClienteModel.DoesNotExist:
            raise RuntimeError(f"Cliente no encontrado con id: {cliente_id}")

        obj.empresa = cliente.empresa
        obj.nombre = cliente.nombre
        obj.identificacion = cliente.identificacion
        obj.contacto = cliente.contacto
        obj.correo = cliente.correo
        obj.activo = cliente.activo
        obj.save()

        return self._to_domain(obj)


    def eliminar(self, cliente_id: int):
        try:
            obj = ClienteModel.objects.get(id=cliente_id)
        except ClienteModel.DoesNotExist:
            raise RuntimeError(f"Cliente no encontrado con id: {cliente_id}")

        obj.activo = False
        obj.save()

    def activar(self, cliente_id: int):
        try:
            obj = ClienteModel.objects.get(id=cliente_id)
        except ClienteModel.DoesNotExist:
            raise RuntimeError(f"Cliente no encontrado con id: {cliente_id}")

        obj.activo = True
        obj.save()