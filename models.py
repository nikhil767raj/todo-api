from pydantic import BaseModel


class Todo(BaseModel):
    title: str
    completed: bool = False

class UserCreate(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):                           
      access_token: str                                                                                
      token_type: str


class TodoResponse(BaseModel):
    id: int                                                                                          
    title: str                                            
    completed: bool

    class Config:
        from_attributes = True
                                                                                                    
class UserResponse(BaseModel):
    id: int                                                                                          
    email: str                                            

    class Config:
        from_attributes = True

