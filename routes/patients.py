from flask import Blueprint, request, jsonify
from database import get_db_connection
from utils.auth_middleware import token_required
# Create Blueprint
patients_bp = Blueprint('patients', __name__)

# 1. ADD PATIENT
@patients_bp.route('/patients', methods=['POST'])
@token_required
def add_patient():

    data = request.json

    name = data.get('name')
    age = data.get('age')
    gender = data.get('gender')
    phone = data.get('phone')
    disease = data.get('disease')

    if not name or not age or not gender or not disease:
        return jsonify({"message": "Missing required fields"}), 400

    conn = get_db_connection()

    conn.execute(
        "INSERT INTO patients (name, age, gender, phone, disease) VALUES (?, ?, ?, ?, ?)",
        (name, age, gender, phone, disease)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Patient added successfully"}), 201


# 2. GET ALL PATIENTS
@patients_bp.route('/patients', methods=['GET'])
@token_required
def get_patients():

    conn = get_db_connection()

    patients = conn.execute(
        "SELECT * FROM patients"
    ).fetchall()

    conn.close()

    patients_list = [dict(patient) for patient in patients]

    return jsonify(patients_list), 200


# 3. GET SINGLE PATIENT
@patients_bp.route('/patients/<int:id>', methods=['GET'])
@token_required
def get_patient(id):

    conn = get_db_connection()

    patient = conn.execute(
        "SELECT * FROM patients WHERE id = ?",
        (id,)
    ).fetchone()

    conn.close()

    if patient is None:
        return jsonify({"message": "Patient not found"}), 404

    return jsonify(dict(patient)), 200


# 4. UPDATE PATIENT
@patients_bp.route('/patients/<int:id>', methods=['PUT'])
@token_required
def update_patient(id):
    data = request.json

    conn = get_db_connection()

    patient = conn.execute(
        "SELECT * FROM patients WHERE id = ?",
        (id,)
    ).fetchone()

    if patient is None:
        conn.close()
        return jsonify({"message": "Patient not found"}), 404

    # Keep old values if not provided
    name = data.get('name', patient['name'])
    age = data.get('age', patient['age'])
    gender = data.get('gender', patient['gender'])
    phone = data.get('phone', patient['phone'])
    disease = data.get('disease', patient['disease'])

    conn.execute(
        "UPDATE patients SET name=?, age=?, gender=?, phone=?, disease=? WHERE id=?",
        (name, age, gender, phone, disease, id)
    )

    conn.commit()
    conn.close()

    # data = request.json

    # name = data.get('name')
    # age = data.get('age')
    # gender = data.get('gender')
    # phone = data.get('phone')
    # disease = data.get('disease')

    # conn = get_db_connection()

    # patient = conn.execute(
    #     "SELECT * FROM patients WHERE id = ?",
    #     (id,)
    # ).fetchone()

    # if patient is None:
    #     conn.close()
    #     return jsonify({"message": "Patient not found"}), 404

    # conn.execute(
    #     "UPDATE patients SET name=?, age=?, gender=?, phone=?, disease=? WHERE id=?",
    #     (name, age, gender, phone, disease, id)
    # )

    # conn.commit()
    # conn.close()

    return jsonify({"message": "Patient updated successfully"}), 200


# 5. DELETE PATIENT
@patients_bp.route('/patients/<int:id>', methods=['DELETE'])
@token_required
def delete_patient(id):

    conn = get_db_connection()

    patient = conn.execute(
        "SELECT * FROM patients WHERE id = ?",
        (id,)
    ).fetchone()

    if patient is None:
        conn.close()
        return jsonify({"message": "Patient not found"}), 404

    conn.execute(
        "DELETE FROM patients WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Patient deleted successfully"}), 200