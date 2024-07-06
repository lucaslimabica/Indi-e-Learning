import sqlite3

DATABASE = "databasel.db"

def get_connection(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    return conn, cursor

def get_users() -> list[tuple]:
    """
    Retrieve all users from the 'users' table.

    ### Return
    A list of tuples, where each tuple contains:
    (id, username, password)

    ### Example
    get_users()
    >>> [(1, 'admin', '123456789'), (2, 'user', '987654321')]

    ### Error Handling
    If the users table is empty, an error message is returned.
    If there is an operational error (e.g., the table does not exist), an error message is returned.

    ### Returns
    - list of tuples: Each tuple contains user data (id, username, password).
    - str: Error message if an error occurs.
    """
    conn, cursor = get_connection(DATABASE)
    try:
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        if not users:
            return "Error: Users Table is Empty"
    except sqlite3.OperationalError as e:
        return f"Error: This table may not exist, Complete Error: {e}"
    finally:
        conn.commit()
        conn.close()
    return users

def get_user(id: int = None, username: str = None) -> tuple:
    """
    Retrieve a user from the 'users' table by ID or username.

    ### Parameters
    - id (int): The ID of the user.
    - username (str): The username of the user.

    ### Return
    A tuple containing user data (id, username, password).

    ### Example
    get_user(1)
    >>> (1, 'admin', '123456789')

    get_user(username='user')
    >>> (2, 'user', '987654321')

    ### Error Handling
    If the user does not exist, an error message is returned.
    If there is an operational error (e.g., the table does not exist), an error message is returned.

    ### Returns
    - tuple: User data (id, username, password).
    - str: Error message if an error occurs.
    """
    conn, cursor = get_connection(DATABASE)
    try:
        if id is not None:
            cursor.execute("SELECT * FROM users WHERE id = ?", (id,))
        elif username is not None:
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        if not user:
            return "Error: ID or Username did not exist"
    except sqlite3.OperationalError as e:
        return f"Error: Maybe the Database isn't available, Complete Error: {e}"
    finally:
        conn.commit()
        conn.close()
    return user

def create_user(userjson: dict) -> tuple:
    """
    Create a new user in the 'users' table and retrieve the newly created user.

    ### Parameters
    - userjson (dict): A dictionary containing 'username' and 'password' keys with corresponding values.

    ### Return
    - tuple: The newly created user as a tuple (id, username, password).
    - str: Error message if an error occurs.

    ### Example
    userjson = {"username": "new_user", "password": "password123"}
    create_user(userjson)
    >>> (3, 'new_user', 'password123')

    ### Error Handling
    If there is an operational error (e.g., the database is not available), an error message is returned.
    """
    conn, cursor = get_connection(DATABASE)
    username = userjson["username"]
    password = userjson["password"]
    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (:username, :password)",
            {"username": username, "password": password}
        )
        conn.commit()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
    except sqlite3.OperationalError as e:
        return f"Error: Maybe the Database isn't available, Complete Error: {e}"
    finally:
        conn.close()
    return user

def get_courses() -> list[tuple]:
    """
    Retrieve all courses from the 'courses' table.

    ### Return
    A list of tuples, where each tuple contains:
    (idc, name, description, subscriptions, value, professor_id)

    ### Example
    get_courses()
    >>> [(1, 'Loren Ipsum', 'A Loren Ipsum course', 200, 120, 1),]

    ### Error Handling
    If the courses table is empty, an error message is returned.
    If there is an operational error (e.g., the table does not exist), an error message is returned.

    ### Returns
    - list of tuples: Each tuple contains course data.
    - str: Error message if an error occurs.
    """
    conn, cursor = get_connection(DATABASE)
    try:
        cursor.execute("SELECT * FROM courses")
        courses = cursor.fetchall()
        if not courses:
            return "Error: Courses Table is Empty"
    except sqlite3.OperationalError as e:
        return f"Error: This table may not exist, Complete Error: {e}"
    finally:
        conn.commit()
        conn.close()
    return courses

def get_course(id: int = None, name: str = None) -> tuple:
    """
    Retrieve a course from the 'courses' table by ID or name.

    ### Parameters
    - id (int): The ID of the course.
    - name (str): The name of the course.

    ### Return
    A tuple containing course data (idc, name, description, subscriptions, value, professor_id).

    ### Example
    get_course(1)
    >>> (1, 'Loren Ipsum', '...', 200, 120, 1)

    get_course(name='Loren Ipsum')
    >>> (1, 'Loren Ipsum', '...', 200, 120, 1)

    ### Error Handling
    If the course does not exist, an error message is returned.
    If there is an operational error (e.g., the table does not exist), an error message is returned.

    ### Returns
    - tuple: Course data (idc, name, description, subscriptions, value, professor_id).
    - str: Error message if an error occurs.
    """
    conn, cursor = get_connection(DATABASE)
    try:
        if id is not None:
            cursor.execute("SELECT * FROM courses WHERE idc = ?", (id,))
        elif name is not None:
            cursor.execute("SELECT * FROM courses WHERE name = ?", (name,))
        course = cursor.fetchone()
        if not course:
            return "Error: ID or Name did not exist"
    except sqlite3.OperationalError as e:
        return f"Error: Maybe the Database isn't available, Complete Error: {e}"
    finally:
        conn.commit()
        conn.close()
    return course

def create_course(coursejson: dict) -> tuple:
    """
    Create a new course in the 'courses' table and retrieve the newly created course.

    ### Parameters
    - coursejson (dict): A dictionary containing 'name', 'description', 'subscriptions', 'value', and 'professor_id' keys with corresponding values.

    ### Return
    - tuple: The newly created course as a tuple (idc, name, description, subscriptions, value, professor_id).
    - str: Error message if an error occurs.

    ### Example
    coursejson = {
        "name": "Math 101",
        "description": "Basic Mathematics",
        "subscriptions": 0,
        "value": 100,
        "professor_id": 1
    }
    create_course(coursejson)
    >>> (1, 'Math 101', 'Basic Mathematics', 0, 100, 1)

    ### Error Handling
    If there is an operational error (e.g., the database is not available), an error message is returned.
    """
    conn, cursor = get_connection(DATABASE)
    try:
        cursor.execute(
            "INSERT INTO courses (name, description, subscriptions, value, professor_id) VALUES (:name, :description, :subscriptions, :value, :professor_id)",
            {
                "name": coursejson["name"],
                "description": coursejson["description"],
                "subscriptions": coursejson["subscriptions"],
                "value": coursejson["value"],
                "professor_id": coursejson["professor_id"]
            }
        )
        conn.commit()
        cursor.execute("SELECT * FROM courses WHERE name = ? AND value = ?", (coursejson["name"], coursejson["value"]))
        course = cursor.fetchone()
    except sqlite3.OperationalError as e:
        return f"Error: Maybe the database isn't available, Complete Error: {e}"
    finally:
        conn.close()
    return course

def examples():
    print(f"Getter Unique: {get_user(1)}")
    print(f"General Getter: {get_users()}")
    print(f"Course Getter: {get_courses()}")
    print(f"Getting Course ID: {get_course(2)}")

