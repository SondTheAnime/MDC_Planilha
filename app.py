import streamlit as st
from datetime import datetime
from config import setup_page, setup_style, show_header
from data import get_initial_data, process_data
from views import show_metrics, show_bar_chart, show_detailed_analysis
from export import show_export_options

def main():
    setup_page()
    setup_style()
    show_header()

    data = get_initial_data()
    df = process_data(data)

    tab1, tab2, tab3 = st.tabs([
        "📊 Visão Geral",
        "📈 Análise Detalhada",
        "⚙️ Configurações"
    ])

    with tab1:
        show_metrics(df)
        show_bar_chart(df)

    with tab2:
        show_detailed_analysis(df)

    with tab3:
        show_export_options(df)

    # Footer
    st.markdown("""
        ---
        <p style='text-align: center; color: #888888;'>
            Desenvolvido por Sond | Última atualização: {}
        </p>
    """.format(datetime.now().strftime("%d/%m/%Y")), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
