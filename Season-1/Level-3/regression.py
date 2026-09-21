import unittest
import tempfile
from pathlib import Path
import code as c

class Regression(unittest.TestCase):
    def test_optional_picture(self):
        self.assertIsNone(c.TaxPayer('', '').get_prof_picture())

    def test_absolute_and_symlink_escape(self):
        user = c.TaxPayer('', '')
        with tempfile.TemporaryDirectory() as temp:
            outside = Path(temp) / 'private.txt'
            outside.write_text('must remain outside the document root')
            link = Path(__file__).parent / 'assets' / 'regression-link'
            link.symlink_to(outside)
            try:
                for path in (str(outside), 'assets/regression-link'):
                    self.assertIsNone(user.get_prof_picture(path))
                    self.assertIsNone(user.get_tax_form_attachment(path))
            finally:
                link.unlink()

if __name__ == '__main__': unittest.main()
