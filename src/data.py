import numpy as np
import pandas as pd


def generate_laboratory_data(n=600, seed=42):
    """Generate reproducible synthetic laboratory quality-control data."""
    rng = np.random.default_rng(seed)
    products = rng.choice(["Solucion A", "Reactivo B", "Buffer C"], size=n)
    targets = np.select([products == "Solucion A", products == "Reactivo B"], [98.0, 101.0], default=100.0)
    assay = targets + rng.normal(0, 2.2, n)
    anomalies = rng.choice(n, size=max(1, n // 25), replace=False)
    assay[anomalies] += rng.choice([-1, 1], len(anomalies)) * rng.uniform(7, 12, len(anomalies))
    dates = pd.Timestamp("2026-01-01") + pd.to_timedelta(rng.integers(0, 250, n), unit="D")
    df = pd.DataFrame({"sample_id": [f"LAB-{i:05d}" for i in range(n)], "date": dates, "product": products, "batch": rng.integers(1000, 1050, n).astype(str), "temperature_c": rng.normal(22, 2, n).round(2), "ph": rng.normal(7, 0.35, n).round(3), "target": targets, "assay_pct": assay.round(2)})
    df.loc[rng.choice(n, size=max(1, n // 30), replace=False), "ph"] = np.nan
    return df


def clean_laboratory_data(df):
    result = df.drop_duplicates(subset=["sample_id"]).copy()
    result["date"] = pd.to_datetime(result["date"], errors="coerce")
    for col in ["ph", "temperature_c", "target", "assay_pct"]:
        result[col] = pd.to_numeric(result[col], errors="coerce")
    result = result.dropna(subset=["date", "assay_pct", "target"])
    result["ph"] = result.groupby("product")["ph"].transform(lambda s: s.fillna(s.median()))
    result["deviation"] = result["assay_pct"] - result["target"]
    result["out_of_spec"] = result["deviation"].abs() > 5
    return result
