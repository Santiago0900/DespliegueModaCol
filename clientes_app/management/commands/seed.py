from django.core.management.base import BaseCommand
from clientes_app.models import RolModel, UsuarioModel
from django.contrib.auth.hashers import make_password


class Command(BaseCommand):
    help = "Crea datos iniciales del sistema (roles y usuarios)"

    def handle(self, *args, **kwargs):

        # -------------------
        # ROLES
        # -------------------
        roles = ['ADMIN', 'OPERATIVO', 'FLUJO_DE_CAJA']

        for r in roles:
            RolModel.objects.get_or_create(
                tipo=r,
                defaults={'activo': True}
            )

        self.stdout.write(self.style.SUCCESS("✔ Roles creados"))

        # -------------------
        # USUARIOS
        # -------------------
        usuarios = [
            ('admin1@modacol.com', 'admin123', 'ADMIN', 'Admin'),
            ('admin2@modacol.com', 'admin123', 'OPERATIVO', 'Operativo'),
            ('admin3@modacol.com', 'admin123', 'FLUJO_DE_CAJA', 'Flujo'),
        ]

        for email, password, rol_name, nombre in usuarios:

            rol = RolModel.objects.get(tipo=rol_name)

            usuario, created = UsuarioModel.objects.get_or_create(
                correo=email,
                defaults={
                    'nombre': nombre,
                    'password_hash': make_password(password),
                    'rol': rol,
                    'activo': True
                }
            )

            if not created:
                usuario.password_hash = make_password(password)
                usuario.activo = True
                usuario.save()

            self.stdout.write(f"✔ Usuario listo: {email}")

        self.stdout.write(self.style.SUCCESS("✔ Seed completado correctamente"))