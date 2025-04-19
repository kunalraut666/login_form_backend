from pydantic import BaseModel

class UserLogin(BaseModel):
    email: str
    password: str
    
class UserCreate(BaseModel):
    email: str
    password: str
    full_name: str

class UserOut(BaseModel):
    id: int
    email: str
    full_name: str
    ok: bool

    class Config:
        orm_mode = True

class Token(BaseModel):
    ok: bool
    full_name: str
    access_token: str
    token_type: str
