class EliminarUsuarioUseCase:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, usuario_id: int):
        self.repository.eliminar(usuario_id)