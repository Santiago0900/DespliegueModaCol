class EliminarClienteUseCase:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, cliente_id: int):
        self.repository.eliminar(cliente_id)