from flask import Flask
import IGNORE.draftsSQLAlchemy as draftsSQLAlchemy

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!"

@app.route('/courses', methods=['GET'])
def get_courses():
    return "Your Courses!"

@app.route('/courses/<int:id>', methods=['GET'])
def get_courseById(id):
    return draftsSQLAlchemy.get_user(id=id)

@app.route('/courses/<username>', methods=['GET'])
def get_courseByUsername(username):
    return draftsSQLAlchemy.get_user(username=username)

@app.route('/users', methods=['GET'])
def get_users():
    return draftsSQLAlchemy.get_users()

@app.route('/users/<int:id>', methods=['GET'])
def get_userById(id):
    return draftsSQLAlchemy.get_user(id=id)

@app.route('/users/<username>', methods=['GET'])
def get_userByUsername(username):
    return draftsSQLAlchemy.get_user(username=username)

if __name__ == '__main__':
    app.run(port=443)