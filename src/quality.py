"""Reproducible ETL quality audit for synthetic laboratory samples."""
import pandas as pd
from src.data import clean_laboratory_data

REQUIRED = ("sample_id", "date", "product", "batch", "temperature_c", "ph", "target", "assay_pct")

def audit_samples(raw):
    """Return source-quality checks before any imputation or deduplication."""
    missing = [c for c in REQUIRED if c not in raw.columns]
    if missing:
        raise ValueError("Faltan columnas obligatorias: " + ", ".join(missing))
    numeric = raw[["temperature_c", "ph", "target", "assay_pct"]].apply(pd.to_numeric, errors="coerce")
    dates = pd.to_datetime(raw["date"], errors="coerce")
    report = [
        ("Registros originales", len(raw)),
        ("Identificadores duplicados", int(raw["sample_id"].duplicated().sum())),
        ("Fechas inválidas o vacías", int(dates.isna().sum())),
        ("pH faltante o inválido", int(numeric["ph"].isna().sum())),
        ("Temperatura faltante o inválida", int(numeric["temperature_c"].isna().sum())),
        ("Ensayo faltante o inválido", int(numeric["assay_pct"].isna().sum())),
        ("Objetivo faltante o inválido", int(numeric["target"].isna().sum())),
        ("pH fuera de rango físico [0,14]", int(((numeric["ph"] < 0) | (numeric["ph"] > 14)).sum())),
    ]
    return pd.DataFrame(report, columns=["Control", "Cantidad"])


def run_etl(raw):
    """Validate source schema, produce audit, and clean samples."""
    report = audit_samples(raw)
    clean = clean_laboratory_data(raw)
    return report, clean
