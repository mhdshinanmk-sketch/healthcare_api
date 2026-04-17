from flask import request, jsonify
from functools import wraps
from utils.jwt_helper import verify_token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"message": "Token is missing"}), 401

        try:
            token = auth_header.split(" ")[1]
        except:
            return jsonify({"message": "Invalid token format"}), 401

        decoded = verify_token(token)

        if not decoded:
            return jsonify({"message": "Invalid or expired token"}), 401

        return f(*args, **kwargs)

    return decorated