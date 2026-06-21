class ObtenerMensajesUseCase:
    def __init__(self, repo):
        self.repo = repo

    def recibidos(self, user_id):
        return self.repo.obtener_recibidos(user_id)

    def enviados(self, user_id):
        return self.repo.obtener_enviados(user_id)