from core.domain.entities.categoria import Categoria
from core.domain.ports.categoria_repository_port import CategoriaRepositoryPort
from clientes_app.models import CategoriaModel


class DjangoCategoriaRepository(CategoriaRepositoryPort):
    def _to_domain(self, obj: CategoriaModel) -> Categoria:
        return Categoria(
            id=obj.id,
            tipo_categoria=obj.tipo_categoria,
            activo=obj.activo,
        )

    def crear(self, categoria: Categoria):
        obj = CategoriaModel.objects.create(
            tipo_categoria=categoria.tipo_categoria,
            activo=categoria.activo if categoria.activo is not None else True,
        )
        return self._to_domain(obj)

    def listar(self):
        return [self._to_domain(obj) for obj in CategoriaModel.objects.all().order_by("id")]

    def filtrar(self, tipo_categoria=None):
        qs = CategoriaModel.objects.all().order_by("id")
        if tipo_categoria:
            qs = qs.filter(tipo_categoria__icontains=tipo_categoria)
        return [self._to_domain(obj) for obj in qs]

    def obtener_por_id(self, categoria_id: int):
        try:
            obj = CategoriaModel.objects.get(id=categoria_id)
            return self._to_domain(obj)
        except CategoriaModel.DoesNotExist:
            raise RuntimeError(f"Categoría no encontrada con id: {categoria_id}")

    def actualizar(self, categoria_id: int, categoria: Categoria):
        try:
            obj = CategoriaModel.objects.get(id=categoria_id)
        except CategoriaModel.DoesNotExist:
            raise RuntimeError(f"Categoría no encontrada con id: {categoria_id}")

        obj.tipo_categoria = categoria.tipo_categoria
        obj.activo = categoria.activo
        obj.save()

        return self._to_domain(obj)

    def eliminar(self, categoria_id: int):
        try:
            obj = CategoriaModel.objects.get(id=categoria_id)
        except CategoriaModel.DoesNotExist:
            raise RuntimeError(f"Categoría no encontrada con id: {categoria_id}")

        obj.activo = False
        obj.save()

    def existe_por_nombre(self, tipo_categoria: str, excluir_id: int = None):
        qs = CategoriaModel.objects.filter(tipo_categoria__iexact=tipo_categoria.strip())

        if excluir_id:
            qs = qs.exclude(id=excluir_id)

            return qs.exists()

    def activar(self, categoria_id: int):
        try:
            obj = CategoriaModel.objects.get(id=categoria_id)
        except CategoriaModel.DoesNotExist:
            raise RuntimeError(f"Categoría no encontrada con id: {categoria_id}")

        obj.activo = True
        obj.save()