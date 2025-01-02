import streamlit as st
from datetime import datetime
from config import setup_page, setup_style, show_header
from data import get_initial_data, process_data
from views import show_metrics, show_bar_chart, show_detailed_analysis, show_salary_analysis
from export import show_export_options

def main():
    setup_page()
    setup_style()
    show_header()

    data = get_initial_data()
    df = process_data(data)

    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Visão Geral",
        "📈 Análise Detalhada",
        "💰 Salários",
        "⚙️ Configurações"
    ])

    with tab1:
        show_metrics(df, data)
        show_bar_chart(df)

    with tab2:
        show_detailed_analysis(df, data)
        
    with tab3:
        show_salary_analysis(df, data)

    with tab4:
        show_export_options(df, data)

    # Footer
    st.markdown("""
        <footer>
            <p>
                <span style='font-size: 1.2rem;'>🚀</span><br>
                Desenvolvido por Sond<br>
                <small>Última atualização: {}</small>
            </p>
        </footer>
    """.format(datetime.now().strftime("%d/%m/%Y")), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
