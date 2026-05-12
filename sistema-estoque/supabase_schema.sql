-- Create Operators Table
CREATE TABLE IF NOT EXISTS operators (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    badge VARCHAR UNIQUE,
    email VARCHAR UNIQUE,
    password VARCHAR,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Items Table
CREATE TABLE IF NOT EXISTS items (
    id SERIAL PRIMARY KEY,
    item_code VARCHAR UNIQUE,
    description VARCHAR,
    lot VARCHAR,
    quantity_m2 FLOAT,
    expected_location VARCHAR,
    sap_warehouse VARCHAR,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Locations Table
CREATE TABLE IF NOT EXISTS locations (
    id SERIAL PRIMARY KEY,
    location_code VARCHAR UNIQUE,
    sector VARCHAR,
    shelf VARCHAR,
    level VARCHAR,
    qr_data VARCHAR
);

-- Create Scans Table
CREATE TABLE IF NOT EXISTS scans (
    id SERIAL PRIMARY KEY,
    item_code VARCHAR,
    scanned_location VARCHAR,
    expected_location VARCHAR,
    operator_id INTEGER REFERENCES operators(id) ON DELETE SET NULL,
    status VARCHAR,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sent_to_sap BOOLEAN DEFAULT FALSE,
    sap_response VARCHAR
);

-- Create Divergences Table
CREATE TABLE IF NOT EXISTS divergences (
    id SERIAL PRIMARY KEY,
    scan_id INTEGER REFERENCES scans(id) ON DELETE CASCADE,
    item_code VARCHAR,
    expected_location VARCHAR,
    found_location VARCHAR,
    resolved BOOLEAN DEFAULT FALSE,
    resolved_at TIMESTAMP,
    resolved_by INTEGER REFERENCES operators(id) ON DELETE SET NULL
);

-- Add recommended indexes
CREATE INDEX idx_operators_badge ON operators(badge);
CREATE INDEX idx_operators_email ON operators(email);
CREATE INDEX idx_items_item_code ON items(item_code);
CREATE INDEX idx_locations_location_code ON locations(location_code);
CREATE INDEX idx_scans_item_code ON scans(item_code);
