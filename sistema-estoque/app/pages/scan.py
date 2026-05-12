import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import streamlit as st
from app.database.db import get_db
from app.services.scan_service import process_scan
import urllib.parse
import cv2
import numpy as np

import os

st.set_page_config(page_title="Escanear Estoque", page_icon="📷")

st.logo(os.path.join(os.path.dirname(os.path.dirname(__file__)), "logo.png"))
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

if not st.session_state.get('operator_id'):
    st.warning("Você precisa estar logado para acessar esta página.")
    st.stop()

st.title("Escanear Rolos e Prateleiras")

# --- SEÇÃO DE CÂMERA ---
st.markdown("### Usar Câmera (Leitor de QR Code)")
st.info("Para testar pelo celular, você pode precisar acessar o sistema usando HTTPS ou configurar o navegador para permitir câmera em sites HTTP (ex: acessar chrome://flags/#unsafely-treat-insecure-origin-as-secure).")

img_file_buffer = st.camera_input("Tire uma foto do QR Code")

# Inicializa o session_state para os códigos se não existirem
if 'scanned_shelf_code' not in st.session_state:
    st.session_state.scanned_shelf_code = ""
if 'scanned_item_code' not in st.session_state:
    st.session_state.scanned_item_code = ""

if img_file_buffer is not None:
    # Converter a imagem para o formato do OpenCV
    bytes_data = img_file_buffer.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
    
    detector = cv2.QRCodeDetector()
    data, bbox, straight_qrcode = detector.detectAndDecode(cv2_img)
    
    if data:
        st.success(f"QR Code lido com sucesso: **{data}**")
        # Logica simples: se começa com TC. ou ROLO, assumimos que é o rolo (Item). Senão, é a prateleira (Location).
        if "TC." in data or data.startswith("TC") or "ROLO" in data:
            st.session_state.scanned_item_code = data
        else:
            st.session_state.scanned_shelf_code = data
    else:
        st.error("Nenhum QR Code encontrado na imagem. Tente chegar mais perto ou focar melhor.")

st.markdown("---")
st.markdown("### Dados Lidos")
shelf_code = st.text_input("QR Code da Prateleira", value=st.session_state.scanned_shelf_code, placeholder="Ex: TEC01.A")
item_code = st.text_input("QR Code do Rolo", value=st.session_state.scanned_item_code, placeholder="Ex: TC.000.296")

if st.button("Validar"):
    if shelf_code and item_code:
        db_generator = get_db()
        db = next(db_generator)
        try:
            status, expected_loc = process_scan(
                db, 
                st.session_state['operator_id'], 
                item_code, 
                shelf_code
            )
            
            # Limpar o session state para o proximo scan
            st.session_state.scanned_shelf_code = ""
            st.session_state.scanned_item_code = ""
            
            # Pass results via session state to the validation page
            st.session_state["val_item_code"] = item_code
            st.session_state["val_scanned_loc"] = shelf_code
            st.session_state["val_expected_loc"] = str(expected_loc)
            st.session_state["val_status"] = status
            
            st.switch_page("pages/Validation.py")
            
        finally:
            db.close()
    else:
        st.warning("Por favor, preencha (ou escaneie) os dois códigos.")


