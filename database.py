from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base() # -> Returns a base class to me define declarative classes (tables)

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
    

engine = create_engine("sqlite:///database.db", echo=True) # Create a connection to the SQLite database
Base.metadata.create_all(bind=engine) # -> Creates the tables (only if they don't exist)

Session = sessionmaker(bind=engine)
session = Session()

user = User("john_doe", "password123")  # Create a new user
session.add(user)
session.commit()
