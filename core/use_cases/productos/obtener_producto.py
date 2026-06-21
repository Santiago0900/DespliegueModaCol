class ObtenerProductoUseCase:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, producto_id: int):
        return self.repository.obtener_por_id(producto_id)