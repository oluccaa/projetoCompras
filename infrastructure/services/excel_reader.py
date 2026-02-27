import pandas as pd
from domain.entities.compra import Compra

class ExcelReader:

    def __init__(self, caminho: str):
        self.caminho = caminho

    def ler_compras(self):
        df = pd.read_excel(self.caminho)
        df.columns = df.columns.astype(str).str.strip().str.upper()

        compras = []

        for _, row in df.iterrows():
            compra = Compra(
                fornecedor=row.get("FORNECEDOR", ""),
                status=row.get("STATUS", ""),
                descricao=row.get("DESCRICAO", ""),
                um=row.get("UN.", ""),
                valor=Compra.limpar_valor(row.get("VALOR")),
                ipi=str(row.get("IPI", "")),
                minimo=str(row.get("MÍNIMO", "")),
                prazo=str(row.get("PRAZO", "")),
                frete=str(row.get("FRETE", "")),
                promocao=str(row.get("PROMOCAO", "")),
            )
            compras.append(compra)

        return compras