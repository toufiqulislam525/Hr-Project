# A Little Explanation on The Project
This project is a HR system called “HR Hero”. It stores the data of users in a office and handles the role of individual users. Based on roles it gives the users some functionality.
## Functionality
1. Employess can check-in and check-out
2. Employees can view attendence reports
3. Employees can apply for leave
4. Managers can add employees to the system
5. Managers can process leave requests(Approve Or Deny)

These Functionalities are managed by different REST API endpoints.
## Api Endpoints
1.  GET users
2.  GET users/{userid}
3.  POST adduser (only manager can do this)
4.  POST checkin
5.  POST checkout
6.  GET attendancereport/daily (for individual user)
7.  GET attendancereport/weekly (for individual user)
8.  GET attendancereport/monthly (for individual user)
9.  POST applyforleave (employee)
10. POST processleaverequest (manager)

# Database Schema
## Tables(columns)
1. users(id,name,role)
2. check_in_out(id,time)
3. attendence(id,check_in,check_out,day,week,month,year)
4. leave_request(id,start_date,end_date,approved)

# Enviroment Setup
## Dependencies
1. FastAPI
2. SQLite

## Setup