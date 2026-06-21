from abc import ABC, abstractmethod


class CategoriaRepositoryPort(ABC):
    @abstractmethod
    def crear(self, categoria):
        pass

    @abstractmethod
    def listar(self):
        pass

    @abstractmethod
    def filtrar(self, tipo_categoria=None):
        pass

    @abstractmethod
    def obtener_por_id(self, categoria_id: int):
        pass

    @abstractmethod
    def actualizar(self, categoria_id: int, categoria):
        pass

    @abstractmethod
    def eliminar(self, categoria_id: int):
        pass

    @abstractmethod
    def activar(self, categoria_id: int):
        pass