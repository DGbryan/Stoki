import streamlit as st
from app.database.db import get_db
from app.services.auth_service import authenticate_operator, register_operator, reset_password
import os

st.set_page_config(page_title="Login", page_icon="🔐")

st.logo(os.path.join(os.path.dirname(os.path.dirname(__file__)), "logo.png"))
st.markdown("""
    <style>
        [data-testid="stSidebarHeader"] img,
        [data-testid="stLogo"],
        [data-testid="stLogo"] img {
            height: 6rem !important;
            max-height: 6rem !important;
            width: auto !important;
        }
    </style>
""", unsafe_allow_html=True)

if 'login_view' not in st.session_state:
    st.session_state['login_view'] = 'login'

db_generator = get_db()
db = next(db_generator)

try:
    if st.session_state['login_view'] == 'login':
        st.title("Login - Unilux S.A")
        email = st.text_input("E-mail do Usuário", placeholder="exemplo@unilux.com.br")
        password = st.text_input("Senha", type="password", placeholder="Sua senha")
        
        if st.button("Entrar", type="primary", use_container_width=True):
            if email and password:
                operator = authenticate_operator(db, email, password)
                if operator:
                    st.session_state['operator_id'] = operator.id
                    st.session_state['operator_name'] = operator.name
                    st.success(f"Login realizado com sucesso! Bem-vindo(a), {operator.name}.")
                    st.switch_page("main.py")
                else:
                    st.error("E-mail ou senha inválidos. Verifique e tente novamente.")
            else:
                st.warning("Por favor, preencha o e-mail e a senha.")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Esqueci a senha", use_container_width=True):
                st.session_state['login_view'] = 'forgot'
                st.rerun()
        with col2:
            if st.button("Cadastrar Usuário", use_container_width=True):
                st.session_state['login_view'] = 'register'
                st.rerun()

    elif st.session_state['login_view'] == 'register':
        st.title("Cadastrar Novo Usuário")
        reg_name = st.text_input("Nome Completo", placeholder="Seu nome")
        reg_email = st.text_input("E-mail", placeholder="exemplo@unilux.com.br")
        reg_password = st.text_input("Senha", type="password", placeholder="Crie uma senha")
        
        if st.button("Salvar Cadastro", type="primary", use_container_width=True):
            if reg_name and reg_email and reg_password:
                try:
                    register_operator(db, reg_name, reg_email, reg_password)
                    st.success("Cadastro realizado com sucesso! Você já pode fazer o login.")
                    st.session_state['login_view'] = 'login'
                    st.rerun()
                except Exception as e:
                    st.error("Erro ao cadastrar. O e-mail já pode estar em uso.")
            else:
                st.warning("Preencha todos os campos para cadastrar.")
        
        if st.button("Voltar ao Login", use_container_width=True):
            st.session_state['login_view'] = 'login'
            st.rerun()

    elif st.session_state['login_view'] == 'forgot':
        st.title("Recuperar Senha")
        forgot_email = st.text_input("Informe seu E-mail", placeholder="exemplo@unilux.com.br")
        
        if st.button("Resetar Senha", type="primary", use_container_width=True):
            if forgot_email:
                success = reset_password(db, forgot_email)
                if success:
                    st.success("Senha redefinida com sucesso! Sua senha temporária é: 1234")
                else:
                    st.error("E-mail não encontrado na base de dados.")
            else:
                st.warning("Por favor, informe o seu e-mail.")
                
        if st.button("Voltar ao Login", use_container_width=True):
            st.session_state['login_view'] = 'login'
            st.rerun()

finally:
    db.close()
