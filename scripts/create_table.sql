CREATE TABLE IF NOT EXISTS insurance_claims (
    IDpol BIGINT,
    ClaimNb INT,
    Exposure FLOAT,
    VehPower INT,
    VehAge INT,
    DrivAge INT,
    BonusMalus INT,
    VehBrand TEXT,
    VehGas TEXT,
    Area TEXT,
    Density FLOAT,
    Region TEXT,
    ClaimAmount FLOAT
);

CREATE TABLE IF NOT EXISTS exposure_summary (
    VehBrand TEXT,
    Area TEXT,
    total_exposure FLOAT
);

CREATE TABLE IF NOT EXISTS density_summary (
    Area TEXT,
    min_density FLOAT,
    max_density FLOAT
);