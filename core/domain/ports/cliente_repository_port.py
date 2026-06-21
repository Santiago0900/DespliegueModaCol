from abc import ABC, abstractmethod


class ClienteRepositoryPort(ABC):
    @abstractmethod
    def crear(self, cliente):
        pass

    @abstractmethod
    def listar(self):
        pass

    @abstractmethod
    def filtrar(self, empresa=None, nombre=None, identificacion=None, correo=None):
        pass

    @abstractmethod
    def obtener_por_id(self, cliente_id: int):
        pass

    @abstractmethod
    def actualizar(self, cliente_id: int, cliente):
        pass

    @abstractmethod
    def eliminar(self, cliente_id: int):
        pass