from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from clientes_app.models import RolModel, UsuarioModel

class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        # ======================
        # ROLES (IDEMPOTENTE)
        # ======================
        roles = ['ADMIN', 'OPERATIVO', 'FLUJO_DE_CAJA']

        for r in roles:
            RolModel.objects.get_or_create(
                tipo=r,
                defaults={'activo': True}
            )

        # ======================
        # USUARIOS (SIN DUPLICAR)
        # ======================
        creds = [
            ('admin1@modacol.com', '12345', 'ADMIN', 'Admin'),
            ('admin2@modacol.com', '12345', 'OPERATIVO', 'Operativo'),
            ('admin3@modacol.com', '12345', 'FLUJO_DE_CAJA', 'Flujo'),
        ]

        for email, password, rol_name, nombre in creds:

            rol = RolModel.objects.get(tipo=rol_name)

            user, created = UsuarioModel.objects.get_or_create(
                correo=email,
                defaults={
                    'nombre': nombre,
                    'password_hash': make_password(password),
                    'rol': rol,
                    'activo': True
                }
            )

            # si ya existe → lo actualiza (NO duplica)
            if not created:
                user.nombre = nombre
                user.password_hash = make_password(password)
                user.rol = rol
                user.activo = True
                user.save()

            self.stdout.write(self.style.SUCCESS(
                f"✔ {email} listo"
            ))