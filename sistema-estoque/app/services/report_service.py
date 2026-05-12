from sqlalchemy.orm import Session
import pandas as pd
from app.database.models import Scan, Divergence, Operator
import io

def get_scans_dataframe(db: Session):
    query = db.query(
        Scan.id, 
        Scan.item_code, 
        Scan.scanned_location, 
        Scan.expected_location, 
        Scan.status, 
        Scan.created_at,
        Operator.name.label("operator_name")
    ).join(Operator, Scan.operator_id == Operator.id)
    
    df = pd.read_sql(query.statement, query.session.bind)
    return df

def get_divergences_dataframe(db: Session):
    query = db.query(
        Divergence.id,
        Divergence.item_code,
        Divergence.expected_location,
        Divergence.found_location,
        Divergence.resolved,
        Divergence.resolved_at
    )
    
    df = pd.read_sql(query.statement, query.session.bind)
    return df

def generate_excel_report(db: Session) -> bytes:
    """Gera um arquivo Excel contendo as listagens de escaneamentos e divergências"""
    scans_df = get_scans_dataframe(db)
    divergences_df = get_divergences_dataframe(db)
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        scans_df.to_excel(writer, sheet_name='Escaneamentos', index=False)
        divergences_df.to_excel(writer, sheet_name='Divergencias', index=False)
    
    return output.getvalue()
