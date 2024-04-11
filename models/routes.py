from flask import request, jsonify, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User, Job

bp = Blueprint('main', __name__)

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Simple validation
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Missing data'}), 400

    # Check if user exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'User already exists'}), 400

    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = User(username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Registered successfully'}), 201

@bp.route('/login', methods=['POST'])
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return jsonify({'message': 'Could not verify'}), 401

    user = User.query.filter_by(username=auth.username).first()

    if not user:
        return jsonify({'message': 'User not found'}), 401

    if check_password_hash(user.password, auth.password):
        # This is where you'd return a token in a real app
        return jsonify({'message': 'Login successful'}), 200

    return jsonify({'message': 'Wrong password'}), 403

@bp.route('/jobs', methods=['POST'])
def create_job():
    data = request.get_json()
    
    # Example simple validation
    if not data or not data.get('title') or not data.get('description'):
        return jsonify({'message': 'Missing data'}), 400

    # In a real app, associate job with logged in user
    new_job = Job(title=data['title'], description=data['description'])
    db.session.add(new_job)
    db.session.commit()

    return jsonify({'message': 'Job created successfully'}), 201

@bp.route('/jobs', methods=['GET'])
def get_jobs():
    jobs = Job.query.all()
    output = []
    for job in jobs:
        job_data = {'title': job.title, 'description': job.description}
        output.append(job_data)
    
    return jsonify({'jobs': output}), 200

