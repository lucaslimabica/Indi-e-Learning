import sqlite3

DATABASE = "databasel.db"

def get_connection(DATABASE):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    return conn, cursor

def get_users() -> list[tuple]:
    """
    RETURN a list of tuples of 
    all users from table 'users'

    ### Return
    [(id, username, password),]
    
    get_users()
    >>> [(1, 'admin', '123456789'), (2, 'user', '987654321'),]
    """
    conn, cursor = get_connection(DATABASE)
    try:
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        conn.commit()
        conn.close()
        if users == "None":
            return "Error: Users Table is Empty"
    except sqlite3.OperationalError:
        return "Error: This Table my be not exist, Complete Error: {sqlite3.OperationalError}"
    return users

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
            return "Error: ID or Username did not exist"
        return user
    except sqlite3.OperationalError:
        return f"Error: Maybe the Database isnt avaliable, Complete Error: {sqlite3.OperationalError}"

def create_user(userjson: dict):
    conn, cursor = get_connection(DATABASE)
    username = userjson["username"]
    password = userjson["password"]
    try:
        # Inserir usuário na tabela users
        cursor.execute("INSERT INTO users (username, password) VALUES (:username, :password)",
                       {"username": userjson["username"],
                        "password": userjson["password"]
                       })
        conn.commit()

        # Selecionar o usuário recém-criado
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()

        conn.close()
        return user
    except sqlite3.OperationalError as e:
        return f"Error: Maybe the Database isn't available, Complete Error: {str(e)}"

def get_courses() -> list[tuple]:
    conn, cursor = get_connection(DATABASE)
    try:
        cursor.execute("SELECT * FROM courses")
        courses = cursor.fetchall()
        conn.commit()
        conn.close()
        if courses == "None":
            return "Error: Courses Table is Empty"
    except sqlite3.OperationalError:
        return False, f"Error: This Table my be not exist, Complete Error: {sqlite3.OperationalError}"
    return courses

def get_course(id: int, name: str=None) -> tuple:
    conn, cursor = get_connection(DATABASE)
    try:
        if id:
            cursor.execute("SELECT * FROM courses WHERE id =?", (id,))
        elif name:
            cursor.execute("SELECT * FROM courses WHERE username =?", (name,))
        course = cursor.fetchone()
        conn.commit()
        conn.close()
        if course == "None":
            return "Error: ID or Name did not exist"
        return course
    except sqlite3.OperationalError:
        return f"Error: Maybe the Database isnt avaliable, Complete Error: {sqlite3.OperationalError}"

def create_course(coursejson: dict):
    conn, cursor = get_connection(DATABASE)

    try:
        # Inserir usuário na tabela users
        cursor.execute("INSERT INTO courses (name, description, subscriptions, value, professor_id) VALUES (:name, :description, :subscriptions, :value, :professor_id)",
                       {"name": coursejson["name"],
                        "description": coursejson["description"],
                        "subscriptions": coursejson["subscriptions"],
                        "value": coursejson["value"],
                        "professor_id": coursejson["professor_id"]})
        conn.commit()

        # Selecionar o usuário recém-criado
        cursor.execute("SELECT * FROM courses WHERE name = ? AND value = ?", (coursejson["name"], coursejson["value"]))
        user = cursor.fetchone()

        conn.close()
        return user
    except sqlite3.OperationalError as e:
        return f"Error: Maybe the Database isn't available, Complete Error: {str(e)}"
    
print(f"Getter Unique (username for example): {get_user(1)[1]}")
print(f"General Getter: {get_users()}")
print(f"Course Getter Unique: {get_courses()}")
print(f"Getting Course ID: {get_course(2)}")