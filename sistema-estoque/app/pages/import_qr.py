import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
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
            height: 4.5rem !important;
            max-height: 4.5rem !important;
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

    st.divider()

    st.header("3. QR Codes de Teste (Prontos para Uso)")
    st.markdown("Use os QR Codes abaixo para testar o sistema no seu celular agora mesmo.")
    
    import qrcode
    
    def generate_qr_image(data):
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        return img

    test_codes = [
        {"type": "Rolo (Correto)", "code": "TC.000.296"},
        {"type": "Rolo (Divergente)", "code": "ROLO-100"},
        {"type": "Prateleira 1", "code": "TEC01.A"},
        {"type": "Prateleira 2", "code": "TEC01.B"}
    ]
    
    cols = st.columns(4)
    for i, test_data in enumerate(test_codes):
        with cols[i]:
            st.markdown(f"**{test_data['type']}**")
            st.caption(f"`{test_data['code']}`")
            st.image(generate_qr_image(test_data["code"]).get_image(), use_container_width=True)

finally:
    db.close()



