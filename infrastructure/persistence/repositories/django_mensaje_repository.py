from clientes_app.models import MensajeModel
from core.domain.entities.mensaje import Mensaje


class DjangoMensajeRepository:

    def _to_entity(self, m):
        return Mensaje(
            id=m.id,
            remitente_id=m.remitente.id,
            remitente_nombre=m.remitente.nombre,
            destinatario_id=m.destinatario.id,
            destinatario_nombre=m.destinatario.nombre,
            asunto=m.asunto,
            contenido=m.contenido,
            fecha_envio=m.fecha_envio,
            leido=m.leido
        )

    def enviar(self, data):
        m = MensajeModel.objects.create(**data)
        return self._to_entity(m)

    def obtener_recibidos(self, user_id):
        return [
            self._to_entity(m)
            for m in MensajeModel.objects.filter(destinatario_id=user_id)
        ]

    def obtener_enviados(self, user_id):
        return [
            self._to_entity(m)
            for m in MensajeModel.objects.filter(remitente_id=user_id)
        ]

    def marcar_leido(self, id):
        MensajeModel.objects.filter(id=id).update(leido=True)

    def contar_no_leidos(self, user_id):
        return MensajeModel.objects.filter(destinatario_id=user_id, leido=False).count()