import sqlite3
import os

def create_database():
    # Connect to SQLite database (creates it if it doesn't exist)
    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Create images table with foreign key to users
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_images (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        image_path TEXT NOT NULL,
        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    )
    ''')
    
    # Create an index on the foreign key for better performance
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_id ON user_images (user_id)')
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    print("Database and tables created successfully!")
    print("Database file: user_database.db")

if __name__ == "__main__":
    create_database()
