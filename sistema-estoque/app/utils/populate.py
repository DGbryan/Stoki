import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database.db import SessionLocal, Base, engine
from app.database.models import Operator, Item, Location

def populate_db():
    print("Criando tabelas...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Verifica se já tem dados
        if db.query(Operator).first():
            print("Banco já populado.")
            return

        # 1. Inserir Operador
        print("Inserindo Operador de teste...")
        op1 = Operator(name="João Silva", badge="1234")
        op2 = Operator(name="Maria Souza", badge="5678")
        db.add_all([op1, op2])
        
        # 2. Inserir Locais (Prateleiras)
        print("Inserindo Prateleiras de teste...")
        loc1 = Location(location_code="TEC01.A", sector="TEC01", shelf="A", level="01")
        loc2 = Location(location_code="B01", sector="B", shelf="01", level="01")
        loc3 = Location(location_code="B02", sector="B", shelf="02", level="01")
        db.add_all([loc1, loc2, loc3])
        
        # 3. Inserir Rolos de Tecido (Items)
        print("Inserindo Rolos de teste...")
        item1 = Item(
            item_code="TC.000.296",
            description="Tecido Screen Blackout",
            lot="TEC01.A.N02",
            quantity_m2=50.0,
            expected_location="TEC01.A",
            sap_warehouse="01"
        )
        item2 = Item(
            item_code="TC.000.290",
            description="Tecido Essentials Grey",
            lot="B02.N01",
            quantity_m2=35.5,
            expected_location="TEC01.A", # intencionalmente errado pro teste
            sap_warehouse="01"
        )
        db.add_all([item1, item2])
        
        db.commit()
        print("Banco de dados populado com sucesso!")
        
    except Exception as e:
        print(f"Erro ao popular banco: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    populate_db()
