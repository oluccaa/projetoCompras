import os
import time
import logging
import sys
from config import get_settings
from infrastructure.services.excel_reader import ExcelReader
from infrastructure.repositories.supabase_compra_repository import SupabaseCompraRepository
from application.use_cases.SincronizarComprasUseCase import SincronizarComprasUseCase

# Configuração do log para acompanhamento no terminal
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def executar_sincronizacao(caminho_excel):
    try:
        logging.info("Lendo planilha e enviando para o Supabase...")
        reader = ExcelReader(caminho_excel)
        repo = SupabaseCompraRepository()
        use_case = SincronizarComprasUseCase(repo, reader)
        
        use_case.executar()
        logging.info("Sincronização concluída com sucesso.")
    except Exception as e:
        logging.error(f"Erro durante a sincronização: {e}")

def iniciar_sistema():
    settings = get_settings()
    caminho_arquivo = settings.caminho_excel

    if not os.path.exists(caminho_arquivo):
        logging.error(f"Arquivo não encontrado: {caminho_arquivo}")
        sys.exit(1)

    # RECOVERY: Executa a sincronização imediatamente ao ligar o sistema.
    # Garante que qualquer alteração feita enquanto o sistema estava offline seja capturada.
    logging.info("Iniciando sistema. Executando rotina de Recovery...")
    executar_sincronizacao(caminho_arquivo)

    # WATCHER: Grava a última modificação e entra em loop de monitoramento.
    ultima_modificacao = os.path.getmtime(caminho_arquivo)
    logging.info(f"Modo Watcher ativado. Monitorando alterações em: {caminho_arquivo}")

    while True:
        try:
            # Polling a cada 3 segundos
            time.sleep(3)
            modificacao_atual = os.path.getmtime(caminho_arquivo)
            
            if modificacao_atual > ultima_modificacao:
                logging.info("Alteração detectada no Excel. Aguardando liberação do arquivo...")
                # Pausa de segurança de 5 segundos para o Excel terminar a gravação no disco
                time.sleep(5) 
                
                executar_sincronizacao(caminho_arquivo)
                
                # Atualiza a referência de tempo
                ultima_modificacao = os.path.getmtime(caminho_arquivo)
                logging.info("Aguardando novas alterações...")

        except PermissionError:
            logging.warning("O arquivo está bloqueado (sendo salvo pelo usuário). Tentando novamente...")
            time.sleep(2)
        except FileNotFoundError:
            logging.warning("Arquivo temporariamente indisponível (comportamento de salvamento).")
            time.sleep(2)
        except KeyboardInterrupt:
            logging.info("Sistema encerrado pelo usuário.")
            break
        except Exception as e:
            logging.error(f"Erro inesperado no watcher: {e}")
            time.sleep(5)

if __name__ == "__main__":
    iniciar_sistema()