# Library Import
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime

# Custom Functions
from Database_Handler import db_query
from Custom_Functions import response_dictionary as r_d, response_dictionary_2 as r_d_2
from Custom_Functions import time_filter


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
            time = time_filter(time)
            values = (id, time)
            db_query(sql, values)

            # Show the current entry in check_in_out table
            sql = 'select * from check_in_out where id=?'
            values = (id,)
            check_in = db_query(sql, values)
            check_in = r_d_2(check_in)  # convert data to json format

            return check_in

    else:
        raise HTTPException(
            status_code=404, detail="Requested User Id is not in the Database")


# API : POST checkout
# Input Format for Post method is Check which is predefined and same as checkin


# Functions For API : POST checkout
def add_to_attendence(id, checkin_time, checkout_time):
    t = datetime.strptime(checkin_time, "%Y-%m-%d %H:%M:%S")
    day = t.day
    month = t.month
    year = t.year
    x = datetime.date(t)
    week = x.strftime("%V")

    sql = "Insert into attendence values(?,?,?,?,?,?,?)"
    values = (id, checkin_time, checkout_time, day, week, month, year)
    db_query(sql, values)


def remove_check_in(id):
    sql = 'DELETE FROM check_in_out WHERE id=?'
    values = (id,)
    db_query(sql, values)


# API : POST checkout
@app.post("/checkout")
def check_out(checkout: Check):
    id = checkout.id
    sql = "Select * from users where id = ?"
    values = (id,)
    user = db_query(sql, values)
    user = r_d(user)

    # check if requested user_id is in the database
    if (user):
        # query for checking if user is checked in or not
        sql = 'select * from check_in_out where id = ?'
        values = (id,)
        user = db_query(sql, values)
        # r_d_2 formats the data to json dictionary of check_in_out format
        user = r_d_2(user)

        # check if requested is checked in or not
        if user:
            checkout_time = str(datetime.now())
            checkout_time = time_filter(checkout_time)  # filtered current time
            checkin_time = user[0]['time']

            # Insert Checkin and checkout time in attendence table
            add_to_attendence(id, checkin_time, checkout_time)

            # Remove data from check_in_out table as employee checked out
            remove_check_in(id)
