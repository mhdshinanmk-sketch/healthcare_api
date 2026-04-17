from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from database import get_db_connection
from utils.jwt_helper import generate_token

# Create Blueprint
login_bp = Blueprint('login', __name__)

# LOGIN ROUTE
@login_bp.route('/auth/login', methods=['POST'])
def login():

    data = request.json

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"message": "Email and password required"}), 400

    conn = get_db_connection()

    user = conn.execute(
        "SELECT * FROM users WHERE email = ?",

        (email,)
    ).fetchone()

    conn.close()

    if user is None:
        return jsonify({"message": "User not found"}), 404

    if not check_password_hash(user["password"], password):
        return jsonify({"message": "Invalid password"}), 401
    token = generate_token(user)

    return jsonify({
        "message": "Login successful",
        "token": token,
         "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"]
        }

    }), 200

 