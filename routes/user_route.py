import os 
from datetime import timedelta
from fastapi import APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse

from model.user import User
from service import user_service as UserService
from schemas import user as UserSchema
from data.db import get_session

accessTokenExpireMinutes = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES') if os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES') is not None else 15

router = APIRouter(prefix = '/api/user')

oauth2Dep = OAuth2PasswordBearer(tokenUrl="login")

@router.get("/get_all")
def get_all_users():
    users = User.get_all()
    if users is None:
        return JSONResponse({"message": "No user exists"}, status_code=204)
    
    users_list = [{"full name": user.full_name, "email": user.email} for user in users]
    return JSONResponse({"users": users_list}, status_code=200)

@router.post("/login")
def login(pData: UserSchema.UserLoginRequest):
    authedUser = UserService.authenticate_user(pData.email, pData.password)
    if not authedUser:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    expiresMins = timedelta(minutes=accessTokenExpireMinutes)
    access_token = UserService.create_access_token(pData={"sub": authedUser.email}, pExpires=expiresMins)

    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/signup")
async def signup(pData: UserSchema.UserSignupRequest):
    foundUser = User.get_one_by_email(pEmail=pData.email)
    if foundUser:
        return JSONResponse({"message": "User already signed up"}, status_code=409)

    newUser = User(full_name=pData.full_name, email=pData.email, password_hash=UserService.hash_password(pData.password))
    
    with get_session() as session:
        session.add(newUser)
        session.commit()
        return JSONResponse({"message": "Added new user successfully"}, status_code=200)