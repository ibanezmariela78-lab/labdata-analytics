import unittest
import pandas as pd
from src.data import generate_laboratory_data, clean_laboratory_data


class LaboratoryDataTests(unittest.TestCase):
    def test_reproducible(self):
        first = generate_laboratory_data(n=100, seed=17)
        second = generate_laboratory_data(n=100, seed=17)
        pd.testing.assert_frame_equal(first, second)

    def test_unique_samples_and_flags(self):
        cleaned = clean_laboratory_data(generate_laboratory_data())
        self.assertEqual(len(cleaned), cleaned["sample_id"].nunique())
        self.assertTrue(cleaned["out_of_spec"].eq(cleaned["deviation"].abs() > 5).all())
        self.assertTrue(cleaned["ph"].notna().all())

    def test_duplicate_removal(self):
        raw = generate_laboratory_data(n=20)
        duplicate = pd.concat([raw, raw.iloc[[0]]], ignore_index=True)
        self.assertEqual(len(clean_laboratory_data(duplicate)), 20)


if __name__ == "__main__":
    unittest.main()
