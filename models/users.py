from pydantic import BaseModel, Field
from typing import Optional
class User(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str
    password: str = Field(..., min_length=6)
    disabled: Optional[bool] = None
    
class UserInDB(User):
    hashed_password: str
    

