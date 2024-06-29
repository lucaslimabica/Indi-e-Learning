from flask import Flask, jsonify
import CREATEbase


app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!"

@app.route('/courses', methods=['GET'])
def get_courses():
    return "Your Courses!"

@app.route('/courses/<int:id>', methods=['GET'])
def get_courseById(id):
    return CREATEbase.get_user(id=id)

@app.route('/courses/<username>', methods=['GET'])
def get_courseByUsername(username):
    return CREATEbase.get_user(username=username)

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(CREATEbase.get_all_users())

@app.route('/users/<int:id>', methods=['GET'])
def get_userById(id):
    return CREATEbase.get_user(id=id)

@app.route('/users/<username>', methods=['GET'])
def get_userByUsername(username):
    return CREATEbase.get_user(username=username)

if __name__ == '__main__':
    app.run(port=443)