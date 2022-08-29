# Library Import
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime

# Custom Functions
from Database_Handler import db_query
from Custom_Functions import response_dictionary as r_d, response_dictionary_2 as r_d_2


app = FastAPI()


# API : GET users
@app.get("/users")
def get_users():
    sql = "Select * from users"
    values = False
    users = db_query(sql, values)

    users = r_d(users)
    # r_d function take users list and converts it to api output format(json)
    return users


# API : GET users/{userid}
@app.get("/users/{userid}")
def get_user_by_id(userid: int):
    id = userid
    sql = "Select * from users where id=?"
    values = (id,)
    users = db_query(sql, values)

    # r_d function take users list and converts it to api output format(json)
    user = r_d(users)
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="Id not in database")


# API : POST adduser
# Input Format for Post method
class User(BaseModel):
    m_id: int  # Id of the person who requested post method
    id: int
    name: str
    role: str


# API : POST adduser
@app.post("/adduser")
def post_add_user(user: User):
    m_id = user.m_id
    id = user.id
    name = user.name
    role = user.role

    if (role != 'employee'):
        raise HTTPException(
            status_code=404, detail="Role of the added person is not Employee")

    sql = "Select * from users where id=?"
    values = (m_id,)
    user = db_query(sql, values)
    user = r_d(user)
    if user:
        # Check If requested user is manager
        if (user[0]['role'] != 'manager'):
            raise HTTPException(
                status_code=404, detail="Requested id is not a manager")

    else:
        raise HTTPException(
            status_code=404, detail="Id of Requested Person is not in Database")

    values = (id,)
    # Check if added id is already in the database
    existance_check = db_query(sql, values)  # Previous sql

    if (existance_check):
        raise HTTPException(
            status_code=404, detail="Id of Employee already Exists")

    else:
        # Add Employee
        sql = "Insert into users values(?,?,?)"
        values = (id, name, role)
        db_query(sql, values)
        # Return All employees with the new employee added
        return get_users()


# API : POST checkin

# Input Format for Post method
class Check(BaseModel):
    id: int


# API : POST checkin
@app.post("/checkin")
def check_in(checkin: Check):
    id = checkin.id
    sql = "select * from users where id=?"
    values = (id,)
    user = db_query(sql, values)
    user = r_d(user)

    # check if requested user_id is in the database
    if (user):
        sql = 'select * from check_in_out where id = ?'
        values = (id,)
        user = db_query(sql, values)

        # r_d_2 formats the data to json dictionary of check_in_out format
        user = r_d_2(user)

        # check if requested user is already checked in
        if user:
            raise HTTPException(
                status_code=404, detail="Already Checked In")
        else:
            # Insert id and current time to check_in_out table
            sql = 'Insert into check_in_out values(?,?)'
            time = str(datetime.now())
