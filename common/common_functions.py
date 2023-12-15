from config import SESSIONLOCAL
from passlib.context import CryptContext


def get_db():
    try:
        db= SESSIONLOCAL()
        yield db
    finally:
        db.close()

bcrypt_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

def get_password_hash(password):
    return bcrypt_context.hash(password)

def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)



