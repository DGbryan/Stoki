import streamlit as st
import os
from app.database.db import get_db
from app.database.models import Item
from app.utils.importer import import_excel_to_db, get_template_excel
from app.utils.qr_generator import create_qr_codes_zip

st.set_page_config(page_title="Importação e QR", page_icon="🖨️", layout="wide")

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

st.title("Importação de Dados e Geração de QR Codes")

db_generator = get_db()
db = next(db_generator)

try:
    st.header("1. Importar Excel com Itens")
    st.markdown("Baixe a planilha modelo, preencha os dados e faça o upload para popular a base de dados em massa.")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.download_button(
            label="Baixar Planilha Modelo",
            data=get_template_excel(),
            file_name="template_itens.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    with col2:
        uploaded_file = st.file_uploader("Upload da Planilha Preenchida", type=["xlsx", "xls"])
        
        if uploaded_file is not None:
            if st.button("Processar Planilha"):
                try:
                    bytes_data = uploaded_file.getvalue()
                    added, updated = import_excel_to_db(db, bytes_data)
                    st.success(f"Planilha importada com sucesso! {added} itens inseridos e {updated} itens atualizados.")
                except Exception as e:
                    st.error(f"Erro ao processar planilha: {e}")

    st.divider()

    st.header("2. Geração de Etiquetas (QR Codes)")
    total_items = db.query(Item).count()
    
    st.info(f"O banco de dados possui **{total_items}** itens cadastrados.")
    
    if total_items > 0:
        if st.button("Gerar QR Codes para Impressão"):
            with st.spinner("Gerando imagens, por favor aguarde..."):
                items = db.query(Item).all()
                base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                qrcodes_dir = os.path.join(base_dir, "data", "qrcodes")
                
                try:
                    zip_bytes = create_qr_codes_zip(items, qrcodes_dir)
                    
                    st.success("QR Codes gerados com sucesso!")
                    st.download_button(
                        label="📦 Baixar Arquivo ZIP com Etiquetas",
                        data=zip_bytes,
                        file_name="qrcodes_etiquetas.zip",
                        mime="application/zip",
                        type="primary"
                    )
                except Exception as e:
                    st.error(f"Ocorreu um erro ao gerar as imagens: {e}")

finally:
    db.close()
