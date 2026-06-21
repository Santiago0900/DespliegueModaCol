class FiltrarCategoriasUseCase:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, tipo_categoria=None):
        return self.repository.filtrar(tipo_categoria=tipo_categoria)