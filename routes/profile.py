from flask import Blueprint, request, jsonify
from database import get_db_connection

# Create Blueprint
profile_bp = Blueprint('profile', __name__)

# # PROFILE ENDPOINT
# @profile_bp.route('/auth/profile', methods=['GET'])
# def get_profile():
#     """
#     Fetch user profile using email
#     """

#     # Get email from query parameter
#     email = request.args.get('email')

#     # Check if email is provided
#     if not email:
#         return jsonify({
#             "message": "Email is required"
#         }), 400

#     # Connect to database
#     conn = get_db_connection()

#     # Fetch user details (excluding password)
#     user = conn.execute(
#         "SELECT id, name, email FROM users WHERE email = ?",
#         (email,)
#     ).fetchone()

#     # Close connection
#     conn.close()

#     # If user not found
#     if user is None:
#         return jsonify({
#             "message": "User not found"
#         }), 404

#     # Convert row to dictionary
#     user_data = dict(user)

#     # Return user profile
#     return jsonify(user_data), 200

@profile_bp.route('/auth/profile', methods=['POST'])
def get_profile():

    data = request.json
    email = data.get('email')

    if not email:
        return jsonify({"message": "Email is required"}), 400

    conn = get_db_connection()

    user = conn.execute(
        "SELECT id, name, email FROM users WHERE email = ?",
        (email,)
    ).fetchone()

    conn.close()

    if user is None:
        return jsonify({"message": "User not found"}), 404

    return jsonify(dict(user)), 200