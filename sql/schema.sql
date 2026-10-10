-- Modelo operacional inicial de laboratorio (PostgreSQL)
CREATE TABLE IF NOT EXISTS laboratory_samples (
    sample_id VARCHAR(30) PRIMARY KEY,
    sampled_at TIMESTAMP NOT NULL,
    product VARCHAR(100) NOT NULL,
    batch VARCHAR(40) NOT NULL,
    temperature_c NUMERIC(8,3),
    ph NUMERIC(6,3),
    target NUMERIC(10,3),
    assay_pct NUMERIC(10,3)
);
CREATE INDEX IF NOT EXISTS idx_samples_product_date ON laboratory_samples(product, sampled_at);
