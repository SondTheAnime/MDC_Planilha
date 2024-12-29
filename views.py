import streamlit as st
import plotly.express as px
import pandas as pd

def show_metrics(df, data):
    df_salarios = create_salary_df(data)
    total_salarios = df_salarios["Custo Total Mensal (R$)"].sum()
    
    col1, col2, col3 = st.columns(3)
    total = df['Custo Mensal Total (R$)'].sum() + total_salarios
    media = total / (len(df) + len(df_salarios))
    qtd_items = len(df) + len(df_salarios)

    with col1:
        st.metric(
            "Custo Mensal Total",
            f"R$ {total:,.2f}",
            delta=f"{((total/media)-1)*100:.1f}% da média"
        )
    with col2:
        st.metric(
            "Custo Médio por Item",
            f"R$ {media:,.2f}"
        )
    with col3:
        st.metric(
            "Quantidade de Itens",
            f"{qtd_items}"
        )

def show_bar_chart(df):
    st.plotly_chart(
        px.bar(
            df,
            x='Descrição do Item',
            y='Custo Mensal Total (R$)',
            title='Visão Geral dos Custos',
            color='Custo Mensal Total (R$)',
            color_continuous_scale='Viridis'
        ).update_layout(
            height=400,
            showlegend=False
        ),
        use_container_width=True
    )

def show_detailed_analysis(df, data):
    # Criar um DataFrame combinado sem os detalhes dos cargos
    df_combined = df.copy()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        show_detailed_table(df_combined)
    
    with col2:
        show_pie_chart(df_combined)
        show_cost_analysis(df_combined)

def show_detailed_table(df):
    st.subheader("Tabela Detalhada")
    st.dataframe(
        df.style.format({
            'Custo Unitário (R$)': 'R${:,.2f}',
            'Valor Unitário Final (R$)': 'R${:,.2f}',
            'Custo Mensal Total (R$)': 'R${:,.2f}',
            'Margem de Lucro (%)': '{:.0f}%'
        }).background_gradient(
            subset=['Custo Mensal Total (R$)'],
            cmap='YlOrRd'
        ),
        use_container_width=True
    )

def show_pie_chart(df):
    st.subheader("Distribuição dos Custos")
    fig_pie = px.pie(
        df,
        values='Custo Mensal Total (R$)',
        names='Descrição do Item',
        hole=0.4
    )
    st.plotly_chart(fig_pie, use_container_width=True)

def show_cost_analysis(df):
    total = df['Custo Mensal Total (R$)'].sum()
    mais_custoso = df.loc[df['Custo Mensal Total (R$)'].idxmax()]
    st.info(f"""
        💡 **Análise Rápida**
        - Item mais custoso: {mais_custoso['Descrição do Item']}
        - Custo: R$ {mais_custoso['Custo Mensal Total (R$)']:,.2f}
        - Representa {(mais_custoso['Custo Mensal Total (R$)']/total*100):.1f}% do total
    """) 

