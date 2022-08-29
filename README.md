# A Little Explanation on The Project
This project is a HR system called “HR Hero”. It stores the data of users in a office and handles the role of individual users. Based on roles it gives the users some functionality.
## Functionality
1. Employess can check-in and check-out
2. Employees can view attendence reports
3. Employees can apply for leave
4. Managers can add employees to the system
5. Managers can process leave requests(Approve Or Deny)

These Functionalities are managed by different REST API endpoints.
## REST Api Endpoints
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

# Getting Started
## Dependencies
1. FastAPI
2. SQLite

## Dependencies Setup For Windows

Install pipenv using pip command
```sh 
pip install --user pipenv
```
Create a new enviroment using pipenv
```sh 
pipenv install 
```
Activate new enviroment using following command
```sh 
pipenv shell
```
Install dependecies using pipenv
```sh 
pipenv  install fastapi
```

## APIs :
###  GET users
URL : 
```
/users
```
Output : 
```sh 
[
  {
    "id": 1,
    "name": "Protim",
    "role": "manager"
  },
  {
    "id": 2,
    "name": "Joy",
    "role": "employee"
  },
  {
    "id": 3,
    "name": "Shuvo",
    "role": "employee"
  },
]
```

###  GET users/{userid}
URL:
```sh
/users/1
```

Output : 
```sh
[
  {
    "id": 1,
    "name": "Protim",
    "role": "manager"
  }
]
```

### POST adduser
URL :
```sh
/adduser
```
Example Input value:
```sh
{
  "m_id": 1,
  "id": 10,
  "name": "Samir",
  "role": "employee"
}
```
Output:

This Post Method Returns all users with new added user
```sh
[
  {
    "id": 1,
    "name": "Protim",
    "role": "manager"
  },
  {
    "id": 2,
    "name": "Joy",
    "role": "employee"
  },
  {
    "id": 3,
    "name": "Shuvo",
    "role": "employee"
  },
  {
    "id": 10,
    "name": "Samir",
    "role": "employee"
  }
]
```

### POST checkin
URL :
```sh
/checkin
```
Example Input value:
```sh
{
  "id": 2
}
```
Output:

This Post method returns newly created checkin entry

```sh
[
  {
    "id": 2,
    "time": "2022-08-29 18:45:31"
  }
]
```


### POST checkout
URL :
```sh
/checkout
```
Example Input value:
```sh
{
  "id": 2
}
```
Output:

This Post method returns new entry in attendence with checkin and checkout values

```sh
[
  {
    "id": 2,
    "check_in": "2022-08-29 18:45:31",
    "check_out": "2022-08-29 18:46:00",
    "day": 29,
    "week": 35,
    "month": 8,
    "year": 2022
  }
]
```
### GET attendancereport/daily
URL : 
```sh
/attendancereport/daily
```
Output : 
```sh 
[
  {
    "id": 2,
    "time": "2022-08-29 18:36:36"
  }
]
```
### GET attendancereport/weekly
URL : 
```sh
/attendancereport/weekly
```
Output : 

Output will be in the format of for every year-week there will be a list of ids with corresponding attendance values
```sh 
{
  "2022-35": {
    "2": 1
  }
}
```

### GET attendancereport/monthly
URL : 
```sh
/attendancereport/monthly
```
Output : 

Output will be in the format of for every year-month there will be a list of ids with corresponding attendance values
```sh 
{
  "2022-8": {
    "2": 1
  }
}
```

### POST applyforleave 
URL :
```sh
/applyforleave
```
Example Input value:
```sh
{
  "id": 2,
  "start_date": "2022-09-29T12:59:54.684Z",
  "end_date": "2022-10-25T12:59:54.684Z"
}
```

Output :

Output will be the Leave Request which is created
```sh
[
  {
    "id": 2,
    "start_date": "2022-09-29",
    "end_date": "2022-10-25",
    "Approved": "Pending"
  }
]
```

### POST processleaverequest
URL : 
```sh
/processleaverequest
```
Example Input value:

process value -1 represents deny, process value 1 represents approve
```sh
{
  "m_id": 1,
  "id": 2,
  "process": -1
}
```
Output:

Output will be the Leave Request which has been processed
```sh
[
  {
    "id": 2,
    "start_date": "2022-09-29",
    "end_date": "2022-10-25",
    "Approved": "Denied"
  }
]
```