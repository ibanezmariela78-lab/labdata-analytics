"""Synthetic inventory and procurement indicators (conceptual MM/PP workflow)."""
import numpy as np
import pandas as pd


def generate_inventory_data(n=120, seed=123):
    rng = np.random.default_rng(seed)
    materials = [("MAT-001", "Acido citrico", "kg"), ("MAT-002", "Cloruro de sodio", "kg"), ("MAT-003", "Etanol", "L"), ("MAT-004", "Frascos esteriles", "unidades")]
    chosen = rng.integers(0, len(materials), size=n)
    stock = rng.integers(0, 600, size=n)
    minimum = rng.integers(50, 180, size=n)
    lead = rng.integers(2, 30, size=n)
    return pd.DataFrame({
        "record_id": [f"INV-{i:05d}" for i in range(n)],
        "material_code": [materials[i][0] for i in chosen],
        "material": [materials[i][1] for i in chosen],
        "unit": [materials[i][2] for i in chosen],
        "warehouse": rng.choice(["Central", "Produccion", "Control de calidad"], n),
        "stock": stock,
        "reorder_point": minimum,
        "lead_time_days": lead,
        "unit_cost_ars": rng.uniform(100, 12000, size=n).round(2),
        "supplier": rng.choice(["Proveedor Norte", "Proveedor Sur", "Proveedor Este"], n),
    })


def inventory_kpis(df):
    result = df.copy()
    result["below_reorder"] = result["stock"] < result["reorder_point"]
    result["stock_value_ars"] = (result["stock"] * result["unit_cost_ars"]).round(2)
    result["replenishment_qty"] = (result["reorder_point"] - result["stock"]).clip(lower=0)
    return result
