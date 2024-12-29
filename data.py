import pandas as pd
import streamlit as st

@st.cache_data
def get_initial_data():
    return {
        "Descrição do Item": [
            "Salário Pessoal",
            "Energia",
            "Aluguel",
            "Internet",
            "Material de Limpeza",
            "Material de Apoio",
            "Marketing",
            "Franquia",
            "Sistema"
        ],
        "Custo Unitário (R$)": [7000.00, 800.00, 2500.00, 150.00, 400.00, 600.00, 250.00, 550.00, 150.00],
        "Quantidade Mensal": [1, 1, 1, 1, 1, 1, 1, 1, 1],
        "Margem de Lucro (%)": [30, 30, 30, 30, 30, 30, 30, 30, 30],
    }

def process_data(data):
    df = pd.DataFrame(data)
    df["Valor Unitário Final (R$)"] = df["Custo Unitário (R$)"] * (1 + df["Margem de Lucro (%)"] / 100)
    df["Custo Mensal Total (R$)"] = df["Valor Unitário Final (R$)"] * df["Quantidade Mensal"]
    return df 