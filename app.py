import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import io

# Configuração da página
st.set_page_config(
    page_title="Orçamento Escolar MDC",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo CSS personalizado
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .st-emotion-cache-1y4p8pa {
        padding: 1rem 1rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #4c78a8;
    }
    </style>
""", unsafe_allow_html=True)

# Título principal com ícone e cor
st.markdown("""
    <h1 style='text-align: center; color: #4c78a8;'>
        🏫 Orçamento Escolar MDC
    </h1>
""", unsafe_allow_html=True)

# Dados iniciais
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

# Criar DataFrame e cálculos
def process_data(data):
    df = pd.DataFrame(data)
    df["Valor Unitário Final (R$)"] = df["Custo Unitário (R$)"] * (1 + df["Margem de Lucro (%)"] / 100)
    df["Custo Mensal Total (R$)"] = df["Valor Unitário Final (R$)"] * df["Quantidade Mensal"]
    return df

# Layout principal
def main():
    data = get_initial_data()
    df = process_data(data)

    # Criar abas
    tab1, tab2, tab3 = st.tabs([
        "📊 Visão Geral",
        "📈 Análise Detalhada",
        "⚙️ Configurações"
    ])

    with tab1:
        # Métricas principais
        col1, col2, col3 = st.columns(3)
        total = df['Custo Mensal Total (R$)'].sum()
        media = df['Custo Mensal Total (R$)'].mean()
        qtd_items = len(df)

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

        # Gráfico principal
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

    with tab2:
        col1, col2 = st.columns([2, 1])
        
        with col1:
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

        with col2:
            st.subheader("Distribuição dos Custos")
            fig_pie = px.pie(
                df,
                values='Custo Mensal Total (R$)',
                names='Descrição do Item',
                hole=0.4
            )
            st.plotly_chart(fig_pie, use_container_width=True)

            # Análise de custos
            mais_custoso = df.loc[df['Custo Mensal Total (R$)'].idxmax()]
            st.info(f"""
                💡 **Análise Rápida**
                - Item mais custoso: {mais_custoso['Descrição do Item']}
                - Custo: R$ {mais_custoso['Custo Mensal Total (R$)']:,.2f}
                - Representa {(mais_custoso['Custo Mensal Total (R$)']/total*100):.1f}% do total
            """)

    with tab3:
        st.subheader("Exportar Dados")
        col1, col2 = st.columns(2)
        
        with col1:
            # Botão de download CSV
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f'orcamento_escolar_{datetime.now().strftime("%Y%m%d")}.csv',
                mime='text/csv',
                help="Clique para baixar os dados em formato CSV"
            )
        
        with col2:
            # Botão de download Excel
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Orçamento')
            
            excel_data = output.getvalue()
            st.download_button(
                label="📥 Download Excel",
                data=excel_data,
                file_name=f'orcamento_escolar_{datetime.now().strftime("%Y%m%d")}.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                help="Clique para baixar os dados em formato Excel"
            )

    # Adicionar footer
    st.markdown("""
        ---
        <p style='text-align: center; color: #888888;'>
            Desenvolvido por Sond | Última atualização: {}
        </p>
    """.format(datetime.now().strftime("%d/%m/%Y")), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
