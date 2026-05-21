from flask import Flask
from flask_cors import CORS
from database import init_db
from routes.auth import auth_bp
from routes.login import login_bp
from routes.profile import profile_bp
from routes.users import users_bp
from routes.patients import patients_bp
from routes.appointments import appointments_bp
from routes.doctors import doctors_bp

# Create Flask application
app = Flask(__name__)

# Register the authentication Blueprint
# This makes all routes from auth.py available in our app
app.register_blueprint(auth_bp)
app.register_blueprint(login_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(users_bp)
app.register_blueprint(patients_bp)
app.register_blueprint(appointments_bp)
app.register_blueprint(doctors_bp)

# Apply CORS AFTER blueprints with proper config
CORS(app, resources={r"/*": {"origins": "*", "allow_headers": "*", "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"]}})

@app.route('/')
def home():
    return "Healthcare API is running!"

# Add CORS headers to all responses
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
    return response

if __name__ == '__main__':
    # Initialize the database (create tables if they don't exist)
    init_db()

    # Run the Flask development server
    # debug=True enables auto-reload and detailed error messages
    app.run(debug=True)