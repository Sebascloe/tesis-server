from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List
from data.users import list_user

class User(BaseModel):
    id:int
    username:str
    password: str

class UserResponse(BaseModel):
    status: int
    user : User

class UsersResponse(BaseModel):
    status: int
    users : List[User]


app =FastAPI()

@app.get("/users",status_code= status.HTTP_200_OK ,response_model= UsersResponse)
def get_users():
    return{
        "status" : 200,
        "users" : list_user
    }

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id : int):
    for user in list_user:
        if user["id"] == user_id:
            return {
                "status" : 200,
                "user" : user
            }

@app.post("/users", response_model=UserResponse)
def create_user(user_data : User):
    new_user = user_data.model_dump()
    list_user.append(new_user)
    return {
        "status" : 201,
        "user" : new_user
    }

@app.put("/users/{user_id}", response_model= UserResponse)
def update_user(user_data : User, user_id: int):
    for user in list_user:
        if user["id"] == user_id:
            user["username"] = user_data.username
            user["password"] = user_data.password
            return {
                "status": 200,
                "user" : user
            }
        
@app.delete("/users/{user_id}", response_model=UserResponse)
def remove_user(user_id : int):
    for user in list_user:
        if user["id"] == user_id:
            list_user.remove(user)
            return {
                "status" : 200,
                "user" : user
            } 
        



@app.get("/")
def route():
    return {"msg": "XD"}