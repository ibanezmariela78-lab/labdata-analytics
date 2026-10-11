import unittest
import pandas as pd
from src.data import generate_laboratory_data
from src.quality import audit_samples, run_etl

class QualityAuditTests(unittest.TestCase):
    def test_missing_ph_count(self):
        raw = generate_laboratory_data(n=90, seed=7)
        report, clean = run_etl(raw)
        counts = dict(zip(report["Control"], report["Cantidad"]))
        self.assertEqual(counts["pH faltante o inválido"], int(raw["ph"].isna().sum()))
        self.assertEqual(len(clean), 90)

    def test_duplicate_count(self):
        raw = generate_laboratory_data(n=30)
        raw = pd.concat([raw, raw.iloc[[0]]], ignore_index=True)
        report = audit_samples(raw)
        counts = dict(zip(report["Control"], report["Cantidad"]))
        self.assertEqual(counts["Identificadores duplicados"], 1)

    def test_required_columns(self):
        with self.assertRaises(ValueError):
            audit_samples(pd.DataFrame({"sample_id": ["x"]}))

if __name__ == "__main__":
    unittest.main()
