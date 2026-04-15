import sqlite3

# Function to get a database connection
def get_db_connection():
    """
    Creates and returns a connection to the SQLite database.
    The database file will be named 'healthcare.db'
    """
    conn = sqlite3.connect('healthcare.db')
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn


# Function to initialize the database and create tables
def init_db():
    """
    Creates the required tables if they do not exist.

    Tables:

    1. users
        - id: unique identifier (auto-increment)
        - name: user's full name
        - email: unique email
        - password: hashed password

    2. patients
        - id: unique identifier (auto-increment)
        - name: patient name
        - age: patient age
        - gender: patient gender
        - phone: contact number (optional)
        - disease: current illness
        - created_at: timestamp when record created
    """

    conn = get_db_connection()

    # Create users table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # Create patients table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            phone TEXT,
            disease TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Save changes
    conn.commit()

    # Close connection
    conn.close()

    print("Database initialized successfully!")


# Run this file directly to initialize database
if __name__ == '__main__':
    init_db()