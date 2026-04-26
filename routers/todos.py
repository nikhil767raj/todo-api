from fastapi import APIRouter, HTTPException, Depends                                                
from sqlalchemy.orm import Session                                                                   
from database import get_db                                                                          
from db_models import Todo as TodoModel, User                                                        
from models import Todo
from auth import get_current_user      
from models import Todo, TodoResponse

                                                        
router = APIRouter()                                                                                 
                                                        
@router.post("/todos", response_model=TodoResponse)
def create_todo(todo: Todo, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):                                                                          
    db_todo = TodoModel(title=todo.title, completed=todo.completed, user_id=current_user.id)
    db.add(db_todo)                                                                                  
    db.commit()                                           
    db.refresh(db_todo)                                                                              
    return db_todo                                        

@router.get("/todos", response_model=list[TodoResponse])    
def get_todos(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(TodoModel).filter(TodoModel.user_id == current_user.id).all()                    
                                                                                                    
@router.get("/todos/{todo_id}", response_model=TodoResponse)                                                                     
def get_todo(todo_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):                               
    todo = db.query(TodoModel).filter(TodoModel.id == todo_id, TodoModel.user_id == current_user.id).first()                                                                             
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")                                
    return todo                                                                                      

@router.put("/todos/{todo_id}", response_model=TodoResponse)                                                                      
def update_todo(todo_id: int, updated_todo: Todo, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):                                                                         
    todo = db.query(TodoModel).filter(TodoModel.id == todo_id, TodoModel.user_id == current_user.id).first()                                                                             
    if not todo:                                          
        raise HTTPException(status_code=404, detail="Todo not found")
    todo.title = updated_todo.title                                                                  
    todo.completed = updated_todo.completed
    db.commit()                                                                                      
    db.refresh(todo)                                      
    return todo
                                                                                                    
@router.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):                               
    todo = db.query(TodoModel).filter(TodoModel.id == todo_id, TodoModel.user_id == current_user.id).first()                                                                             
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")                                
    db.delete(todo)                                                                                  
    db.commit()
    return {"message": "Todo deleted"}                                                               
                                                        