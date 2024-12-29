import pandas as pd
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

def get_env_list(key, type_cast=str):
    """Converte string do .env em lista com tipo específico"""
    return [type_cast(x.strip()) for x in os.getenv(key, '').split(',')]

def get_env_float(key, default=0.0):
    """Obtém valor float do .env"""
    return float(os.getenv(key, default))

# Dados de exemplo para teste local
DADOS_EXEMPLO = {
    "itens": {
        "descricoes": get_env_list("ITEM_DESCRICOES"),
        "custos": get_env_list("ITEM_CUSTOS", float),
        "quantidades": get_env_list("ITEM_QUANTIDADES", int),
        "margens": get_env_list("ITEM_MARGENS", int)
    },
    "salarios": {
        "cargos": get_env_list("SALARIO_CARGOS"),
        "valores": get_env_list("SALARIO_VALORES", float),
        "quantidade_funcionarios": get_env_list("SALARIO_QUANTIDADES", int),
        "impostos": {
            "inss": get_env_float("IMPOSTO_INSS", 0.20),
            "fgts": get_env_float("IMPOSTO_FGTS", 0.08),
            "IRPF": get_env_float("IMPOSTO_IRPF", 0.27),
            "decimo": get_env_float("IMPOSTO_DECIMO", 0.08)
        }
    }
}

@st.cache_data
def get_initial_data():
    try:
        dados_itens = {
            "Descrição do Item": st.secrets.itens.descricoes,
            "Custo Unitário (R$)": st.secrets.itens.custos,
            "Quantidade Mensal": st.secrets.itens.quantidades,
            "Margem de Lucro (%)": st.secrets.itens.margens
        }
        dados_salarios = {
            "cargos": st.secrets.salarios.cargos,
            "valores": st.secrets.salarios.valores,
            "quantidade": st.secrets.salarios.quantidade_funcionarios,
            "impostos": st.secrets.salarios.impostos
        }
    except:
        print("Usando dados de exemplo para teste local")
        dados_itens = {
            "Descrição do Item": DADOS_EXEMPLO["itens"]["descricoes"],
            "Custo Unitário (R$)": DADOS_EXEMPLO["itens"]["custos"],
            "Quantidade Mensal": DADOS_EXEMPLO["itens"]["quantidades"],
            "Margem de Lucro (%)": DADOS_EXEMPLO["itens"]["margens"]
        }
        dados_salarios = {
            "cargos": DADOS_EXEMPLO["salarios"]["cargos"],
            "valores": DADOS_EXEMPLO["salarios"]["valores"],
            "quantidade": DADOS_EXEMPLO["salarios"]["quantidade_funcionarios"],
            "impostos": DADOS_EXEMPLO["salarios"]["impostos"]
        }
    
    return {
        "itens": dados_itens,
        "salarios": dados_salarios
    }

def process_data(data):
    df = pd.DataFrame(data["itens"])
    
    # Calcular o custo total dos salários
    df_salarios = pd.DataFrame({
        "Cargo": data["salarios"]["cargos"],
        "Salário Base (R$)": data["salarios"]["valores"],
        "Quantidade": data["salarios"]["quantidade"]
    })
    
    # Calcular impostos e total
    impostos = data["salarios"]["impostos"]
    total_impostos = impostos["inss"] + impostos["fgts"] + impostos["IRPF"] + impostos["decimo"]
    
    # Calcular custo total dos salários
    custo_total_salarios = sum(
        salario * (1 + total_impostos) * qtd 
        for salario, qtd in zip(data["salarios"]["valores"], data["salarios"]["quantidade"])
    )
    
    # Atualizar a linha de Salário Pessoal com o custo total
    mask_salario = df["Descrição do Item"] == "Salário Pessoal"
    df.loc[mask_salario, "Custo Unitário (R$)"] = custo_total_salarios
    df.loc[mask_salario, "Quantidade Mensal"] = 1
    
    # Calcular valores finais
    df["Valor Unitário Final (R$)"] = df["Custo Unitário (R$)"] * (1 + df["Margem de Lucro (%)"] / 100)
    df["Custo Mensal Total (R$)"] = df["Valor Unitário Final (R$)"] * df["Quantidade Mensal"]
    
    return df 