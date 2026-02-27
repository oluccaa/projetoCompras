class SincronizarComprasUseCase:

    def __init__(self, repository, excel_reader):
        self.repository = repository
        self.excel_reader = excel_reader

    def executar(self):
        compras = self.excel_reader.ler_compras()
        self.repository.salvar_todas(compras)