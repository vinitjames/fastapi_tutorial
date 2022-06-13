from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str)-> str:
    return pwd_context.hash(password)

def verify_password(raw_pass: str, hashed_pass: str) -> bool:
    return pwd_context.verify(raw_pass, hashed_pass)
