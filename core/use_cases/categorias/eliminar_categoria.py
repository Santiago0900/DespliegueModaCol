class EliminarCategoriaUseCase:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, categoria_id: int):
        self.repository.eliminar(categoria_id)