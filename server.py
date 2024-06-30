from flask import Flask #, jsonify
import CRUDbaseL


app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!"

# @app.route('/courses', methods=['GET'])
# def get_courses():
#     pass
#     #return "Your Courses!"
# 
# @app.route('/courses/<int:id>', methods=['GET'])
# def get_courseById(id):
#     pass
#     #return CRUDbaseL.get_user(id=id)

@app.route('/courses/<username>', methods=['GET'])
def get_courseByUsername(username):
    pass
    #return CRUDbaseL.get_user(username=username)

@app.route('/users', methods=['GET'])
def get_users():    
    return CRUDbaseL.get_users()

@app.route('/users/<int:id>', methods=['GET'])
def get_userById(id):
    pass
    #return CRUDbaseL.get_user(id=id)

@app.route('/users/<username>', methods=['GET'])
def get_userByUsername(username):
    pass
    #return CRUDbaseL.get_user(username=username)

if __name__ == '__main__':
    app.run(port=443)