import pandas as pd
import unicodedata
from domain.entities.compra import Compra

def normalizar_texto(texto):
    """Remove acentos, pontos e espaços das colunas para evitar quebras"""
    try:
        texto = str(texto)
        # Remove acentos
        texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8')
        # Remove pontos e espaços extras, passa a maiúsculas
        return texto.replace('.', '').strip().upper()
    except Exception:
        return str(texto)

class ExcelReader:

    def __init__(self, caminho: str):
        self.caminho = caminho

    def ler_compras(self):
        df = pd.read_excel(self.caminho)
        
        # Aplica a normalização a todos os nomes de colunas
        df.columns = [normalizar_texto(col) for col in df.columns]
        
        # Preenche os valores vazios (NaN) com string vazia
        df = df.fillna("")

        compras = []

        for _, row in df.iterrows():
            compra = Compra(
                fornecedor=str(row.get("FORNECEDOR", "")),
                status=str(row.get("STATUS", "")),
                descricao=str(row.get("DESCRICAO", "")),
                um=str(row.get("UN", "")), # Sem ponto, pois foi limpo na normalização
                valor=Compra.limpar_valor(row.get("VALOR")),
                ipi=str(row.get("IPI", "")),
                minimo=Compra.limpar_valor(row.get("MINIMO")), # Sem acento e convertido para número
                prazo=str(row.get("PRAZO", "")),
                frete=Compra.limpar_valor(row.get("FRETE")), # Convertido para número
                promocao=str(row.get("PROMOCAO", "")),
            )
            compras.append(compra)

        return compras