import streamlit as st
import pandas as pd
from infrastructure.repositories.supabase_compra_repository import SupabaseCompraRepository
from application.use_cases.listar_compras import ListarCompras

st.set_page_config(layout="wide")
st.title("PAINEL DE COTAÇÕES")

repo = SupabaseCompraRepository()
use_case = ListarCompras(repo)

compras = use_case.executar()

if compras:
    df = pd.DataFrame([c.__dict__ for c in compras])

    col1, col2, col3 = st.columns(3)
    col1.metric("ITENS", len(df))
    col2.metric("FORNECEDORES", df['fornecedor'].nunique())
    col3.metric("PREÇO MÉDIO", f"R$ {df['valor'].mean():,.2f}")

    busca = st.text_input("Pesquisar")

    if busca:
        df = df[df.astype(str).apply(lambda x: x.str.contains(busca, case=False)).any(axis=1)]

    st.dataframe(df, use_container_width=True)
else:
    st.warning("Nenhum dado encontrado.")