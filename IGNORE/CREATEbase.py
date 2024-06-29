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
        return f"(id={self.id}, username={self.username}, password={self.password}, creation_data={self.creation_date})"

    def get_json(self) -> str:
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

    def __init__(self, name, user, courses_list="[]", area="Technical Engineering"):
        self.name = name
        self.user = user  # The User Object
        self.area = area
        self.courses_list = courses_list if courses_list else "[]"

    def __repr__(self) -> str:
        return f"<Professor(id={self.id}, username='{self.name}', creation_date='{self.creation_date}', list_of_courses='{self.courses_list}')>"

    def get_json(self) -> str:
        return json.dumps({
            'id': self.id,
            'name': self.name,
            'area': self.area,
            'creation_date': self.creation_date,
            'list_of_courses': self.courses_list,
            'user_id': self.user_id
        }, indent=2)

    def get_courses_json(self) -> str:
        return json.dumps(self.courses_list, indent=4)

    def get_courses(self) -> list:
        try:
            return self.courses_list.split()
        except AttributeError:
            return [""]

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

def get_all_users():
    return session.query(User).all()


############### EXEMPLES #################

# user1 = session.query(User).filter_by(username="benObiw").first()
# session.commit()

# professor1 = session.query(Professor).filter_by(name="Master Kenobi").first()
# session.add(professor1)
# session.commit()
# 
# course1 = Course(name="Rules 101", professor=professor1, description="Learn how to follow the rules")
# course2 = Course(name="Negotiation", professor=professor1, description="The Best Confflict is the Confflict You Don't Fight")
# session.add_all([course1, course2])
# session.commit()
# 
# courses = session.query(Course).all()
# courses_names = [course.name for course in courses]
# 
# for course in courses_names:
#     professor1.courses_list = professor1.get_courses().append(course)
#     session.commit()

# print(session.query(User).all())
# print(session.query(Professor).all())
# print(session.query(Course).all())