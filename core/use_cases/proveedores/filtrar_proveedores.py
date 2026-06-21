class FiltrarProveedoresUseCase:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, razon_social=None, identificacion=None, correo=None):
        return self.repository.filtrar(
            razon_social=razon_social,
            identificacion=identificacion,
            correo=correo,
        )