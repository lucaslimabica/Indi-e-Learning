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

def create_user(userjson: dict):
    conn, cursor = get_connection(DATABASE)
    username = userjson["username"]
    password = userjson["password"]
    try:
        # Inserir usuário na tabela users
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()

        # Selecionar o usuário recém-criado
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()

        conn.close()
        return True, user
    except sqlite3.OperationalError as e:
        return False, f"Error: Maybe the Database isn't available, Complete Error: {str(e)}"

def get_courses() -> list[tuple]:
    conn, cursor = get_connection(DATABASE)
    try:
        cursor.execute("SELECT * FROM courses")
        courses = cursor.fetchall()
        conn.commit()
        conn.close()
        if courses == "None":
            return False, "Error: Courses Table is Empty"
    except sqlite3.OperationalError:
        return False, f"Error: This Table my be not exist, Complete Error: {sqlite3.OperationalError}"
    return True, f"{courses}"

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
            return False, "Error: ID or Name did not exist"
        return True, f"{course}"
    except sqlite3.OperationalError:
        return False, f"Error: Maybe the Database isnt avaliable, Complete Error: {sqlite3.OperationalError}"

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
        return True, user
    except sqlite3.OperationalError as e:
        return False, f"Error: Maybe the Database isn't available, Complete Error: {str(e)}"
    
create_course({
    "name": "The Light Saber 101 Basics Vol.3",
    "description": "How to use a basic light saber", 
    "subscriptions": 2,
    "value": 8100,
    "professor_id": 1 
})