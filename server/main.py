# main.py 

# Standard library imports
import os
import io
from functools import wraps

# Third party imports
from flask import Flask, jsonify, request, g, url_for
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import jwt
from jwt import exceptions
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd

#  application imports
# from app.models import User, Post
from app.config import Config

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

CORS(app)  # This will enable CORS for all routes

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Association table
association_table = db.Table('association_table', 
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    # New fields
    name = db.Column(db.String(120), nullable=False)  # This will store the user's full name
    bio = db.Column(db.String(500), nullable=True)  # This will store the user's bio
    profile_photo = db.Column(db.String(500), nullable=True)  # This will store the URL of the profile photo
    # Associates and associations fields (representing 'following' and 'followers')
    associates = db.relationship('User', secondary=association_table, 
                                primaryjoin=(association_table.c.follower_id == id), 
                                secondaryjoin=(association_table.c.followed_id == id),
                                backref=db.backref('associations', lazy='dynamic'), 
                                lazy='dynamic')
    # Posts relationship
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

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    # Check if user exists and password is correct
    if user and check_password_hash(user.password, password):
        token = jwt.encode({'user_id': user.id}, app.config['SECRET_KEY'], algorithm="HS256")
        return jsonify({'message': 'Login successful', 'token': token}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 400


@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    name = data.get('name')

    # Check if user already exists
    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'User already exists'}), 400

    # If not, create a new user
    hashed_password = generate_password_hash(password, method='scrypt')
    
    # Set default profile photo path
    default_profile_photo_path = url_for('static', filename='default_profile_img.png')
    
    new_user = User(username=username, password=hashed_password, name=name, profile_photo=default_profile_photo_path)
    
    db.session.add(new_user)
    db.session.commit()

    # Generate JWT token for the new user
    token = jwt.encode({'user_id': new_user.id}, app.config['SECRET_KEY'], algorithm="HS256")

    return jsonify({'message': 'User created successfully', 'user_id': new_user.id, 'token': token}), 201




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

@app.route('/user/<username>', methods=['GET'])
def get_user_profile(username):
    # Fetch user from the database
    user = User.query.filter_by(username=username).first()

    # If user doesn't exist, return an error
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Return user profile information as JSON
    user_json = {
        'id': user.id, 
        'username': user.username,
        'name': user.name,
        'bio': user.bio, 
        'profile_photo': user.profile_photo
    }
    return jsonify(user_json)


@app.route('/upload_photo', methods=['POST'])
@authenticate
def upload_photo():
    # Check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    file = request.files['file']

    # If user does not select file, the browser might
    # submit an empty part without a filename.
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        # Secure the filename and save it
        filename = secure_filename(file.filename)

        # Create a directory for the user if it doesn't exist
        user_dir = os.path.join(app.config['UPLOAD_FOLDER'], str(g.current_user.id))
        os.makedirs(user_dir, exist_ok=True)
        
        filepath = os.path.join(user_dir, filename)
        file.save(filepath)

        # Update user's profile photo
        g.current_user.profile_photo = filepath
        db.session.commit()

        return jsonify({'message': 'Profile photo updated successfully'}), 200

    return jsonify({'message': 'Allowed file types are png, jpg, jpeg,'}), 400


def init_db():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    init_db()
    app.run()