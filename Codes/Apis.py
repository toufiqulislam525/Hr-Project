# Library Import
from select import select
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import date, datetime


# Custom Functions
from Database_Handler import db_query
from Custom_Functions import response_dictionary as r_d, response_dictionary_2 as r_d_2, response_dictionary_3 as r_d_3
from Custom_Functions import attendence_sheet_result_formatter as r_d_4, leave_request_formatter as r_d_5
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
# Input Format for Post method is Check which is predefined and same as checkin
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

            # Return The Attendence table data as response
            sql = "select * from attendence where id = ? and check_in = ?"
            values = (id, checkin_time)
            attendence = db_query(sql, values)
            # r_d_3 formats the data to json dictionary of Attendece format
            attendence = r_d_3(attendence)
            return attendence

        else:
            raise HTTPException(
                status_code=404, detail="User is not Checked In")

    else:
        raise HTTPException(
            status_code=404, detail="Provided User Id is not in the Database")


# API : GET attendancereport

# API : GET attendancereport/daily

def attendence_sheet_generator_daily():
    sql = "select check_in from attendence order by year Desc, month Desc, day Desc"
    values = False
    attendence_sheet = db_query(sql, values)

    date_list = []
    ind_date_list = []
    for check_in in attendence_sheet:
        t = datetime.strptime(check_in[0], "%Y-%m-%d %H:%M:%S")
        y = t.year
        m = t.month
        d = t.day
        date = datetime.date(t)

        if str(date) not in date_list:
            date_list.append(str(date))
            ind_date = (y, m, d)
            ind_date_list.append(ind_date)

    # daily Attendence
    ids_list = []
    for ind_date in ind_date_list:
        sql = "select id from attendence where year = ? and month =? and day = ?"
        values = ind_date
        ids = db_query(sql, values)
        temp = []
        for id in ids:
            if (id[0] not in temp):
                temp.append(id[0])
        ids_list.append(temp)

    attendence_sheet_result = list(zip(ind_date_list, date_list, ids_list))
    return attendence_sheet_result


def attendence_sheet_generator_weekly():
    sql = "select check_in from attendence order by year Desc, month Desc, day Desc"
    values = False
    attendence_sheet = db_query(sql, values)

    date_list = []
    ind_date_list = []
    for check_in in attendence_sheet:
        t = datetime.strptime(check_in[0], "%Y-%m-%d %H:%M:%S")
        y = t.year
        date = datetime.date(t)
        w = date.strftime("%V")  # Week

        if str(date) not in date_list:
            date_list.append(str(date))
            ind_date = (y, w)
            ind_date_list.append(ind_date)

    # Weekly Attendence
    weekly_present = {}
    for ind_date in ind_date_list:
        date = str(ind_date[0])
        date = date + "-" + ind_date[1]
        sql = "select id from attendence where year = ? and week= ?"
        values = ind_date
        ids = db_query(sql, values)
        count_present = {}
        for id in ids:
            x = id[0]
            count_present[x] = count_present.get(x, 0) + 1
        weekly_present[date] = count_present
    return weekly_present


def attendence_sheet_generator_monthly():
    sql = "select check_in from attendence order by year Desc, month Desc, day Desc"
    values = False
    attendence_sheet = db_query(sql, values)

    date_list = []
    ind_date_list = []
    for check_in in attendence_sheet:
        t = datetime.strptime(check_in[0], "%Y-%m-%d %H:%M:%S")
        y = t.year
        m = t.month
        date = datetime.date(t)

        if str(date) not in date_list:
            date_list.append(str(date))
            ind_date = (y, m)
            ind_date_list.append(ind_date)

    # Monthly Attendence
    monthly_present = {}
    for ind_date in ind_date_list:
        date = str(ind_date[0])
        date = date + "-" + str(ind_date[1])
        sql = "select id from attendence where year = ? and month= ?"
        values = ind_date
        ids = db_query(sql, values)
        count_present = {}
        for id in ids:
            x = id[0]
            count_present[x] = count_present.get(x, 0) + 1
        monthly_present[date] = count_present

    return monthly_present


# API : GET attendancereport/daily
@app.get("/attendancereport/daily")
def get_attendancereport_daily():
    attendence_sheet = attendence_sheet_generator_daily()
    attendence_sheet = r_d_4(attendence_sheet)
    return attendence_sheet


# API : GET attendancereport/weekly
@app.get("/attendancereport/weekly")
def get_attendancereport_weekly():
    attendence_sheet = attendence_sheet_generator_weekly()
    return attendence_sheet


# API : GET attendancereport/monthly
@app.get("/attendancereport/monthly")
def get_attendancereport_monthly():
    attendence_sheet = attendence_sheet_generator_monthly()
    return attendence_sheet


# API : POST applyforleave

# Input Format for Post method is Check which is predefined and same as checkin
class leave_request(BaseModel):
    id: int
    start_date: datetime
    end_date: datetime


def check(id):
    sql = "Select * from leave_request where id = ? and approved = 0"
    values = (id,)
    result = db_query(sql, values)
    if not result:
        return True
    else:
        return False


@app.post("/applyforleave")
def apply_for_leave_req(rq: leave_request):
    id = rq.id
    time_difference = rq.end_date - rq.start_date
    time_difference_in_days = time_difference.days
    print(time_difference)
    if (time_difference_in_days <= 0):
        raise HTTPException(
            status_code=404, detail="Invalid Start and end time")

    # Taking Start and End Date Excluding Hour,min,second
    start_date = time_filter(str(rq.start_date))
    start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
    start_date = datetime.date(start_date)

    end_date = time_filter(str(rq.end_date))
    end_date = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
    end_date = datetime.date(end_date)

    # check if given id is in the database and if user's role is employee
    sql = "select * from users where id = ?"
    values = (id,)
    users = db_query(sql, values)
    user = r_d(users)
    if user:
        role = user[0]['role']
        if (role == 'employee'):
            # Check for pending request
            flag = check(id)
            if (flag):
                # Add Leave Request
                sql = "Insert into leave_request values(?,?,?,?)"
                values = (id, start_date, end_date, 0)
                db_query(sql, values)

                # Show Current Leave Request
                sql = "Select * from leave_request where id = ?"
                values = (id,)
                leave_request = db_query(sql, values)
                leave_request = r_d_5(leave_request)
                return leave_request

            else:
                raise HTTPException(
                    status_code=404, detail="Previous Leave Request Pending")
        else:
            raise HTTPException(
                status_code=404, detail="Role of provided id is not employee")
    else:
        raise HTTPException(
            status_code=404, detail="Provided id is not in the database")
