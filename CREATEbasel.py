import sqlite3
import datetime

conn = sqlite3.connect('databasel.db')
c = conn.cursor()

c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
""")

c.execute("""
    CREATE TABLE IF NOT EXISTS courses (
        idc INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT NOT NULL,
        subscriptions INTEGER DEFAULT 0,
        professor_id INTEGER NOT NULL,
        value INTEGER,
        FOREIGN KEY (professor_id) REFERENCES professors(idp)
    )
""")

c.execute("""
    CREATE TABLE IF NOT EXISTS professors (
        idp INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        academic_education TEXT NOT NULL,
        user_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
""")

conn.commit()

# c.execute("""INSERT INTO users (username, password) VALUES ('benObiw', 'hellothere123')""")

user = c.execute("""SELECT * FROM users WHERE username = 'benObiw'""").fetchone() # -> Tuple of the user
print(f"Users Login: {user[1]}")

conn.close()
