class ObtenerUsuarioUseCase:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, usuario_id: int):
        return self.repository.obtener_por_id(usuario_id)