import sqlite3

# Function to get a database connection
def get_db_connection():
    """
    Creates and returns a connection to the SQLite database.
    The database file will be named 'healthcare.db'
    """
    conn = sqlite3.connect('healthcare.db')
    conn.row_factory = sqlite3.Row  # This allows us to access columns by name
    return conn

# Function to initialize the database and create tables
def init_db():
    """
    Creates the users table if it doesn't exist.
    Table structure:
    - id: unique identifier for each user (auto-incremented)
    - name: user's full name
    - email: user's email (must be unique)
    - password: hashed password (never store plain text passwords!)
    """
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()  # Save the changes
    conn.close()   # Close the connection
    print("Database initialized successfully!")

# Run this when the module is executed directly
if __name__ == '__main__':
    init_db()
