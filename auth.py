from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,HTTPException,status
from models.users import UserInDB
from config.database import collection
from pydantic import BaseModel
from typing import Optional

class TokenData(BaseModel):
    username: Optional[str] = None
    
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = "83daa0256a2289b0fb23693bf1f6034d44396675749244721a2b20e896e11662"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_user(db, username: str):
    user_dict = db.find_one({"username": username})
    return user_dict

def authenticate(username: str, password: str, db):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user["password"]):
        return False
    return user

def create_access_token(data:dict, expires_delta:timedelta):
    to_encode=data.copy()
    if expires_delta:
        expire=datetime.utcnow()+expires_delta
    else:
        expire=datetime.utcnow()+timedelta(minutes=15)
    to_encode.update({"exp":expire})
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token:str=Depends(oauth2_scheme)):
    credential_exception=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credential_exception
        token_data=TokenData(username=username)
    except JWTError:
        raise credential_exception
    user=get_user(collection,username=token_data.username)
    if user is None:
        raise credential_exception
    return user
        
async def get_current_active_user(current_user:UserInDB=Depends(get_current_user)):
    if current_user["disabled"]:
        raise HTTPException(status_code=400,detail="Inactive user")
    return current_user