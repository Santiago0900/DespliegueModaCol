from django.core.management.base import BaseCommand
from clientes_app.models import RolModel, ModuloModel, RolPermisoModel

class Command(BaseCommand):
    help = "Asigna todos los permisos al rol ADMIN"

    def handle(self, *args, **kwargs):
        try:
            rol = RolModel.objects.get(tipo="ADMIN")
        except RolModel.DoesNotExist:
            self.stdout.write(self.style.ERROR(" No existe el rol ADMIN"))
            return

        modulos = ModuloModel.objects.all()

        RolPermisoModel.objects.filter(rol=rol).delete()

        for modulo in modulos:
            RolPermisoModel.objects.create(
                rol=rol,
                modulo=modulo,
                puede_ver=True,
                puede_crear=True,
                puede_editar=True,
                puede_eliminar=True,
            )

        self.stdout.write(self.style.SUCCESS(" ADMIN ahora es DIOS en el sistema"))