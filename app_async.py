from fastapi import FastAPI, HTTPException
from typing import List, Optional
from BAL_async import TodoBAL_async
from models import Todo, TodoCreate, TodoUpdate
import uvicorn

use_redis = False
app = FastAPI()
todo_bal = TodoBAL_async(use_redis)

@app.post("/todos/", response_model=Todo)
async def create_todo(todo: TodoCreate):
    created_todo = await todo_bal.create_todo(todo.title, todo.description)
    return created_todo

@app.get("/todos/", response_model=List[Todo])
async def read_todos(query: Optional[dict]):
    todos = await todo_bal.search_todos(query)
    if not todos:
        raise HTTPException(status_code=404, detail="No Todo not found with specified filter")
    return todos

@app.get("/todos/{todo_id}", response_model=Todo)
async def read_todo(todo_id: int):
    todo = await todo_bal.get_todo_by_id(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.get("/todos/getcompleted/", response_model=List[Todo])
async def get_completed_todos():
    todos = await todo_bal.get_completed_todos()
    if not todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todos

@app.get("/todos/getpending/", response_model=List[Todo])
async def get_pending_todos():
    todos = await todo_bal.get_pending_todos()
    if not todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todos

@app.put("/todos/{todo_id}", response_model=Todo)
async def update_todo(todo_id: int, todo_update: TodoUpdate):
    updated_todo = await todo_bal.update_todo(todo_id, **todo_update.dict(exclude_unset=True))
    if not updated_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return updated_todo

@app.delete("/todos/{todo_id}", response_model=bool)
async def delete_todo(todo_id: int):
    deletion_status = await todo_bal.delete_todo(todo_id)
    if not deletion_status:
        raise HTTPException(status_code=404, detail="Todo not found")
    return True

if __name__ == "__main__":
    uvicorn.run(app, reload=False, ws_ping_timeout=1800, ws_ping_interval=30)
