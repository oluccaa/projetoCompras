from dataclasses import dataclass


@dataclass
class Compra:
    fornecedor: str
    status: str
    descricao: str
    um: str
    valor: float
    ipi: str
    minimo: str
    prazo: str
    frete: str
    promocao: str

    @staticmethod
    def limpar_valor(valor_raw):
        """
        Converte valor vindo do Excel como:
        'R$ 1.234,56' → 1234.56
        """
        if not valor_raw:
            return 0.0

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