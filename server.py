from flask import Flask
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!"

@app.route('/courses', methods=['GET'])
def get_courses():
    return "Your Courses!"

if __name__ == '__main__':
    app.run(port=443)