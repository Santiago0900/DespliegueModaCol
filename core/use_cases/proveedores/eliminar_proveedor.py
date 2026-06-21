class EliminarProveedorUseCase:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, proveedor_id: int):
        self.repository.eliminar(proveedor_id)