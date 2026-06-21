class ObtenerProveedorUseCase:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, proveedor_id: int):
        return self.repository.obtener_por_id(proveedor_id)