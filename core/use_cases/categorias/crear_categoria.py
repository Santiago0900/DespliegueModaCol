from core.domain.entities.categoria import Categoria
from core.use_cases.categorias.validators import validar_tipo_categoria


class CrearCategoriaUseCase:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, data: dict):
        tipo_categoria = validar_tipo_categoria(data.get("tipo_categoria"))

        if self.repository.existe_por_nombre(tipo_categoria):
            raise RuntimeError("Ya existe una categoría con ese nombre")

        categoria = Categoria(
            tipo_categoria=tipo_categoria,
            activo=data.get("activo", True),
        )
        return self.repository.crear(categoria)