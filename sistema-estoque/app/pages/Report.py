import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import streamlit as st
from app.database.db import get_db
from app.services.report_service import get_scans_dataframe, get_divergences_dataframe, generate_excel_report

import os

st.set_page_config(page_title="Relatórios", page_icon="📊", layout="wide")

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

st.title("Relatórios Operacionais")

db_generator = get_db()
db = next(db_generator)

try:
    st.subheader("Histórico de Escaneamentos")
    scans_df = get_scans_dataframe(db)
    
    if scans_df.empty:
        st.info("Nenhum escaneamento registrado.")
    else:
        st.dataframe(scans_df, use_container_width=True)

    st.divider()
    
    st.subheader("Divergências")
    div_df = get_divergences_dataframe(db)
    if div_df.empty:
        st.info("Nenhuma divergência registrada.")
    else:
        st.dataframe(div_df, use_container_width=True)

    st.divider()
    
    # Download Excel
    st.subheader("Exportação")
    excel_data = generate_excel_report(db)
    
    st.download_button(
        label="📥 Exportar Excel",
        data=excel_data,
        file_name="relatorio_estoque.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

finally:
    db.close()


