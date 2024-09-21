import os 
from datetime import timedelta
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from model.user import User
from errors.data_errors import DataDuplicationError, DataMissingError
from service import user_service as UserService

accessTokenExpireMinutes = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES') if os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES') is not None else 15

router = APIRouter(prefix = '/api/user')

oauth2Dep = OAuth2PasswordBearer(tokenUrl="login")

@router.get("/get_all")
def get_all_users() -> list[User]:
    return UserService.get_all_users()

@router.post("/login")
async def login(pFormData: OAuth2PasswordRequestForm = Depends()):
    authedUser = UserService.authenticate_user(pFormData.username, pFormData.password)
    if not authedUser:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    expiresMins = timedelta(minutes=accessTokenExpireMinutes)
    