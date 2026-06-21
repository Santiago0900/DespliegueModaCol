
class ActivarVentaUseCase:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, venta_id: int):
        self.repository.activar(venta_id)