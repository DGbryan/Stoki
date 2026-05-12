from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database.db import Base, engine

class Operator(Base):
    __tablename__ = "operators"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    badge = Column(String, unique=True, index=True, nullable=True)
    email = Column(String, unique=True, index=True, nullable=True)
    password = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())

class Item(Base):
    __tablename__ = "items"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    item_code = Column(String, unique=True, index=True)
    description = Column(String)
    lot = Column(String)
    quantity_m2 = Column(Float)
    expected_location = Column(String)
    sap_warehouse = Column(String)
    created_at = Column(DateTime, default=func.now())

class Location(Base):
    __tablename__ = "locations"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    location_code = Column(String, unique=True, index=True)
    sector = Column(String)
    shelf = Column(String)
    level = Column(String)
    qr_data = Column(String)

class Scan(Base):
    __tablename__ = "scans"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    item_code = Column(String, index=True)
    scanned_location = Column(String)
    expected_location = Column(String)
    operator_id = Column(Integer, ForeignKey("operators.id"))
    status = Column(String) # CORRETO, DIVERGENTE, NAO_ENCONTRADO
    created_at = Column(DateTime, default=func.now())
    sent_to_sap = Column(Boolean, default=False)
    sap_response = Column(String, nullable=True)

class Divergence(Base):
    __tablename__ = "divergences"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    scan_id = Column(Integer, ForeignKey("scans.id"))
    item_code = Column(String)
    expected_location = Column(String)
    found_location = Column(String)
    resolved = Column(Boolean, default=False)
    resolved_at = Column(DateTime, nullable=True)
    resolved_by = Column(Integer, ForeignKey("operators.id"), nullable=True)

# Create tables if they do not exist
Base.metadata.create_all(bind=engine)
