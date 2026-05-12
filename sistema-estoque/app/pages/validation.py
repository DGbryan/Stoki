import streamlit as st

import os

st.set_page_config(page_title="Resultado", page_icon="📝")

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

if not st.session_state.get('operator_id'):
    st.warning("Você precisa estar logado para acessar esta página.")
    st.stop()

st.title("Resultado da Validação")

# Recupera parâmetros via session state
if "val_status" not in st.session_state:
    st.info("Nenhuma validação recente encontrada.")
    if st.button("Voltar ao Scanner"):
        st.switch_page("pages/scan.py")
    st.stop()

status = st.session_state.get("val_status")
item_code = st.session_state.get("val_item_code")
scanned_loc = st.session_state.get("val_scanned_loc")
expected_loc = st.session_state.get("val_expected_loc")

if status == "CORRETO":
    st.success("✅ CORRETO")
    st.markdown(f"**Item:** {item_code}")
    st.markdown(f"**Local escaneado:** {scanned_loc}")
    st.markdown(f"**Local esperado:** {expected_loc}")
elif status == "DIVERGENTE":
    st.error("❌ DIVERGENTE")
    st.markdown(f"**Item:** {item_code}")
    st.markdown(f"**Local escaneado:** {scanned_loc}")
    st.markdown(f"**Local esperado:** {expected_loc}  ← *deveria estar aqui*")
else:
    st.warning("⚠️ ITEM NÃO ENCONTRADO NA BASE")
    st.markdown(f"**Item:** {item_code}")
    st.markdown(f"**Local escaneado:** {scanned_loc}")

st.divider()

if st.button("Escanear Novo Item", type="primary"):
    # Limpa dados da validação
    for k in ["val_status", "val_item_code", "val_scanned_loc", "val_expected_loc"]:
        if k in st.session_state:
            del st.session_state[k]
    st.switch_page("pages/scan.py")
