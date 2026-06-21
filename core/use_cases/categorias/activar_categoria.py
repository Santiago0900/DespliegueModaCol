class ActivarCategoriaUseCase:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, categoria_id: int):
        self.repository.activar(categoria_id)