from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import json

Base = declarative_base()  # Returns a base class to define declarative classes (tables)

class Professor(Base):
    __tablename__ = 'professors'

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String, nullable=False)
    creation_date = Column("creation_date", DateTime, default=datetime.now)
    courses_list = Column("courses_list", String, nullable=True)
    user_id = Column("user_id", ForeignKey('users.id'), nullable=False)
    user_login = Column("user_login", nullable=False)
    user_password = Column("user_password", nullable=False)
    user = relationship("User", back_populates="professors")

    def __init__(self, name, user, courses_list=None):
        self.name = name
        self.user = user
        self.user_login = user.id
        self.user_password = user.password
        self.courses_list = json.dumps(courses_list) if courses_list else json.dumps([]) # -> JSON of the list

    def __repr__(self):
        return f"<Professor(id={self.id}, username='{self.name}', creation_date='{self.creation_date}', list_of_courses='{self.courses_list}')>"

class Course(Base):
    __tablename__ = 'courses'

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String, nullable=False)
    description = Column("description", String, nullable=True)
    creation_date = Column("creation_date", DateTime, default=datetime.now)
    subscribers = Column("subscribers", Integer, default=0)
    professor_id = Column(Integer, ForeignKey('professors.id'), nullable=True)
    professor = relationship("Professor", back_populates="courses_list")

    def __init__(self, name, description=None, professor=None):
        self.name = name
        self.description = description
        self.professor = professor
        self.subscribers = 0

class User(Base):
    __tablename__ = 'users'

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    username = Column("username", String, unique=True, nullable=False)
    password = Column("password", String, nullable=False)
    creation_date = Column("creation_date", DateTime, default=datetime.now)

    # Table Creation
    def __init__(self, username, password):
        self.username = username
        self.password = password

    # Method to check info about the user (like the __str__ method)
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', password='{self.password}', creation_date='{self.creation_date}')>"

class Document(Base):
    __tablename__ = 'documents'

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String, nullable=False)
    user_owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    expiration_date = Column("expiration_date", DateTime, nullable=True)
    owner = relationship("User", back_populates="documents")

    # Table Creation
    def __init__(self, name, owner, expiration_date=None):
        self.name = name
        self.owner = owner
        self.expiration_date = expiration_date

    # Method to check info about the document (like the __str__ method)
    def __repr__(self):
        return f"<Document(id={self.id}, name='{self.name}', owner='{self.owner.username}', expiration_date='{self.expiration_date}')>"

# Add the relationship from the User side
User.documents = relationship("Document", order_by=Document.id, back_populates="owner")

engine = create_engine("sqlite:///database.db", echo=True)  # Create a connection to the SQLite database
Base.metadata.create_all(bind=engine)  # Creates the tables (only if they don't exist)

Session = sessionmaker(bind=engine)
session = Session()

# Check if 'admin' user exists before adding
if not session.query(User).filter_by(username='admin').first():
    admin_user = User("admin", "87654321")
    session.add(admin_user)
    session.commit()

# Fetch all users
# users_list = session.query(User).all()
# for user in users_list:
#     print(user)

# if users_list:
#     drivers_license = Document("Drivers License", users_list[0])
#     session.add(drivers_license)
#     session.commit()

# not_secured_users = session.query(User).filter(User.password == '87654321').all()
# for user in not_secured_users:  # User's type = class User
#     print(f"{user.username} hasn't a secure password.")

# new_user = User("suporte", "87654321")  # Create a new user
# session.add(new_user)  # Add the new user to the session
# session.commit()  # Commit the changes to the database

# Print the admin's password
# admin_user = session.query(User).filter_by(username='admin').first()
# if admin_user:
#     print(f"The admin password is {admin_user.password}")
# 
# # Print the name of the document owned by the admin
# admin_document = session.query(Document).filter_by(user_owner_id=admin_user.id).first()
# if admin_document:
#     print(f"The admin document is {admin_document.name}")

def get_users():
    Session = sessionmaker(bind=engine)
    session = Session()
    
    users = session.query(User).all()
    users_dict = [
        {
            "id": user.id,
            "username": user.username,
            "password": user.password,
            "creation_date": user.creation_date.isoformat()
        }
        for user in users
    ]
    
    users_json = json.dumps(users_dict, indent=4)
    return users_json

def get_user(id=None, username: str=None):
    try:
        if id or username:
            Session = sessionmaker(bind=engine)
            session = Session()

            if id:
                user = session.query(User).filter(User.id == id).first()
            else:
                user = session.query(User).filter(User.username == username).first()
            user_dict = {
                "id": user.id,
                "username": user.username,
                "password": user.password,
                "creation_date": user.creation_date.isoformat()
            }

            user_json = json.dumps(user_dict, indent=4)
            return user_json
    except AttributeError as e:
        # The object has no attribute 'id' or 'username'
        return json.dumps({"Sucess": "False", "Error Type": "Object hasnt a solicited attribute or maybe it doest exist", "Data": {"error": str(e)}}, indent=4)
    finally:
        session.close()
