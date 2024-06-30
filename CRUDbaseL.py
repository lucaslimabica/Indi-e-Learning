import sqlite3

DATABASE = "databasel.db"

def get_connection(DATABASE):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    return conn, cursor

def get_users() -> list[tuple]:
    conn, cursor = get_connection(DATABASE)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.commit()
    conn.close()
    return f"{users}"
