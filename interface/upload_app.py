import sys
import logging
from config import get_settings
from infrastructure.services.excel_reader import ExcelReader
from infrastructure.repositories.supabase_compra_repository import SupabaseCompraRepository
from application.use_cases.SincronizarComprasUseCase import SincronizarComprasUseCase

# Configuração simples de log para registar a execução
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def executar_sincronizacao():
    try:
        logging.info("A iniciar a sincronização das cotações...")
        
        # Utiliza o caminho definido no ficheiro .env
        settings = get_settings()
        
        reader = ExcelReader(settings.caminho_excel)
        repo = SupabaseCompraRepository()
        use_case = SincronizarComprasUseCase(repo, reader)

        use_case.executar()
        
        logging.info("Sincronização concluída com sucesso.")
        
    except Exception as e:
        logging.error(f"Erro durante a sincronização: {e}")
        sys.exit(1)

if __name__ == "__main__":
    executar_sincronizacao()