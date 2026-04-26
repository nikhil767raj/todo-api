from passlib.context import CryptContext
from jose import JWTError, jwt                            
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from db_models import User
from sqlalchemy.orm import Session 
from database import get_db
from config import settings                                                                          
  
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"                                                                                  
ACCESS_TOKEN_EXPIRE_MINUTES = 30



pwd_context = CryptContext(schemes=["bcrypt"] , deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str , hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()                                                                          
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})                                                                
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict):                                                                
    to_encode = data.copy()                               
    expire = datetime.utcnow() + timedelta(days=30)                                                  
    to_encode.update({"exp": expire})              
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return email
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")



def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):            
    email = verify_token(token)
    user = db.query(User).filter(User.email == email).first()                                        
    if user is None:                                                                                 
        raise HTTPException(status_code=401, detail="User not found")
    return user