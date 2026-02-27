from dataclasses import dataclass
import pandas as pd

@dataclass
class Compra:
    fornecedor: str
    status: str
    descricao: str
    um: str
    valor: float
    ipi: str
    minimo: str # Mantido como string devido a valores como "1 PEÇA"
    prazo: str
    frete: str  # Mantido como string devido a valores como "FOB" ou "CIF"
    promocao: str

    @staticmethod
    def limpar_valor(valor_raw):
        """
        Garante a conversão correta independentemente de o Pandas 
        entregar uma string formatada ou um float.
        """
        if not valor_raw or pd.isna(valor_raw):
            return 0.0

        if isinstance(valor_raw, (int, float)):
            return float(valor_raw)

        valor = (
            str(valor_raw)
            .replace("R$", "")
            .replace(".", "")
            .replace(",", ".")
            .strip()
        )

        try:
            return float(valor)
        except ValueError:
            return 0.0