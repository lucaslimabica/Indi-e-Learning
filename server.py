from flask import Flask
import database

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!"

@app.route('/courses', methods=['GET'])
def get_courses():
    return "Your Courses!"

@app.route('/users', methods=['GET'])
def get_users():
    return database.get_users()

@app.route('/users/<int:id>', methods=['GET'])
def get_userById(id):
    return database.get_user(id=id)

@app.route('/users/<username>', methods=['GET'])
def get_userByUsername(username):
    return database.get_user(username=username)

if __name__ == '__main__':
    app.run(port=443)