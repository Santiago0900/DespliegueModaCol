class FiltrarVentasUseCase:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, fecha_inicio=None, fecha_fin=None, cliente_id=None):
        return self.repository.filtrar(fecha_inicio, fecha_fin, cliente_id)