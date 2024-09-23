from passlib.context import CryptContext
from datetime import datetime
from jose import jwt
import os

from model.user import User;

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

ALGORITHM = "HS256"
JWT_TOKEN_EXPIRES = os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES") # minutes
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

def authenticate_user(pEmail, pPlainPass: str) -> User | None:
    user = User.get_one_by_email(pEmail)
    if user is None:
        return None 
    
    if not verify_password(pPlainPass, user.password_hash):
        return None 
    
    return user
    
def verify_password(pPlainPass, pHashPass: str) -> bool:
    return pwd_context.verify(pPlainPass, pHashPass)

def create_access_token(pData: dict, pExpires: datetime):
    now = datetime.utcnow()
    expires = pExpires or datetime.timedelta(minutes=JWT_TOKEN_EXPIRES)

    src = pData.copy()
    src.update({"exp": now + expires})

    encoded_jwt = jwt.encode(src, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def hash_password(pPassword: str) -> str:
    return pwd_context.hash(pPassword)