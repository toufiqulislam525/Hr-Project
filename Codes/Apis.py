# Library Import
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime

# Custom Functions
from Database_Handler import db_query
from Custom_Functions import response_dictionary as r_d


app = FastAPI()


@app.get("/users")
def get_users():
    sql = "Select * from users"
    values = False
    users = db_query(sql, values)
    users = r_d(users)
    return users
