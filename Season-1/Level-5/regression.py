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
        hashed = hasher.password_hash('correct password phrase', salts[0])
        self.assertTrue(hasher.password_verification('correct password phrase', hashed))
        self.assertFalse(hasher.password_verification('wrong', hashed))

    def test_long_password_never_truncated(self):
        hasher = c.Bcrypt_hasher()
        salt = c.Random_generator().generate_salt()
        with self.assertRaises(ValueError):
            hasher.password_hash('x' * 73, salt)
        hashed = hasher.password_hash('x' * 72, salt)
        self.assertFalse(hasher.password_verification('x' * 73, hashed))

    def test_legacy_api_is_also_salted_bcrypt(self):
        hasher = c.MD5_hasher()
        a, b = hasher.password_hash('same'), hasher.password_hash('same')
        self.assertNotEqual(a, b)
        self.assertTrue(a.startswith('$2b$'))
        self.assertFalse(hasher.password_verification('wrong', a))
        self.assertEqual(c.PASSWORD_HASHER, 'Bcrypt_hasher')

if __name__ == '__main__': unittest.main()
