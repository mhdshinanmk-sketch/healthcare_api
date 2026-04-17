from flask import Blueprint, request, jsonify
from database import get_db_connection
from utils.auth_middleware import token_required

appointments_bp = Blueprint('appointments', __name__)

# 1. CREATE APPOINTMENT
@appointments_bp.route('/appointments', methods=['POST'])
@token_required
def create_appointment():

    data = request.json

    patient_id = data.get('patient_id')
    doctor_name = data.get('doctor_name')
    date = data.get('date')
    time = data.get('time')

    if not patient_id or not doctor_name or not date or not time:
        return jsonify({"message": "Missing required fields"}), 400

    conn = get_db_connection()

    # Check if patient exists
    patient = conn.execute(
        "SELECT * FROM patients WHERE id = ?",
        (patient_id,)
    ).fetchone()

    if patient is None:
        conn.close()
        return jsonify({"message": "Patient not found"}), 404

    conn.execute(
        "INSERT INTO appointments (patient_id, doctor_name, date, time) VALUES (?, ?, ?, ?)",
        (patient_id, doctor_name, date, time)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Appointment created successfully"}), 201


# 2. GET ALL APPOINTMENTS
@appointments_bp.route('/appointments', methods=['GET'])
@token_required
def get_appointments():

    conn = get_db_connection()

    appointments = conn.execute(
        "SELECT * FROM appointments"
    ).fetchall()

    conn.close()

    return jsonify([dict(a) for a in appointments]), 200


# 3. GET APPOINTMENTS BY PATIENT
@appointments_bp.route('/appointments/patient/<int:id>', methods=['GET'])
@token_required
def get_appointments_by_patient(id):

    conn = get_db_connection()

    appointments = conn.execute(
        "SELECT * FROM appointments WHERE patient_id = ?",
        (id,)
    ).fetchall()

    conn.close()

    return jsonify([dict(a) for a in appointments]), 200


# 4. UPDATE APPOINTMENT STATUS
@appointments_bp.route('/appointments/<int:id>', methods=['PUT'])
@token_required
def update_appointment(id):

    data = request.json
    status = data.get('status')

    if not status:
        return jsonify({"message": "Status is required"}), 400

    conn = get_db_connection()

    appointment = conn.execute(
        "SELECT * FROM appointments WHERE id = ?",
        (id,)
    ).fetchone()

    if appointment is None:
        conn.close()
        return jsonify({"message": "Appointment not found"}), 404

    conn.execute(
        "UPDATE appointments SET status = ? WHERE id = ?",
        (status, id)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Appointment updated"}), 200


# 5. DELETE APPOINTMENT
@appointments_bp.route('/appointments/<int:id>', methods=['DELETE'])
@token_required
def delete_appointment(id):

    conn = get_db_connection()

    appointment = conn.execute(
        "SELECT * FROM appointments WHERE id = ?",
        (id,)
    ).fetchone()

    if appointment is None:
        conn.close()
        return jsonify({"message": "Appointment not found"}), 404

    conn.execute(
        "DELETE FROM appointments WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Appointment deleted"}), 200