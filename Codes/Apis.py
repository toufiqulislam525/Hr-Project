# Library Import
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime

# Custom Functions
from Database_Handler import db_query
from Custom_Functions import response_dictionary as r_d


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
