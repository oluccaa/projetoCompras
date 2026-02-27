import streamlit as st
from infrastructure.services.excel_reader import ExcelReader
from infrastructure.repositories.supabase_compra_repository import SupabaseCompraRepository
from application.use_cases.SincronizarComprasUseCase import SincronizarComprasUseCase

CAMINHO_EXCEL = r"Z:\Compras\Controladoria\TABELA_BASE_AÇOS_VITAL.xlsx"

st.title("AÇOS VITAL - SINCRONIZAÇÃO")

if st.button("SINCRONIZAR AGORA"):
    try:
        reader = ExcelReader(CAMINHO_EXCEL)
        repo = SupabaseCompraRepository()
        use_case = SincronizarComprasUseCase(repo, reader) # Corrigida a chamada da classe

        use_case.executar()

        st.success("DADOS SINCRONIZADOS COM SUCESSO")
    except Exception as e:
        st.error(f"Erro: {e}")