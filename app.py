from flask import Flask
from database import init_db
from routes.auth import auth_bp
from routes.login import login_bp
# Create Flask application
app = Flask(__name__)

# Register the authentication Blueprint
# This makes all routes from auth.py available in our app
app.register_blueprint(auth_bp)
app.register_blueprint(login_bp)
@app.route('/')
def home():
    return "Healthcare API is running!"

if __name__ == '__main__':
    # Initialize the database (create tables if they don't exist)
    init_db()

    # Run the Flask development server
    # debug=True enables auto-reload and detailed error messages
    app.run(debug=True)