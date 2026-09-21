# Welcome to Secure Code Game Season-1/Level-5!

# This is the last level of our first season, good luck!

import secrets
import os
import bcrypt

class Random_generator:

    # generates a random token
    def generate_token(self, length=8, alphabet=(
    '0123456789'
    'abcdefghijklmnopqrstuvwxyz'
    'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    )):
        return ''.join(secrets.choice(alphabet) for _ in range(length))

    # generates salt
    def generate_salt(self, rounds=12):
        return bcrypt.gensalt(rounds=rounds)

class Bcrypt_hasher:
    @staticmethod
    def _password_bytes(password):
        encoded = password.encode('utf-8')
        # bcrypt has a 72-byte limit. Fail explicitly; never silently truncate.
        if not encoded or len(encoded) > 72:
            raise ValueError("Password must contain between 1 and 72 UTF-8 bytes")
        return encoded

    def password_hash(self, password, salt):
        return bcrypt.hashpw(self._password_bytes(password), salt).decode('ascii')

    def password_verification(self, password, password_hash):
        try:
            return bcrypt.checkpw(self._password_bytes(password), password_hash.encode('ascii'))
        except (ValueError, UnicodeError):
            return False


# Legacy name retained for the supplied tests; the algorithm is bcrypt.
SHA256_hasher = Bcrypt_hasher

class MD5_hasher(SHA256_hasher):
    """Legacy API name only: new hashes use salted bcrypt, never MD5.

    Existing MD5 digests require a password reset; they are not accepted.
    """
    def password_hash(self, password):
        return super().password_hash(password, bcrypt.gensalt())

# a collection of sensitive secrets necessary for the software to operate
PRIVATE_KEY = os.environ.get('PRIVATE_KEY')
PUBLIC_KEY = os.environ.get('PUBLIC_KEY')
SECRET_KEY = os.environ.get('SECRET_KEY')
PASSWORD_HASHER = 'Bcrypt_hasher'


# Contribute new levels to the game in 3 simple steps!
# Read our Contribution Guideline at github.com/skills/secure-code-game/blob/main/CONTRIBUTING.md