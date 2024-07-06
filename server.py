from flask import Flask, jsonify, request
import CRUDbaseL
import json

app = Flask(__name__)

STR_SUCESS = "Sucess: True, data: "
STR_ERROR = "Sucess: False, error: "

def validate_json(json_string, required_keys) -> bool:
    """
    Valida o JSON assegurando que nele estão todas as necessárias chaves.

    Args:
        json_string (str): O JSON como uma string.
        required_keys (list): Array de todas as chaves do JSON.

    Returns:
        bool: True se todas as chaves necessárias estão presentes, caso contrário, False.
    """
    try:
        # JSON string -> dict
        data = json.loads(json_string)
    except:  # noqa: E722
        return False

    # Verify if do all required keys are in the json 
    for key in required_keys:
        if key not in data:
            return False

    return True

@app.route('/')
def home():
    return "Hello, World!"

@app.route('/users', methods=['GET'])
def get_users():
    data = CRUDbaseL.get_users()
    
    if isinstance(data, str) and data.startswith("Error"):
        return jsonify({"error": data}), 500
    
    return jsonify({"Sucess": "True", "Data": data}), 200


@app.route('/users', methods=['POST'])
def create_users():
    json = request.get_json()
    if validate_json(json, ["username", "password"]):
        sucess, data = CRUDbaseL.create_user(json)
        if sucess:
            return 201, jsonify(STR_SUCESS + data)
        else:
            return jsonify(STR_ERROR + data)
    return 400, jsonify(f"{STR_ERROR} Invalide JSON String")

@app.route('/users/<int:id>', methods=['GET'])
def get_userById(id):
    sucess, data = CRUDbaseL.get_user(id=id)
    if sucess:
        return 200, jsonify(f"{STR_SUCESS} {data}")
    else:
        return jsonify(f"{STR_ERROR} {data}")

@app.route('/users/<username>', methods=['GET'])
def get_userByUsername(username):
    sucess, data = CRUDbaseL.get_user(username=username)
    if sucess:
        return 200, jsonify(f"{STR_SUCESS} {data}")
    else:
        return jsonify(f"{STR_ERROR} {data}")

@app.route('/courses', methods=['GET'])
def get_courses():
    pass

@app.route('/courses/<username>', methods=['GET'])
def get_courseByUsername(username):
    pass

if __name__ == '__main__':
    app.run(port=443)