from pydantic import BaseModel
from typing import Optional




class newuser(BaseModel):
    id:int
    username:str
    email:str
    password:str
    WABAID:int
    PAccessToken:str
    Phone_id:int
    api_key:Optional[str]


class register_user(BaseModel):
    username:str
    email:str
    password:str
    WABAID:int
    PAccessToken:str
    Phone_id:int

# login user model

class LoginUser(BaseModel):
    username:str
    password:str