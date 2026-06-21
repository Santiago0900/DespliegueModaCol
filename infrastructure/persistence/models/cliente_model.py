from django.db import models


class ClienteModel(models.Model):
    empresa = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    identificacion = models.CharField(max_length=20, unique=True)
    contacto = models.CharField(max_length=20, blank=True, null=True)
    correo = models.EmailField(max_length=100, unique=True, blank=True, null=True)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "clientes"
        ordering = ["id"]

    def __str__(self):
        return f"{self.empresa} - {self.nombre}"