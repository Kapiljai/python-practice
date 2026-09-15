from fastapi import FastAPI , HTTPException
from pydantic import BaseModel
import logging
logger = logging.getLogger('uvicorn.error')
app = FastAPI()
# logger.info(app)

class Task(BaseModel):
    name : str
    age : int
    task : bool
#todo app
todos = []

@app.post("/create")
def todo_create(task : Task):
    data = {
        "name" : task.name,
        "age": task.age,
        "task" : task.task
    }
    todos.append(data)
    return {"message" : "Todos add" , "data" : todos} 
    
@app.get("/todos")
def todo():
    if todos is not None:
        return todos
  

@app.get("/todo/{name}")
def get_by_name(name : str):
    for todo in todos:
        if todo["name"] == name:
            return todo
    raise HTTPException(
        status_code=404,
        detail="Todo not found"
    )

@app.delete("/todo/{name}")
def delete(name : str):
    for todo in todos:
        if todo["name"] == name:
            todo.remove(todo)
            return{
                "message" : "successfully delete"
            }
    raise HTTPException(
        status_code=404,
        detail="Data Not Found"
    )
    
@app.put("/todo/{name}")
def update(name : str , age : int , task : bool):
    for todo in todos:
        if todo["name"] == name:
            data = {
                "name" : name,
                "age" : age,
                "task" : task
            }
            todo.update(data)
            return {
                "message" : "Todo data updated successfully"
            }
        