from typing import List
from domain.entities.compra import Compra
from domain.repositories.compra_repository import CompraRepository
from infrastructure.database.supabase_client import get_client

class SupabaseCompraRepository(CompraRepository):

    def __init__(self):
        self.client = get_client()

    def salvar_todas(self, compras: List[Compra]) -> None:
        dados = [compra.__dict__ for compra in compras]

        self.client.table("compras").delete().neq("id", 0).execute()
        self.client.table("compras").insert(dados).execute()

    def listar_todas(self) -> List[Compra]:
        res = self.client.table("compras").select("*").execute()
        return [Compra(**item) for item in res.data]