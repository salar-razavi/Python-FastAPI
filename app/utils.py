from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash_password ( password : str)->str:
    return pwd_context.hash(password)
def verify_password(password_input,password_real):
    return pwd_context.verify(password_input,password_real)