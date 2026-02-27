from abc import ABC, abstractmethod
from typing import List
from domain.entities.compra import Compra

class CompraRepository(ABC):

    @abstractmethod
    def salvar_todas(self, compras: List[Compra]) -> None:
        pass

    @abstractmethod
    def listar_todas(self) -> List[Compra]:
        pass