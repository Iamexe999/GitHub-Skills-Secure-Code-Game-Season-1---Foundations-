import unittest
import code as c

class Regression(unittest.TestCase):
    def test_invalid_products(self):
        for quantity in (-1, 0, 1.5, True, 101):
            result = c.validorder(c.Order('r', [c.Item('product', 'tv', 10, quantity)]))
            self.assertIn('Invalid', result)

    def test_nonfinite_amounts(self):
        for amount in (float('nan'), float('inf'), float('-inf')):
            self.assertIn('Invalid', c.validorder(c.Order('r', [c.Item('payment', '', amount, 1)])))

    def test_large_cancellation_in_both_orders(self):
        items = [c.Item('payment', '', 1e19, 1), c.Item('product', '', 1000, 1), c.Item('payment', '', -1e19, 1)]
        for order in (items, list(reversed(items))):
            self.assertEqual(c.validorder(c.Order('r', order)), 'Order ID: r - Payment imbalance: $-1000.00')

if __name__ == '__main__': unittest.main()
