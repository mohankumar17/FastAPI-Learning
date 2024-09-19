from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"]) #Hasing Algorithm is bcrypt

def get_hash_pwd(pwd):
    return pwd_context.hash(pwd)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)