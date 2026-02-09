"""
Authentication Module
Handles user authentication, password hashing, and session management
"""
import sqlite3
import bcrypt
from flask_login import UserMixin
from config import Config

class User(UserMixin):
    def __init__(self, id, email):
        self.id = id
        self.email = email

def init_db():
    """Initialize the database with users table"""
    conn = sqlite3.connect(Config.DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        )
    ''')
    
    # Create default admin user if doesn't exist
    cursor.execute('SELECT COUNT(*) FROM users WHERE email = ?', (Config.DEFAULT_ADMIN_EMAIL,))
    if cursor.fetchone()[0] == 0:
        password_hash = hash_password(Config.DEFAULT_ADMIN_PASSWORD)
        cursor.execute(
            'INSERT INTO users (email, password_hash) VALUES (?, ?)',
            (Config.DEFAULT_ADMIN_EMAIL, password_hash)
        )
        print(f"✅ Default admin user created: {Config.DEFAULT_ADMIN_EMAIL}")
        print(f"   Password: {Config.DEFAULT_ADMIN_PASSWORD}")
        print("   ⚠️  CHANGE THIS PASSWORD IMMEDIATELY!")
    
    conn.commit()
    conn.close()

def hash_password(password):
    """Hash a password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password, password_hash):
    """Verify a password against its hash"""
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))

def get_user_by_email(email):
    """Retrieve user by email"""
    conn = sqlite3.connect(Config.DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT id, email FROM users WHERE email = ?', (email,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return User(id=row[0], email=row[1])
    return None

def get_user_by_id(user_id):
    """Retrieve user by ID"""
    conn = sqlite3.connect(Config.DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT id, email FROM users WHERE id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return User(id=row[0], email=row[1])
    return None

def authenticate_user(email, password):
    """Authenticate user with email and password"""
    conn = sqlite3.connect(Config.DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT id, email, password_hash FROM users WHERE email = ?', (email,))
    row = cursor.fetchone()
    
    if row and verify_password(password, row[2]):
        # Update last login
        cursor.execute('UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?', (row[0],))
        conn.commit()
        conn.close()
        return User(id=row[0], email=row[1])
    
    conn.close()
    return None

def update_password(user_id, new_password):
    """Update user password"""
    password_hash = hash_password(new_password)
    conn = sqlite3.connect(Config.DATABASE)
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET password_hash = ? WHERE id = ?', (password_hash, user_id))
    conn.commit()
    conn.close()
    return True
