class FiltrarComprasUseCase:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, fecha_desde=None, fecha_hasta=None, proveedor_id=None):
        return self.repository.filtrar(
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta,
            proveedor_id=proveedor_id,
        )