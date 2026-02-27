import pandas as pd
import unicodedata
import hashlib
from domain.entities.compra import Compra

def normalizar_texto(texto):
    """Remove acentos, pontos e espaços das colunas para evitar quebras"""
    try:
        texto = str(texto)
        texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8')
        return texto.replace('.', '').strip().upper()
    except Exception:
        return str(texto)

class ExcelReader:

    def __init__(self, caminho: str):
        self.caminho = caminho

    def ler_compras(self):
        df = pd.read_excel(self.caminho)
        
        # Normaliza as colunas lidas do Excel
        df.columns = [normalizar_texto(col) for col in df.columns]
        
        # Preenche os valores vazios (NaN) com string vazia
        df = df.fillna("")

        # Dicionário para armazenar compras únicas baseadas na hash
        compras_unicas = {}

        for _, row in df.iterrows():
            compra = Compra(
                fornecedor=str(row.get("FORNECEDOR", "")),
                status=str(row.get("STATUS", "")),
                descricao=str(row.get("DESCRICAO", "")),
                um=str(row.get("UN", "")),
                valor=Compra.limpar_valor(row.get("VALOR")),
                ipi=str(row.get("IPI", "")),
                minimo=str(row.get("MINIMO", "")),
                prazo=str(row.get("PRAZO", "")),
                frete=str(row.get("FRETE", "")),
                promocao=str(row.get("PROMOCAO", "")),
            )
            
            # Geração da Hash MD5
            # Combina Fornecedor e Descrição para criar uma identidade única da linha
            string_base = f"{compra.fornecedor}_{compra.descricao}".upper().encode('utf-8')
            hash_linha = hashlib.md5(string_base).hexdigest()

            # O dicionário impede a entrada de itens duplicados
            if hash_linha not in compras_unicas:
                compras_unicas[hash_linha] = compra

        # Retorna apenas os valores únicos, prontos para a inserção em lote no Supabase
        return list(compras_unicas.values())