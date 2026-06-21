class FiltrarFlujoCajaUseCase:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, desde=None, hasta=None):
        return self.repository.filtrar(desde, hasta)