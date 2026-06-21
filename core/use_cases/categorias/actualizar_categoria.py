from core.domain.entities.categoria import Categoria
from core.use_cases.categorias.validators import validar_tipo_categoria


class ActualizarCategoriaUseCase:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, categoria_id: int, data: dict):
        actual = self.repository.obtener_por_id(categoria_id)
        tipo_categoria = validar_tipo_categoria(data.get("tipo_categoria"))

        if self.repository.existe_por_nombre(tipo_categoria, excluir_id=categoria_id):
            raise RuntimeError("Ya existe una categoría con ese nombre")

        categoria = Categoria(
            id=categoria_id,
            tipo_categoria=tipo_categoria,
            activo=data.get("activo", actual.activo),
        )
        return self.repository.actualizar(categoria_id, categoria)