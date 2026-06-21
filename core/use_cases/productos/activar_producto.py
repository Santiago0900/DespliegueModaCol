class ActivarProductoUseCase:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, producto_id: int):
        self.repository.activar(producto_id)