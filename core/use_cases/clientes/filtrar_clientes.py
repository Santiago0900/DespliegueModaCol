class FiltrarClientesUseCase:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, empresa=None, nombre=None, identificacion=None, correo=None):
        return self.repository.filtrar(
            empresa=empresa,
            nombre=nombre,
            identificacion=identificacion,
            correo=correo,
        )