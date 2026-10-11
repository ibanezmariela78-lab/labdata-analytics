import unittest
from src.inventory import generate_inventory_data, inventory_kpis


class InventoryTests(unittest.TestCase):
    def test_reproducibility(self):
        a = generate_inventory_data(n=15, seed=9)
        b = generate_inventory_data(n=15, seed=9)
        self.assertTrue(a.equals(b))

    def test_replenishment(self):
        df = inventory_kpis(generate_inventory_data(n=100))
        self.assertTrue((df["replenishment_qty"] >= 0).all())
        self.assertTrue((df["below_reorder"] == (df["stock"] < df["reorder_point"])).all())
        self.assertTrue((df["stock_value_ars"] >= 0).all())


if __name__ == "__main__":
    unittest.main()
