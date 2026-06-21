class FiltrarProductosUseCase:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, nombre=None, descripcion=None, proveedor_id=None):
        return self.repository.filtrar(
            nombre=nombre,
            descripcion=descripcion,
            proveedor_id=proveedor_id,
        )