# main.py 

# Standard library imports
import os
import io
from functools import wraps

# Third party imports
from flask import Flask, jsonify, request, g
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import jwt
from jwt import exceptions
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd

# Local application imports
# from app.models import User, Post
from app.config import Config

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)
CORS(app)  # This will enable CORS for all routes

# Initialize SQLAlchemy
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)  # description can be optional
    data = db.Column(db.Text, nullable=False)  # This will store the CSV data


def authenticate(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            print(request.headers['Authorization'])
            token = request.headers['Authorization'].split(" ")[1]
        
        print('Received token:', token)  # Debug

        if not token:
            return jsonify({'message': 'Token is missing.'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            print('Decoded token data:', data)  # Debug
            current_user = db.session.get(User, data['user_id'])
            if current_user is None:
                print('User not found for user_id:', data['user_id'])  # Debug
                return jsonify({'message': 'User not found.'}), 401
            print('Current user:', current_user)  # Debug
            g.current_user = current_user
        except exceptions.ExpiredSignatureError:
            print('Token has expired')  # Debug
            return jsonify({'message': 'Token has expired.'}), 401
        except exceptions.InvalidTokenError:
            print('Token is invalid')  # Debug
            return jsonify({'message': 'Token is invalid.'}), 401
        except Exception as e:
            print('Error decoding token:', str(e))  # Debug
            return jsonify({'message': 'Token is invalid.'}), 401

        return f(*args, **kwargs)

    return decorated_function

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    # Check if user exists and password is correct
    if user and check_password_hash(user.password, password):
        token = jwt.encode({'user_id': user.id}, app.config['SECRET_KEY'])
        return jsonify({'message': 'Login successful', 'token': token}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 400



@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Check if user already exists
    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'User already exists'}), 400

    # If not, create a new user
    hashed_password = generate_password_hash(password, method='scrypt')
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201





@app.route('/post', methods=['POST'])
@authenticate
def post():
    file = request.files['file']
    title = request.form.get('title')
    description = request.form.get('description')

    # make sure a file is provided
    if not file:
        return jsonify({'message': 'No file uploaded.'}), 400

    # make sure it's a CSV file
    if not file.filename.endswith('.csv'):
        return jsonify({'message': 'File type not supported. Please upload a CSV file.'}), 400

    filename = secure_filename(file.filename)
    file.save(os.path.join('uploads', filename))

    # read the CSV file and save raw data
    with open(os.path.join('uploads', filename), 'r') as f:
        csv_data = f.read()

    # save post to database
    new_post = Post(title=title, description=description, user_id=g.current_user.id, data=csv_data)
    db.session.add(new_post)
    db.session.commit()

    return jsonify({'message': 'File uploaded successfully'}), 201


@app.route('/posts', methods=['GET'])
@authenticate
def get_posts():
    posts = Post.query.filter_by(user_id=g.current_user.id).all()
    posts_json = [{'id': post.id, 'title': post.title} for post in posts]
    return jsonify(posts_json)


@app.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = db.session.get(Post, post_id)
    if post is None:
        return jsonify({'message': 'Post not found'}), 404

    csv_data = io.StringIO(post.data)
    df = pd.read_csv(csv_data)
    table_html = df.head().to_html()

    return jsonify({'tableHTML': table_html, 'title': post.title, 'description': post.description})

@app.route('/posts/<int:post_id>', methods=['DELETE'])
@authenticate
def delete_post(post_id):
    post = db.session.get(Post, post_id)
    if post is None:
        return jsonify({'message': 'Post not found'}), 404

    if post.user_id != g.current_user.id:
        return jsonify({'message': 'Not authorized to delete this post'}), 403

    db.session.delete(post)
    db.session.commit()

    return jsonify({'message': 'Post deleted successfully'}), 200



@app.route('/user', methods=['DELETE'])
@authenticate
def delete_user():
    # Get the current user
    user = g.current_user

    # Delete all posts of the user
    Post.query.filter_by(user_id=user.id).delete()

    # Delete the user
    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'User and all related posts deleted successfully'}), 200

@app.route('/search_user/<username>', methods=['GET'])
def search_user(username):
    # Use SQLAlchemy's ilike function to search for similar usernames
    users = User.query.filter(User.username.ilike(f"{username}%")).all()
    
    # Return a list of users
    users_json = [{'id': user.id, 'username': user.username} for user in users]
    return jsonify(users_json)




def init_db():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    init_db()
    app.run()