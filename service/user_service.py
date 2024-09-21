from passlib.context import CryptContext

from model.user import User;
from repository import user_repository as UserRepository;

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

def get_all_users() -> list[User]:
    return UserRepository.get_all()

def authenticate_user(pName, pPlainPass: str) -> User | None:
    user = UserRepository.get_one_by_name(pName)
    if user is None:
        return None 
    
    if not verify_password(pPlainPass, user.hash):
        return None 
    
    return user
    
def verify_password(pPlainPass, pHashPass: str) -> bool:
    return pwd_context.verify(pPlainPass, pHashPass)

