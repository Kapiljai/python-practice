from fastapi import FastAPI , HTTPException , status , Query , Depends
from pydantic import BaseModel
import logging
logger = logging.getLogger('uvicorn.error')
app = FastAPI()
# logger.info(app)

class Task(BaseModel):
    name : str
    age : int
    task : bool
    
    
class Profile(BaseModel):
    name : str
    status : bool
    login : bool
class Address(BaseModel):
    address : str
    city : str
    pincode : int
    user : Profile
#todo app

class ProfileResponse(BaseModel):
    name: str
class AddressResponse(BaseModel):
    address: str
    city: str
    pincode: int
    user: ProfileResponse
class UserResponse(BaseModel):
    message : str
    user_data:list[AddressResponse]
    
class TaskUpdate(BaseModel):
    age: int
    task: bool
todos = []

userData = []

@app.post("/create" , status_code= status.HTTP_201_CREATED)
def todo_create(task : Task):
    data = {
        "name" : task.name,
        "age": task.age,
        "task" : task.task
    }
    todos.append(data)
    return {"message" : "Todos add" , "data" : todos} 
    
@app.get("/todos" , status_code=status.HTTP_200_OK)
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
            todos.remove(todo)
            return{
                "message" : "successfully delete"
            }
    raise HTTPException(
        status_code=404,
        detail="Data Not Found"
    )
    
@app.put("/todo/{name}")
def update(name : str, data : TaskUpdate):
    for todo in todos:
        if todo["name"] == name:
            data = {
                "name" : name,
                "age" : data.age,
                "task" : data.task
            }
            todo.update(data)
            return {
                "message" : "Todo data updated successfully"
            }
        
@app.get("/task")
def get_query(task: str = Query(..., min_length = 3), status: bool = False, title: str = ""):
    # Now 'task' is a real string passed by the user
    if task == "Admin":
        return {"message": f"You are searching value by parameter: {task}"}
        
    return {"message": f"Normal search for: {task}"}


@app.post("/user" ,response_model=UserResponse)
def user_create(user_data : Address):
    userData.append(user_data)
    return {
        "message" : "user Successfully created",
        "user_data" : userData
    }
    
# def getToken():
#     return 'my-secret-token'
def verifyToken(token : str):
    if token != 'my-secret-token':
        raise HTTPException(
            status_code= 403,
            detail= "Unauthorized"
        ) 
    return {"token" : token}

@app.get("/profile" , status_code= status.HTTP_202_ACCEPTED)
def profile(token : str = Depends(verifyToken)):
    return {"message" : "Successfully login"}
    
    