import streamlit as st
from infrastructure.services.excel_reader import ExcelReader
from infrastructure.repositories.supabase_compra_repository import SupabaseCompraRepository
from application.use_cases.sincronizar_compras import SincronizarCompras

CAMINHO_EXCEL = r"Z:\Compras\Controladoria\TABELA_BASE_AÇOS_VITAL.xlsx"

st.title("AÇOS VITAL - SINCRONIZAÇÃO")

if st.button("🚀 SINCRONIZAR AGORA"):
    try:
        reader = ExcelReader(CAMINHO_EXCEL)
        repo = SupabaseCompraRepository()
        use_case = SincronizarCompras(repo, reader)

        use_case.executar()

        st.success("DADOS SINCRONIZADOS COM SUCESSO")
    except Exception as e:
        st.error(f"Erro: {e}")