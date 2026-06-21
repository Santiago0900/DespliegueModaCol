class EliminarCompraUseCase:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, compra_id: int):
        self.repository.eliminar(compra_id)