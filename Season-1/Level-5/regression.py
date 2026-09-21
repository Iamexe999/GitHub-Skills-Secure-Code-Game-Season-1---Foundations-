import unittest
from unittest.mock import patch
import code as c

class Regression(unittest.TestCase):
    def test_secure_token_source(self):
        with patch.object(c.secrets, 'choice', return_value='x') as choice:
            self.assertEqual(c.Random_generator().generate_token(16), 'x' * 16)
            self.assertEqual(choice.call_count, 16)

    def test_random_salts_and_wrong_password(self):
        rd, hasher = c.Random_generator(), c.SHA256_hasher()
        salts = [rd.generate_salt() for _ in range(2)]
        self.assertNotEqual(*salts)
        hashed = hasher.password_hash('correct password' * 10, salts[0])
        self.assertTrue(hasher.password_verification('correct password' * 10, hashed))
        self.assertFalse(hasher.password_verification('wrong', hashed))

    def test_legacy_api_is_also_salted_bcrypt(self):
        hasher = c.MD5_hasher()
        a, b = hasher.password_hash('same'), hasher.password_hash('same')
        self.assertNotEqual(a, b)
        self.assertTrue(a.startswith('$2b$'))
        self.assertFalse(hasher.password_verification('wrong', a))
        self.assertEqual(c.PASSWORD_HASHER, 'SHA256_hasher')

if __name__ == '__main__': unittest.main()
