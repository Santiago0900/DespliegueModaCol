class EliminarProductoUseCase:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, producto_id: int):
        self.repository.eliminar(producto_id)