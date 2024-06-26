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

if __name__ == '__main__':
    app.run(port=443)