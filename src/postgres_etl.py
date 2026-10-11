"""Optional PostgreSQL loader for synthetic laboratory samples.

Requires LABDATA_DATABASE_URL environment variable; never stores credentials.
The Streamlit dashboard does not need a database to operate.
"""
import os
import pandas as pd
from sqlalchemy import create_engine, text
from src.data import generate_laboratory_data, clean_laboratory_data
from src.quality import audit_samples

DDL = """
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
"""

UPSERT = """
INSERT INTO laboratory_samples
(sample_id, sampled_at, product, batch, temperature_c, ph, target, assay_pct)
VALUES (:sample_id, :sampled_at, :product, :batch, :temperature_c, :ph, :target, :assay_pct)
ON CONFLICT (sample_id) DO UPDATE SET
sampled_at = EXCLUDED.sampled_at,
product = EXCLUDED.product,
batch = EXCLUDED.batch,
temperature_c = EXCLUDED.temperature_c,
ph = EXCLUDED.ph,
target = EXCLUDED.target,
assay_pct = EXCLUDED.assay_pct;
"""

def records_for_loading(df):
    """Prepare validated rows, replacing pandas missing values with SQL NULL."""
    required = ["sample_id", "date", "product", "batch", "temperature_c", "ph", "target", "assay_pct"]
    missing = set(required) - set(df.columns)
    if missing:
        raise ValueError("Faltan columnas: " + ", ".join(sorted(missing)))
    data = df[required].rename(columns={"date": "sampled_at"}).copy()
    data["sampled_at"] = pd.to_datetime(data["sampled_at"], errors="raise")
    data = data.astype(object).where(pd.notna(data), None)
    return data.to_dict("records")

def load_to_postgres(database_url, df):
    """Idempotent UPSERT, executed in a single transaction."""
    if not database_url.startswith(("postgresql://", "postgresql+psycopg://")):
        raise ValueError("La conexión debe usar PostgreSQL.")
    records = records_for_loading(df)
    engine = create_engine(database_url, pool_pre_ping=True)
    try:
        with engine.begin() as connection:
            connection.execute(text(DDL))
            if records:
                connection.execute(text(UPSERT), records)
    finally:
        engine.dispose()
    return len(records)

def main():
    url = os.environ.get("LABDATA_DATABASE_URL")
    if not url:
        raise SystemExit("Falta LABDATA_DATABASE_URL. No se realizó ninguna conexión.")
    raw = generate_laboratory_data()
    report = audit_samples(raw)
    clean = clean_laboratory_data(raw)
    count = load_to_postgres(url, clean)
    print(f"Registros cargados o actualizados: {count}")
    print(report.to_string(index=False))

if __name__ == "__main__":
    main()
