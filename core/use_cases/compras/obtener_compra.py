class ObtenerCompraUseCase:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, compra_id: int):
        return self.repository.obtener_por_id(compra_id)