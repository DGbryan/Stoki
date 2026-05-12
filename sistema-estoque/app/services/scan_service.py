from sqlalchemy.orm import Session
from app.database.models import Operator, Item, Location, Scan, Divergence

def get_operator_by_badge(db: Session, badge: str) -> Operator:
    return db.query(Operator).filter(Operator.badge == badge).first()

def get_item_by_code(db: Session, item_code: str) -> Item:
    return db.query(Item).filter(Item.item_code == item_code).first()

def get_location_by_code(db: Session, location_code: str) -> Location:
    return db.query(Location).filter(Location.location_code == location_code).first()

def process_scan(db: Session, operator_id: int, item_code: str, scanned_location_code: str):
    """
    Registra um scan e compara o local esperado com o real.
    Retorna o status e uma mensagem descritiva.
    """
    item = get_item_by_code(db, item_code)
    
    if not item:
        # Registra scan mesmo assim para histórico, mas o item não foi encontrado na base
        new_scan = Scan(
            item_code=item_code,
            scanned_location=scanned_location_code,
            expected_location="N/A",
            operator_id=operator_id,
            status="NAO_ENCONTRADO"
        )
        db.add(new_scan)
        db.commit()
        return "NAO_ENCONTRADO", None

    expected_loc = item.expected_location
    
    if expected_loc == scanned_location_code:
        status = "CORRETO"
    else:
        status = "DIVERGENTE"
        
    new_scan = Scan(
        item_code=item_code,
        scanned_location=scanned_location_code,
        expected_location=expected_loc,
        operator_id=operator_id,
        status=status
    )
    db.add(new_scan)
    db.commit()
    db.refresh(new_scan)
    
    if status == "DIVERGENTE":
        new_divergence = Divergence(
            scan_id=new_scan.id,
            item_code=item_code,
            expected_location=expected_loc,
            found_location=scanned_location_code,
            resolved=False
        )
        db.add(new_divergence)
        db.commit()
        
    return status, expected_loc
