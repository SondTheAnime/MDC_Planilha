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

def show_header():
    st.markdown("""
        <h1 style='text-align: center; color: #4c78a8;'>
            🏫 Orçamento Escolar MDC
        </h1>
    """, unsafe_allow_html=True) 