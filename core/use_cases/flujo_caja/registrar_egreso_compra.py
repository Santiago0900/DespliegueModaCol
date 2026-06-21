class RegistrarEgresoCompraUseCase:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, compra):
        return self.repository.registrar_egreso_por_compra(compra)