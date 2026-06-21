class FiltrarUsuariosUseCase:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, nombre=None, correo=None, rol_id=None):
        return self.repository.filtrar(nombre=nombre, correo=correo, rol_id=rol_id)