from typing import List
from domain.entities.compra import Compra
from domain.repositories.compras_repository import CompraRepository
from infrastructure.database.supabase_cliente import get_client

class SupabaseCompraRepository(CompraRepository):

    def __init__(self):
        self.client = get_client()

    def salvar_todas(self, compras: List[Compra]) -> None:
        dados = [compra.__dict__ for compra in compras]

        # Apaga os dados antigos usando uma condição que será sempre verdadeira,
        # sem depender de IDs numéricos ou UUIDs.
        self.client.table("compras").delete().neq("fornecedor", "N/A_INEXISTENTE").execute()

        # Insere os novos dados em lotes de 500 para evitar erro de limite de payload (Too Large)
        tamanho_lote = 500
        for i in range(0, len(dados), tamanho_lote):
            lote = dados[i:i + tamanho_lote]
            self.client.table("compras").insert(lote).execute()

    def listar_todas(self) -> List[Compra]:
        res = self.client.table("compras").select("*").execute()
        
        compras_list = []
        for item in res.data:
            # Filtra o dicionário devolvido pelo Supabase para incluir apenas 
            # as chaves que a classe Compra realmente possui
            campos_validos = {k: v for k, v in item.items() if k in Compra.__annotations__}
            compras_list.append(Compra(**campos_validos))
            
        return compras_list