from fastapi import FastAPI,status
from data.users import list_users
from pydantic import BaseModel
from typing import List

class User(BaseModel):
    id: int
    username: str
    password: str
    
class UserResponse(BaseModel):
    status: int
    user: User

class UsersResponse(BaseModel):
    status: int
    users: List[User]

app = FastAPI()

@app.get('/users', status_code=status.HTTP_200_OK, response_model=UsersResponse)
def get_users():
    return{
        "status" : 200,
        "users" : list_users
    }

@app.get('/users/{user_id}', status_code=status.HTTP_200_OK, response_model=UserResponse)
def get_user(user_id: int):
    for user in list_users:
        if user["id"] == user_id:
            return{
                "status" : 200,
                "user" : user
            }

@app.post('/users', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user_data : User):
    new_user = user_data.model_dump()
    list_users.append(new_user)
    return{
        "status": 201,
        "user": new_user
    }
    
@app.put('/users/{user_id}', status_code=status.HTTP_200_OK, response_model=UserResponse)
def update_user(data_user: User, user_id : int):
    for user in list_users:
        if user['id'] == user_id:
            user["username"] = data_user.username
            user["password"] = data_user.password
            return{
                "status": 200,
                "user": user
            }
            
@app.delete('/users/{user_id}',status_code=status.HTTP_200_OK,response_model=UserResponse)
def delete_user(user_id: int):
    for user in list_users:
        if user["id"] == user_id:
            list_users.remove(user)
            return{
                "status": 200,
                "user": user
            }
