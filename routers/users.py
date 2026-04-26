from fastapi import APIRouter, HTTPException, Depends     
from sqlalchemy.orm import Session                                                                   
from database import get_db
from db_models import User                                                                           
from models import UserCreate, UserResponse, TokenResponse             
from auth import hash_password, verify_password, create_access_token, create_refresh_token
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
                                                                                                       
class RefreshRequest(BaseModel):                                                                     
    refresh_token: str

                                                                                                    
router = APIRouter()
                                                                                                    
@router.post("/register", response_model=UserResponse)    
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:                                                                                
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = hash_password(user.password)                                                            
    new_user = User(email=user.email, hashed_password=hashed)                                        
    db.add(new_user)
    db.commit()                                                                                      
    db.refresh(new_user)                                                                             
    return new_user

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):          
    db_user = db.query(User).filter(User.email == form_data.username).first()                        
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")                           
    if not verify_password(form_data.password, db_user.hashed_password):                             
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token({"sub": db_user.email})                                          
    refresh_token = create_refresh_token({"sub": db_user.email})        
    return {                                                                                         
          "access_token": access_token,
          "refresh_token": refresh_token,                                                              
          "token_type": "bearer"                            
      }

@router.post("/refresh")                                                                             
def refresh(refresh_token: str, db: Session = Depends(get_db)):
    email = verify_token(refresh_token)                        
    user = db.query(User).filter(User.email == email).first()                                        
    if not user:                                             
        raise HTTPException(status_code=401, detail="Invalid token")                                 
    new_access_token = create_access_token({"sub": user.email})     
    return {"access_token": new_access_token}     