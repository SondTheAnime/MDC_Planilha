import pandas as pd
import streamlit as st

@st.cache_data
def get_initial_data():
    return {
        "Descrição do Item": st.secrets.itens.descricoes,
        "Custo Unitário (R$)": st.secrets.itens.custos,
        "Quantidade Mensal": st.secrets.itens.quantidades,
        "Margem de Lucro (%)": st.secrets.itens.margens,
    }

def process_data(data):
    df = pd.DataFrame(data)
    df["Valor Unitário Final (R$)"] = df["Custo Unitário (R$)"] * (1 + df["Margem de Lucro (%)"] / 100)
    df["Custo Mensal Total (R$)"] = df["Valor Unitário Final (R$)"] * df["Quantidade Mensal"]
    return df 