from flask import Blueprint, request, jsonify
from database import get_db_connection
from utils.auth_middleware import token_required
import sqlite3

# Create Blueprint
doctors_bp = Blueprint('doctors', __name__)

# 1. ADD DOCTOR
@doctors_bp.route('/doctors', methods=['POST'])
@token_required
def add_doctor():

    data = request.json

    name = data.get('name')
    specialization = data.get('specialization')
    phone = data.get('phone')
    email = data.get('email')

    # Validation
    if not name or not specialization:
        return jsonify({"message": "Name and specialization required"}), 400

    conn = get_db_connection()

    try:
        conn.execute(
            "INSERT INTO doctors (name, specialization, phone, email) VALUES (?, ?, ?, ?)",
            (name, specialization, phone, email)
        )
        conn.commit()

        return jsonify({"message": "Doctor added successfully"}), 201

    except sqlite3.IntegrityError:
        return jsonify({"message": "Email already exists"}), 400

    finally:
        conn.close()


# 2. GET ALL DOCTORS
@doctors_bp.route('/doctors', methods=['GET'])
@token_required
def get_doctors():

    conn = get_db_connection()

    try:
        doctors = conn.execute(
            "SELECT * FROM doctors"
        ).fetchall()

        return jsonify([dict(d) for d in doctors]), 200

    finally:
        conn.close()


# 3. GET SINGLE DOCTOR
@doctors_bp.route('/doctors/<int:id>', methods=['GET'])
@token_required
def get_doctor(id):

    conn = get_db_connection()

    try:
        doctor = conn.execute(
            "SELECT * FROM doctors WHERE id = ?",
            (id,)
        ).fetchone()

        if doctor is None:
            return jsonify({"message": "Doctor not found"}), 404

        return jsonify(dict(doctor)), 200

    finally:
        conn.close()


# # 4. UPDATE DOCTOR
# @doctors_bp.route('/doctors/<int:id>', methods=['PUT'])
# @token_required
# def update_doctor(id):

#     data = request.json

#     name = data.get('name')
#     specialization = data.get('specialization')
#     phone = data.get('phone')
#     email = data.get('email')

#     conn = get_db_connection()

#     try:
#         doctor = conn.execute(
#             "SELECT * FROM doctors WHERE id = ?",
#             (id,)
#         ).fetchone()

#         if doctor is None:
#             return jsonify({"message": "Doctor not found"}), 404

#         conn.execute(
#             "UPDATE doctors SET name=?, specialization=?, phone=?, email=? WHERE id=?",
#             (name, specialization, phone, email, id)
#         )

#         conn.commit()

#         return jsonify({"message": "Doctor updated successfully"}), 200

#     except sqlite3.IntegrityError:
#         return jsonify({"message": "Email already exists"}), 400

#     finally:
#         conn.close

@doctors_bp.route('/doctors/<int:id>', methods=['PUT'])
@token_required
def update_doctor(id):

    data = request.json

    conn = get_db_connection()

    try:
        # Step 1: Get existing doctor
        doctor = conn.execute(
            "SELECT * FROM doctors WHERE id = ?",
            (id,)
        ).fetchone()

        if doctor is None:
            return jsonify({"message": "Doctor not found"}), 404

        # Step 2: Use old values if not provided
        name = data.get('name', doctor['name'])
        specialization = data.get('specialization', doctor['specialization'])
        phone = data.get('phone', doctor['phone'])
        email = data.get('email', doctor['email'])

        # Step 3: Update
        conn.execute(
            "UPDATE doctors SET name=?, specialization=?, phone=?, email=? WHERE id=?",
            (name, specialization, phone, email, id)
        )

        conn.commit()

        return jsonify({"message": "Doctor updated successfully"}), 200

    except sqlite3.IntegrityError:
        return jsonify({"message": "Email already exists"}), 400

    finally:
        conn.close()

# 5. DELETE DOCTOR
@doctors_bp.route('/doctors/<int:id>', methods=['DELETE'])
@token_required
def delete_doctor(id):

    conn = get_db_connection()

    try:
        doctor = conn.execute(
            "SELECT * FROM doctors WHERE id = ?",
            (id,)
        ).fetchone()

        if doctor is None:
            return jsonify({"message": "Doctor not found"}), 404

        conn.execute(
            "DELETE FROM doctors WHERE id = ?",
            (id,)
        )

        conn.commit()

        return jsonify({"message": "Doctor deleted successfully"}), 200

    finally:
        conn.close()