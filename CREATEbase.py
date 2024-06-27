from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import json

Base = declarative_base()  # Returns a base class to define declarative classes (tables)

class User(Base):
    __tablename__ = 'users'

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    username = Column("username", String, unique=True, nullable=False)
    password = Column("password", String, nullable=False)
    creation_date = Column("creation_date", DateTime, default=datetime.now)

    # Relantionships with other tables
    professors = relationship("Professor", back_populates="user")

    # Method to check info about the user (like the __str__ method)
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', password='{self.password}', creation_date='{self.creation_date}')>"

    def get_json(self):
        return json.dumps({
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'creation_date': self.creation_date,
            'professors': [professor.get_json() for professor in self.professors]
        })

class Professor(Base):
    __tablename__ = 'professors'

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String, nullable=False)
    area = Column("area", String, nullable=False)
    creation_date = Column("creation_date", DateTime, default=datetime.now)
    courses_list = Column("courses_list", String, nullable=True)
    user_id = Column("user_id", ForeignKey('users.id'), nullable=False)

    # Relantionships
    user = relationship("User", back_populates="professors")
    courses = relationship("Course", back_populates="professor")

    def __init__(self, name, user, courses_list=None, area="Technical Engineering"):
        self.name = name
        self.user = user  # The User Object
        self.area = area
        self.courses_list = json.dumps(courses_list, indent=2) if courses_list else json.dumps([])  # -> JSON of the list

    def __repr__(self):
        return f"<Professor(id={self.id}, username='{self.name}', creation_date='{self.creation_date}', list_of_courses='{self.courses_list}')>"

    def get_json(self):
        return json.dumps({
            'id': self.id,
            'name': self.name,
            'area': self.area,
            'creation_date': self.creation_date,
            'list_of_courses': self.courses_list,
            'user_id': self.user_id
        }, indent=2)

    def get_courses_json(self):
        return self.courses_list

    def get_courses(self):
        return json.loads(self.courses_list)  # Convert JSON back to list


class Course(Base):
    __tablename__ = 'courses'

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String, nullable=False)
    description = Column("description", String, nullable=True)
    creation_date = Column("creation_date", DateTime, default=datetime.now)
    subscribers = Column("subscribers", Integer, default=0)
    professor_id = Column(Integer, ForeignKey('professors.id'), nullable=True)

    # Relantionships
    professor = relationship("Professor", back_populates="courses")

    def __init__(self, name, description="Hello There!", professor=None):
        self.name = name
        self.description = description
        self.professor = professor  # The Professor Object
        self.subscribers = 0

        self.professor.courses_list.append(self.name)
    
    def get_json(self):
        return json.dumps({
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'creation_date': self.creation_date,
            'subscribers': self.subscribers,
            'professor_id': self.professor_id
        }, indent=2)

    def __repr__(self):
        return f"<Course(id={self.id}, name='{self.name}', description='{self.description}', creation_date='{self.creation_date}', subscribers={self.subscribers})>"

engine = create_engine("sqlite:///database2.db", echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()