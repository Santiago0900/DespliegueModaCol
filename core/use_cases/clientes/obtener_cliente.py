class ObtenerClienteUseCase:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, cliente_id: int):
        return self.repository.obtener_por_id(cliente_id)