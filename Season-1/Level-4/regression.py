import unittest
import code as c

class Regression(unittest.TestCase):
    def test_injected_symbols_cannot_update_or_read_other_rows(self):
        op = c.DB_CRUD_ops()
        for symbol in ("MSFT'; DROP TABLE stocks--", "' OR 1=1--"):
            self.assertNotIn('[RESULT]', op.get_stock_price(symbol))
            op.update_stock_price(symbol, 999.0)
            self.assertIn('[RESULT] (300.0,)', op.get_stock_price('MSFT'))

    def test_arbitrary_scripts_rejected_before_any_execution(self):
        op = c.DB_CRUD_ops()
        for method in (op.exec_multi_query, op.exec_user_script):
            for query in ("DROP TABLE stocks", "SELECT price FROM stocks WHERE symbol = 'MSFT'; UPDATE stocks SET price = 999", "SELECT * FROM sqlite_master"):
                with self.assertRaises(ValueError): method(query)
        self.assertIn('[RESULT] (300.0,)', op.get_stock_price('MSFT'))

    def test_fractional_price(self):
        op = c.DB_CRUD_ops()
        try:
            op.update_stock_price('MSFT', 300.75)
            self.assertIn('(300.75,)', op.get_stock_price('MSFT'))
        finally:
            op.update_stock_price('MSFT', 300.0)

if __name__ == '__main__': unittest.main()
