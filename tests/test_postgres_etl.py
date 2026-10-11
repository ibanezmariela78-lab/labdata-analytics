import unittest
from src.data import generate_laboratory_data, clean_laboratory_data
from src.postgres_etl import records_for_loading, load_to_postgres

class PostgresETLTests(unittest.TestCase):
    def test_records_are_prepared(self):
        clean = clean_laboratory_data(generate_laboratory_data(n=40))
        records = records_for_loading(clean)
        self.assertEqual(len(records), 40)
        self.assertIn("sampled_at", records[0])
        self.assertNotIn("date", records[0])

    def test_reject_non_postgres_url(self):
        with self.assertRaises(ValueError):
            load_to_postgres("sqlite:///:memory:", [])

if __name__ == "__main__":
    unittest.main()
