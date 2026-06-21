class ObtenerRolUseCase:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, rol_id: int):
        return self.repository.obtener_por_id(rol_id)