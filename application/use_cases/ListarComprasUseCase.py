class ListarComprasUseCase:

    def __init__(self, repository):
        self.repository = repository

    def executar(self):
        return self.repository.listar_todas()