from pydantic import BaseModel ,ConfigDict ,EmailStr
from typing import Optional , List
from datetime import datetime



class User_Create(BaseModel):
    email : EmailStr
    password : str
    

class User_Out(BaseModel):
    id : int
    email : EmailStr
    created_at : datetime
    model_config = ConfigDict(from_attributes=True)
    

class PostBase(BaseModel):
    title : str
    content : str
    published: Optional[bool] = True
    
class PostCreate(PostBase):
    pass

class Posts(BaseModel):
    id : int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
        

        
        
class Update_Post (PostBase):
    title : Optional[str] = None
    content : Optional[str] = None
    published : Optional[bool] = None
    
    


    
    
class Show_Posts(BaseModel):
    id : int
    title : str
    content : str
    published: bool
    owner_id : int
    created_at: datetime
    voters : Optional[int] = 0
    owner : User_Out
    
    class Config :
        orm_mode = True
    
class User_Update(BaseModel):
    password : str
    
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class Token_Data(BaseModel):
    id : Optional[int] = None