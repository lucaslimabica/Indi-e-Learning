from flask import Flask, jsonify
import CRUDbaseL


app = Flask(__name__)

STR_SUCESS = "Sucess: True, data: "
STR_ERROR = "Sucess: False, error: "

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
    sucess, data = CRUDbaseL.get_users()
    if sucess:
        return jsonify(STR_SUCESS + data)
    else:
        return jsonify(STR_ERROR + data)


@app.route('/users/<int:id>', methods=['GET'])
def get_userById(id):
    sucess, data = CRUDbaseL.get_user(id=id)
    if sucess:
        return jsonify(STR_SUCESS + data)
    else:
        return jsonify(STR_ERROR + data)

@app.route('/users/<username>', methods=['GET'])
def get_userByUsername(username):
    sucess, data = CRUDbaseL.get_user(username=username)
    if sucess:
        return jsonify(STR_SUCESS + data)
    else:
        return jsonify(STR_ERROR + data)

if __name__ == '__main__':
    app.run(port=443)