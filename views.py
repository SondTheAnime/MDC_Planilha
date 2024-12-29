import streamlit as st
import plotly.express as px

def show_metrics(df):
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

def show_detailed_analysis(df):
    col1, col2 = st.columns([2, 1])
    
    with col1:
        show_detailed_table(df)
    
    with col2:
        show_pie_chart(df)
        show_cost_analysis(df)

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