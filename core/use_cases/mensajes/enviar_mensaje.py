class EnviarMensajeUseCase:
    def __init__(self, repo):
        self.repo = repo

    def execute(self, data: dict):
        if not data.get("destinatario_id"):
            raise RuntimeError("El destinatario es obligatorio")
        if not data.get("asunto"):
            raise RuntimeError("El asunto es obligatorio")
        if not data.get("contenido"):
            raise RuntimeError("El contenido es obligatorio")

        return self.repo.enviar(data)