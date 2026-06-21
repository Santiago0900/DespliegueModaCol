from clientes_app.models import PasswordResetTokenModel, UsuarioModel


class DjangoPasswordResetRepository:
    def crear(self, usuario_id: int, token: str):
        usuario = UsuarioModel.objects.get(id=usuario_id)
        return PasswordResetTokenModel.objects.create(
            usuario=usuario,
            token=token
        )

    def obtener_token_valido(self, token: str):
        try:
            obj = PasswordResetTokenModel.objects.select_related("usuario").get(
                token=token,
                usado=False
            )

            if obj.expiro():
                return None

            return obj
        except PasswordResetTokenModel.DoesNotExist:
            return None

    def marcar_como_usado(self, token_obj):
        token_obj.usado = True
        token_obj.save()