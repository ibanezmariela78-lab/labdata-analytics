import unittest
from src.data import generate_laboratory_data, clean_laboratory_data
from src.predictive import evaluate_assay_model

class PredictiveTests(unittest.TestCase):
    def test_holdout_and_metrics(self):
        data = clean_laboratory_data(generate_laboratory_data(n=120))
        metrics, results = evaluate_assay_model(data)
        self.assertEqual(len(results), 30)
        self.assertEqual(set(metrics["Modelo"]), {"Random Forest", "Referencia (media)"})
        self.assertTrue((metrics["MAE"] >= 0).all())
        self.assertTrue((results["Error absoluto"] >= 0).all())

    def test_small_dataset(self):
        data = clean_laboratory_data(generate_laboratory_data(n=20))
        with self.assertRaises(ValueError):
            evaluate_assay_model(data)

if __name__ == "__main__":
    unittest.main()
