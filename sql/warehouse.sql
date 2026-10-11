-- Dimensional warehouse: demonstration model for synthetic lab quality control.
CREATE TABLE IF NOT EXISTS dim_product (
    product_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    product_name TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS dim_batch (
    batch_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    batch_code TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS dim_date (
    date_key DATE PRIMARY KEY,
    calendar_year INTEGER NOT NULL,
    calendar_month INTEGER NOT NULL,
    calendar_day INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS fact_lab_assay (
    sample_id VARCHAR(30) PRIMARY KEY,
    date_key DATE NOT NULL REFERENCES dim_date(date_key),
    product_key BIGINT NOT NULL REFERENCES dim_product(product_key),
    batch_key BIGINT NOT NULL REFERENCES dim_batch(batch_key),
    assay_pct NUMERIC(10,3) NOT NULL,
    target_pct NUMERIC(10,3) NOT NULL,
    temperature_c NUMERIC(8,3),
    ph NUMERIC(6,3),
    out_of_spec BOOLEAN NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_fact_assay_date ON fact_lab_assay(date_key);
CREATE INDEX IF NOT EXISTS idx_fact_assay_product ON fact_lab_assay(product_key);

-- Example: out-of-spec rate by product.
SELECT p.product_name, COUNT(*) AS sample_count,
       ROUND(100.0 * AVG(CASE WHEN f.out_of_spec THEN 1 ELSE 0 END), 2) AS out_of_spec_pct
FROM fact_lab_assay f
JOIN dim_product p ON p.product_key = f.product_key
GROUP BY p.product_name
ORDER BY out_of_spec_pct DESC;
