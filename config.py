import streamlit as st

def setup_page():
    st.set_page_config(
        page_title="Orçamento Escolar MDC",
        page_icon="🏫",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def setup_style():
    st.markdown("""
        <style>
        /* Estilo geral da página */
        .main {
            padding: 2rem 3rem;
            max-width: 1200px;
            margin: 0 auto;
        }
        
        /* Cabeçalho */
        h1 {
            color: #2c3e50;
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 2rem;
            text-align: center;
            padding: 1rem;
            border-bottom: 3px solid #4c78a8;
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: #f8f9fa;
            padding: 0.5rem;
            border-radius: 10px;
        }
        
        .stTabs [data-baseweb="tab"] {
            padding: 12px 24px;
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: #4c78a8;
            border-radius: 8px;
            color: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        /* Cards/Métricas */
        [data-testid="stMetricValue"] {
            font-size: 1.8rem !important;
            font-weight: 700 !important;
            color: #2c3e50 !important;
        }
        
        [data-testid="stMetricDelta"] {
            font-size: 1rem !important;
            color: #666 !important;
        }
        
        /* DataFrames */
        .dataframe {
            border-radius: 8px !important;
            overflow: hidden !important;
            border: 1px solid #eee !important;
        }
        
        /* Gráficos */
        [data-testid="stPlotlyChart"] > div {
            border-radius: 10px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.05);
            padding: 1rem;
            background: white;
        }
        
        /* Botões */
        .stDownloadButton button {
            background-color: #4c78a8 !important;
            color: white !important;
            border-radius: 8px !important;
            padding: 0.5rem 1rem !important;
            font-weight: 600 !important;
            border: none !important;
            transition: all 0.3s ease !important;
        }
        
        .stDownloadButton button:hover {
            background-color: #3a5d82 !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
        }
        
        /* Footer */
        footer {
            margin-top: 3rem;
            padding-top: 1rem;
            border-top: 1px solid #eee;
            text-align: center;
            color: #666;
        }
        
        /* Responsividade */
        @media (max-width: 768px) {
            .main {
                padding: 1rem;
            }
            
            h1 {
                font-size: 2rem;
            }
            
            [data-testid="stMetricValue"] {
                font-size: 1.5rem !important;
            }
        }
        </style>
    """, unsafe_allow_html=True)

def show_header():
    st.markdown("""
        <div style='text-align: center; padding: 2rem 0;'>
            <h1>
                <span style='font-size: 3rem;'>🏫</span><br>
                Orçamento Escolar MDC
            </h1>
            <p style='color: #666; font-size: 1.1rem; margin-top: -1rem;'>
                Sistema de Gestão e Análise de Custos Escolares
            </p>
        </div>
    """, unsafe_allow_html=True) 