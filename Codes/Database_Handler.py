# Manages All database operations
import sqlite3


# db_query(sql,tpls) Database query executer funcion, Parameters are sql and tpls
# sql is the query as string
# tpls is the value provided for the query as tuple


def db_query(sql, tpls):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    if tpls:
        users = c.execute(sql, tpls)
    else:
        users = c.execute(sql)

    users = list(users)
    conn.commit()
    conn.close()
    return users
