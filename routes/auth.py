from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db_connection
import sqlite3

# Create a Blueprint for authentication routes
# This helps organize routes into separate modules
auth_bp = Blueprint('auth', __name__)

# REGISTER ENDPOINT
@auth_bp.route('/auth/register', methods=['POST'])
def register():
    """
    Register a new user.
    Expects JSON data: {"name": "John Doe", "email": "john@example.com", "password": "securepass123"}
    """
    # Get JSON data from the request body
    data = request.get_json()

    # Validate that all required fields are present
    if not data or not data.get('name') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Name, email, and password are required'}), 400

    name = data['name']
    email = data['email']
    password = data['password']

    # Hash the password for security (never store plain text passwords!)
    # generate_password_hash creates a secure hash that we can store safely
    # Using 'pbkdf2:sha256' method for compatibility with Python 3.9
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    try:
        # Connect to the database
        conn = get_db_connection()

        # Insert the new user into the database
        conn.execute(
            'INSERT INTO users (name, email, password) VALUES (?, ?, ?)',
            (name, email, hashed_password)
        )
        conn.commit()  # Save changes
        conn.close()   # Close connection

        # Return success response
        return jsonify({
            'message': 'User registered successfully!',
            'user': {
                'name': name,
                'email': email
            }
        }), 201  # 201 means "Created"

    except sqlite3.IntegrityError:
        # This happens when the email already exists (UNIQUE constraint violation)
        return jsonify({'error': 'Email already exists'}), 409  # 409 means "Conflict"

    except Exception as e:
        # Catch any other errors
        return jsonify({'error': 'Registration failed', 'details': str(e)}), 500


# LOGIN ENDPOINT
@auth_bp.route('/auth/login', methods=['POST'])
def login():
    """
    Login an existing user.
    Expects JSON data: {"email": "john@example.com", "password": "securepass123"}
    """
    # Get JSON data from the request body
    data = request.get_json()

    # Validate that all required fields are present
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password are required'}), 400

    email = data['email']
    password = data['password']

    # Connect to the database
    conn = get_db_connection()

    # Find the user by email
    user = conn.execute(
        'SELECT * FROM users WHERE email = ?',
        (email,)
    ).fetchone()  # fetchone() returns one row or None if not found

    conn.close()

    # Check if user exists
    if user is None:
        return jsonify({'error': 'Invalid email or password'}), 401  # 401 means "Unauthorized"

    # Check if password matches
    # check_password_hash compares the plain password with the hashed password
    if not check_password_hash(user['password'], password):
        return jsonify({'error': 'Invalid email or password'}), 401

    # If everything is correct, return success response
    return jsonify({
        'message': 'Login successful!',
        'user': {
            'id': user['id'],
            'name': user['name'],
            'email': user['email']
        }
    }), 200  # 200 means "OK"
