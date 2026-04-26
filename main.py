from fastapi import FastAPI
from routers import todos, users
from database import engine, Base                                                                    
import db_models

db_models.Base.metadata.create_all(bind=engine)     
      
app = FastAPI()
app.include_router(todos.router)
app.include_router(users.router)