def show_salary_analysis(df, data):
    st.subheader("Análise de Salários por Cargo")
    
    # Criar DataFrame de salários com impostos
    df_salarios = pd.DataFrame({
        "Cargo": data["salarios"]["cargos"],
        "Salário Base (R$)": data["salarios"]["valores"],
        "Quantidade": data["salarios"]["quantidade"]
    })
    
    # Calcular impostos e encargos
    impostos = data["salarios"]["impostos"]
    
    df_salarios["INSS (R$)"] = df_salarios["Salário Base (R$)"] * impostos["inss"]
    df_salarios["FGTS (R$)"] = df_salarios["Salário Base (R$)"] * impostos["fgts"]
    df_salarios["IRPF (R$)"] = df_salarios["Salário Base (R$)"] * impostos["IRPF"]
    df_salarios["Provisão 13º (R$)"] = df_salarios["Salário Base (R$)"] * impostos["decimo"]
    
    # Total de encargos por funcionário
    df_salarios["Total Encargos (R$)"] = (
        df_salarios["INSS (R$)"] + 
        df_salarios["FGTS (R$)"] + 
        df_salarios["IRPF (R$)"] + 
        df_salarios["Provisão 13º (R$)"]
    )
    
    # Calcular custo total por funcionário
    df_salarios["Custo por Funcionário (R$)"] = df_salarios["Salário Base (R$)"] + df_salarios["Total Encargos (R$)"]
    df_salarios["Custo Total Mensal (R$)"] = df_salarios["Custo por Funcionário (R$)"] * df_salarios["Quantidade"]
    
    # Métricas principais
    total_salarios_base = (df_salarios["Salário Base (R$)"] * df_salarios["Quantidade"]).sum()
    total_encargos = (df_salarios["Total Encargos (R$)"] * df_salarios["Quantidade"]).sum()
    total_geral = df_salarios["Custo Total Mensal (R$)"].sum()
    total_funcionarios = df_salarios["Quantidade"].sum()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Total da Folha Salarial",
            f"R$ {total_geral:,.2f}",
            delta=f"Encargos: {(total_encargos/total_salarios_base*100):.1f}%"
        )
    with col2:
        st.metric(
            "Total de Funcionários",
            f"{total_funcionarios}",
            delta=f"Média R$ {(total_geral/total_funcionarios):,.2f}/func."
        )
    with col3:
        st.metric(
            "Maior Custo por Cargo",
            f"R$ {df_salarios['Custo Total Mensal (R$)'].max():,.2f}",
            delta=f"Cargo: {df_salarios.loc[df_salarios['Custo Total Mensal (R$)'].idxmax(), 'Cargo']}"
        )
    
    # Visualizações
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.dataframe(
            df_salarios.style.format({
                'Salário Base (R$)': 'R${:,.2f}',
                'INSS (R$)': 'R${:,.2f}',
                'FGTS (R$)': 'R${:,.2f}',
                'IRPF (R$)': 'R${:,.2f}',
                'Provisão 13º (R$)': 'R${:,.2f}',
                'Total Encargos (R$)': 'R${:,.2f}',
                'Custo por Funcionário (R$)': 'R${:,.2f}',
                'Custo Total Mensal (R$)': 'R${:,.2f}'
            }).background_gradient(
                subset=['Custo Total Mensal (R$)'],
                cmap='YlOrRd'
            ),
            use_container_width=True
        )
    
    with col2:
        # Gráfico de pizza com custos totais
        fig = px.pie(
            df_salarios,
            values='Custo Total Mensal (R$)',
            names='Cargo',
            title='Distribuição dos Custos com Salários',
            hole=0.4
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Gráfico de barras comparativo
    st.plotly_chart(
        px.bar(
            df_salarios,
            x='Cargo',
            y=['Salário Base (R$)', 'Total Encargos (R$)'],
            title='Comparativo: Salário Base vs Encargos por Cargo',
            barmode='group'
        ).update_layout(height=400),
        use_container_width=True
    )

def create_salary_df(data):
    df_salarios = pd.DataFrame({
        "Cargo": data["salarios"]["cargos"],
        "Salário Base (R$)": data["salarios"]["valores"],
        "Quantidade": data["salarios"]["quantidade"]
    })
    
    impostos = data["salarios"]["impostos"]
    
    # Calculando cada encargo separadamente usando .get()
    df_salarios["INSS (R$)"] = df_salarios["Salário Base (R$)"] * impostos.get("inss", 0)
    df_salarios["FGTS (R$)"] = df_salarios["Salário Base (R$)"] * impostos.get("fgts", 0)
    df_salarios["Acidente (R$)"] = df_salarios["Salário Base (R$)"] * impostos.get("acidente", 0)
    df_salarios["Educação (R$)"] = df_salarios["Salário Base (R$)"] * impostos.get("educacao", 0)
    df_salarios["DSR (R$)"] = df_salarios["Salário Base (R$)"] * impostos.get("dsr", 0)
    df_salarios["13º (R$)"] = df_salarios["Salário Base (R$)"] * impostos.get("decimo", 0)
    df_salarios["Sistema S (R$)"] = df_salarios["Salário Base (R$)"] * impostos.get("sistema_s", 0)
    df_salarios["Férias (R$)"] = df_salarios["Salário Base (R$)"] * impostos.get("ferias", 0)
    
    # Total de encargos por funcionário
    df_salarios["Total Encargos (R$)"] = (
        df_salarios["INSS (R$)"] + 
        df_salarios["FGTS (R$)"] + 
        df_salarios["Acidente (R$)"] +
        df_salarios["Educação (R$)"] +
        df_salarios["DSR (R$)"] +
        df_salarios["13º (R$)"] +
        df_salarios["Sistema S (R$)"] +
        df_salarios["Férias (R$)"]
    )
    
    df_salarios["Custo por Funcionário (R$)"] = df_salarios["Salário Base (R$)"] + df_salarios["Total Encargos (R$)"]
    df_salarios["Custo Total Mensal (R$)"] = df_salarios["Custo por Funcionário (R$)"] * df_salarios["Quantidade"]
    
    return df_salarios
