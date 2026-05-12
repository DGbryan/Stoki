import pandas as pd
from sqlalchemy.orm import Session
from app.database.models import Item
import io

EXPECTED_COLUMNS = ['Código', 'Descrição', 'Lote', 'Qtd(m2)', 'Local Esperado', 'Depósito']

def import_excel_to_db(db: Session, excel_file: bytes):
    """
    Lê o arquivo Excel de bytes, valida as colunas e importa para a tabela de items.
    """
    df = pd.read_excel(io.BytesIO(excel_file))
    
    # Valida as colunas
    missing_cols = [col for col in EXPECTED_COLUMNS if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Faltam colunas no Excel: {', '.join(missing_cols)}")
    
    # Processa os itens
    items_added = 0
    items_updated = 0
    
    for _, row in df.iterrows():
        item_code = str(row['Código']).strip()
        if not item_code or item_code == 'nan':
            continue
            
        existing_item = db.query(Item).filter(Item.item_code == item_code).first()
        
        if existing_item:
            # Update
            existing_item.description = str(row['Descrição'])
            existing_item.lot = str(row['Lote'])
            existing_item.quantity_m2 = float(row['Qtd(m2)'])
            existing_item.expected_location = str(row['Local Esperado']).strip()
            existing_item.sap_warehouse = str(row['Depósito'])
            items_updated += 1
        else:
            # Insert
            new_item = Item(
                item_code=item_code,
                description=str(row['Descrição']),
                lot=str(row['Lote']),
                quantity_m2=float(row['Qtd(m2)']),
                expected_location=str(row['Local Esperado']).strip(),
                sap_warehouse=str(row['Depósito'])
            )
            db.add(new_item)
            items_added += 1
            
    db.commit()
    return items_added, items_updated

def get_template_excel() -> bytes:
    """Retorna bytes de um Excel vazio com as colunas esperadas para o usuário usar como base."""
    df = pd.DataFrame(columns=EXPECTED_COLUMNS)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name="Template Importacao")
    return output.getvalue()
