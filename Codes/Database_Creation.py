import sqlite3

# Database Schema Initialized
# Tables : users,check_in_out,attendence,leave_req


def create_tables():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    create_user_table = """
    CREATE TABLE users(
        id integer,
        name text,
        role text
    )"""

    create_check_in_out_table = """
    CREATE TABLE check_in_out(
        id integer,
        time text
    )"""

    create_attendence_table = """
    CREATE TABLE attendence(
        id integer,
        check_in text,
        check_out text,
        day integer,
        week integer,
        month integer,
        year integer
    )"""

    create_leave_request_table = """
    CREATE TABLE leave_request(
        id integer,
        start_date text,
        end_date text,
        approved integer
    )"""

    try:
        c.execute(create_leave_request_table)
        c.execute(create_user_table)
        c.execute(create_check_in_out_table)
        c.execute(create_attendence_table)
    except Exception as e:
        print(e)
    finally:
        conn.commit()
        conn.close()


# Initialized user table with some dummy data
def hard_code_data():
    data = [
        (1, 'Protim', 'manager'),
        (2, 'Joy', 'employee'),
        (3, 'Shuvo', 'employee')
    ]

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    sql = "Insert into users values(?,?,?)"
    try:
        x = c.execute("select * from users")
        x = list(x)
        if not (x):
            for row in data:
                c.execute(sql, row)
    except Exception as e:
        print(e)

    finally:
        conn.commit()
        conn.close()


if __name__ == "__main__":
    create_tables()
    hard_code_data()
