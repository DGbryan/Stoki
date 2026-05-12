import streamlit as st
import os
import sys

# Adiciona o diretório raiz ao path para os imports funcionarem
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(
    page_title="Sistema de Conferência de Estoque",
    page_icon="📦",
    layout="centered"
)

st.logo(os.path.join(os.path.dirname(__file__), "logo.png"))
st.markdown("""
    <style>
        [data-testid="stSidebarHeader"] img,
        [data-testid="stLogo"],
        [data-testid="stLogo"] img {
            height: 4.5rem !important;
            max-height: 4.5rem !important;
            width: auto !important;
        }
    </style>
""", unsafe_allow_html=True)

# Inicializa o session state se não existir
if 'operator_id' not in st.session_state:
    st.session_state['operator_id'] = None
if 'operator_name' not in st.session_state:
    st.session_state['operator_name'] = None

def main():
    if not st.session_state['operator_id']:
        st.switch_page("pages/login.py")
    else:
        st.title(f"Bem-vindo(a), {st.session_state['operator_name']}")
        st.markdown("Selecione uma opção no menu lateral para começar.")

if __name__ == "__main__":
    main()

