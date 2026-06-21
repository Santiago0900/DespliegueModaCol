class ObtenerCategoriaUseCase:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, categoria_id: int):
        return self.repository.obtener_por_id(categoria_id)