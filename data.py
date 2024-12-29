import pandas as pd
import streamlit as st

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
    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")
        raise e
    
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