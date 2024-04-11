from flask import Flask, jsonify, request
from models import db, User, Task
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movers.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        return user

@app.route('/api/users', methods=['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        return jsonify({'message': 'Missing arguments'}), 400
    if User.query.filter_by(username=username).first() is not None:
        return jsonify({'message': 'User already exists'}), 400
    user = User(username=username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'username': user.username}), 201, {'Location': f'/api/users/{user.id}'}

@app.route('/api/tasks', methods=['GET'])
@auth.login_required
def get_tasks():
    tasks = Task.query.all()
    return jsonify({'tasks': [task.to_json() for task in tasks]})

if __name__ == '__main__':
    app.run(debug=True)

