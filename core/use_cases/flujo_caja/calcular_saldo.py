class CalcularSaldoUseCase:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, desde=None, hasta=None):
        return self.repository.calcular_saldo(desde, hasta)