import sys
sys.path.append('.')
from app.database.db import SessionLocal
from app.database.models import Item, Location
import qrcode
import os

db = SessionLocal()

# Add test items and locations
test_data = [
    # Correct pairs
    {"item_code": "ROLO-100", "loc_code": "PRAT-A1", "desc": "Tecido Azul", "expected": "PRAT-A1"},
    {"item_code": "ROLO-101", "loc_code": "PRAT-A2", "desc": "Tecido Verde", "expected": "PRAT-A2"},
    # Divergent pairs
    {"item_code": "ROLO-200", "loc_code": "PRAT-B1", "desc": "Tecido Vermelho", "expected": "PRAT-B1"},
    {"item_code": "ROLO-201", "loc_code": "PRAT-B2", "desc": "Tecido Amarelo", "expected": "PRAT-B2"},
]

# Extra locations for divergence
extra_locs = ["PRAT-X9", "PRAT-Z1"]

for data in test_data:
    item = db.query(Item).filter(Item.item_code == data["item_code"]).first()
    if not item:
        item = Item(item_code=data["item_code"], expected_location=data["expected"], description=data["desc"])
        db.add(item)
    else:
        item.expected_location = data["expected"]
    
    loc = db.query(Location).filter(Location.location_code == data["loc_code"]).first()
    if not loc:
        loc = Location(location_code=data["loc_code"])
        db.add(loc)

for loc_code in extra_locs:
    loc = db.query(Location).filter(Location.location_code == loc_code).first()
    if not loc:
        loc = Location(location_code=loc_code)
        db.add(loc)

db.commit()
db.close()

# Generate QR Codes
qr_dir = r"C:\Users\Bryan\.gemini\antigravity\brain\60e4d28d-8c8b-4dda-85a6-1bed74f52b0b\qr_testes"
os.makedirs(qr_dir, exist_ok=True)

qrs_to_gen = [
    ("ROLO-100", "qr_rolo_100_correto.png"),
    ("PRAT-A1", "qr_prat_A1_correto.png"),
    
    ("ROLO-101", "qr_rolo_101_correto.png"),
    ("PRAT-A2", "qr_prat_A2_correto.png"),
    
    ("ROLO-200", "qr_rolo_200_divergente.png"),
    ("PRAT-X9", "qr_prat_X9_divergente.png"),
    
    ("ROLO-201", "qr_rolo_201_divergente.png"),
    ("PRAT-Z1", "qr_prat_Z1_divergente.png"),
]

for text, filename in qrs_to_gen:
    img = qrcode.make(text)
    img.save(os.path.join(qr_dir, filename))

print("QR codes generated.")
