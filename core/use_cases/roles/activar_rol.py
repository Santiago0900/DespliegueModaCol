class ActivarRolUseCase:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, rol_id: int):
        self.repository.activar(rol_id)