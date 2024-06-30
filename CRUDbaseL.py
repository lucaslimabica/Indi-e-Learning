import sqlite3

DATABASE = "databasel.db"

def get_connection(DATABASE):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    return conn, cursor

def get_users() -> list[tuple]:
    conn, cursor = get_connection(DATABASE)
    try:
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        conn.commit()
        conn.close()
        if users == "None":
            return False, "Error: Users Table is Empty"
    except sqlite3.OperationalError:
        return False, f"Error: This Table my be not exist, Complete Error: {sqlite3.OperationalError}"
    return True, f"{users}"

def get_user(id: int, username: str=None) -> tuple:
    conn, cursor = get_connection(DATABASE)
    try:
        if id:
            cursor.execute("SELECT * FROM users WHERE id =?", (id,))
        elif username:
            cursor.execute("SELECT * FROM users WHERE username =?", (username,))
        user = cursor.fetchone()
        conn.commit()
        conn.close()
        if user == "None":
            return False, "Error: ID or Username did not exist"
        return True, f"{user}"
    except sqlite3.OperationalError:
        return False, f"Error: Maybe the Database isnt avaliable, Complete Error: {sqlite3.OperationalError}"


value, data = get_user(2)
print(data, type(data))