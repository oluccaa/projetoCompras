from dataclasses import dataclass

@dataclass
class Compra:
    fornecedor: str
    status: str
    descricao: str
    um: str
    valor: float
    ipi: str
    minimo: float # Atualizado para aceitar números
    prazo: str
    frete: float  # Atualizado para aceitar números
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