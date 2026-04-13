from flask import Blueprint, request, jsonify
from database import get_db_connection

# Create Blueprint
users_bp = Blueprint('users', __name__)

# 1. GET ALL USERS
@users_bp.route('/users', methods=['GET'])
def get_users():

    conn = get_db_connection()

    users = conn.execute(
        "SELECT id, name, email FROM users"
    ).fetchall()

    conn.close()

    # Convert list of rows to list of dictionaries
    users_list = [dict(user) for user in users]

    return jsonify(users_list), 200


# 2. GET SINGLE USER
@users_bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):

    conn = get_db_connection()

    user = conn.execute(
        "SELECT id, name, email FROM users WHERE id = ?",
        (id,)
    ).fetchone()

    conn.close()

    if user is None:
        return jsonify({"message": "User not found"}), 404

    return jsonify(dict(user)), 200


# 3. UPDATE USER
@users_bp.route('/users/<int:id>', methods=['PUT'])
def update_user(id):

    data = request.json
    name = data.get('name')
    email = data.get('email')

    if not name or not email:
        return jsonify({"message": "Name and email required"}), 400

    conn = get_db_connection()

    # Check if user exists
    user = conn.execute(
        "SELECT * FROM users WHERE id = ?",
        (id,)
    ).fetchone()

    if user is None:
        conn.close()
        return jsonify({"message": "User not found"}), 404

    # Update user
    conn.execute(
        "UPDATE users SET name = ?, email = ? WHERE id = ?",
        (name, email, id)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "User updated successfully"}), 200


# 4. DELETE USER
@users_bp.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):

    conn = get_db_connection()

    # Check if user exists
    user = conn.execute(
        "SELECT * FROM users WHERE id = ?",
        (id,)
    ).fetchone()

    if user is None:
        conn.close()
        return jsonify({"message": "User not found"}), 404

    # Delete user
    conn.execute(
        "DELETE FROM users WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "User deleted successfully"}), 200