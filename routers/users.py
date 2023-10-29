from fastapi import APIRouter, Form, HTTPException
from typing import Annotated
from pydantic import BaseModel
import uuid
import csv
from fastapi import Depends
from auth import oauth2_scheme



router = APIRouter()


class Person(BaseModel):
    id: str
    username: str
    firstname: str
    lastname: str
    email: str
    password: str


#Save to a csv 
def save_to_csv(data):
    with open("new.csv", "a", newline='') as file:
        writer = csv.writer(file)
        writer.writerow([data.id, data.username, data.firstname, data.lastname, data.email, data.password])
        
    
#Password Validation
def is_valid_password(password):
    return any(c.isalpha() for c in password) and any(c.isdigit() for c in password) and any(c.isalnum() for c in password) and any(c.isupper() for c in password)


# Sign Up Route

@router.post("/signup", status_code=200)
async def signup(
    username: Annotated[str, Form()],
    firstname: Annotated[str, Form()],
    lastname: Annotated[str, Form()],
    email: Annotated[str, Form()],
    password: Annotated[str, Form()],
):
    with open('new.csv', mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row and row[1] == username:
                raise HTTPException(status_code=400, detail="Username already exists")
            if row and row[4] == email:
                raise HTTPException(status_code=400, detail="Email already exists")
            if len(password) < 8 or not is_valid_password(password):
                raise HTTPException(status_code=400, detail="Password must be at least 8 characters long and contain at least one letter, and one digit") 
    new_user = Person(id=str(uuid.uuid4()), username=username, firstname=firstname, lastname=lastname, email=email, password=password,)
    save_to_csv(new_user)
    return {"Signup Successful"}




#Login Route

@router.post("/login", status_code=200)
async def login(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
):
    with open('new.csv', mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row and row[1] == username:
                if row[5] == password:
                    return {"message": "Login successful"}
                else:
                    raise HTTPException(status_code=401, detail="Invalid Username and Password Combination")
        raise HTTPException(status_code=404, detail="Invalid Username and Password Combination")

@router.get("/users/me")
async def read_users_me(current_user: str = Depends(oauth2_scheme)):
    return {"username": current_user}
