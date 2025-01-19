from fastapi import APIRouter,HTTPException,Depends,status,Request
from models.users import User
from config.database import collection
from scheme.schemas import one_user, many_users
from bson import ObjectId
from datetime import timedelta
from auth import hash_password, verify_password, create_access_token, oauth2_scheme,authenticate,ACCESS_TOKEN_EXPIRE_MINUTES,get_current_active_user
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import FileResponse
from pydantic import BaseModel
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import bleach

class Token(BaseModel):
    access_token: str
    token_type: str

router=APIRouter()

limiter = Limiter(key_func=get_remote_address)

@router.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("static/favicon.ico")

@router.get("/")
async def get_users():
    users=collection.find()
    return many_users(users)

@router.get("/{id}")
async def get_user(id:str):
    user=collection.find_one({"_id":ObjectId(id)})
    return one_user(user)
@router.post("/")
async def create_user(user:User):
    sanitized_username = bleach.clean(user.username)
    sanitized_email = bleach.clean(user.email) 
    user.password = hash_password(user.password)
    user_dict = dict(user)
    user_dict["username"] = sanitized_username
    user_dict["email"] = sanitized_email
    result = collection.insert_one(user_dict)
    new_user = collection.find_one({"_id": result.inserted_id})
    return one_user(new_user)

@router.post("/token",response_model=Token)
@limiter.limit("5/minute")
async def login(request:Request,form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate(form_data.username, form_data.password,collection)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    collection.update_one({"username": form_data.username}, {"$set": {"disabled": False}})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me",response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@router.put("/{id}")
async def update_user(id:str,user:User):
    sanitized_username = bleach.clean(user.username)
    sanitized_email = bleach.clean(user.email) 
    user.password = hash_password(user.password)
    user_dict = dict(user)
    user_dict["username"] = sanitized_username
    user_dict["email"] = sanitized_email
    collection.find_one_and_update({"_id":ObjectId(id)},{"$set":user_dict})
    user=collection.find_one({"_id":ObjectId(id)})
    return one_user(user)

@router.delete("/{id}")
async def delete_user(id:str):
    user=collection.find_one({"_id":ObjectId(id)})
    collection.delete_one(user)
    return one_user(user)


