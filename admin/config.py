"""
Flask Admin Panel Configuration
"""
import os
from datetime import timedelta

class Config:
    # Base directory
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    
    # Secret key for session management
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Session configuration
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # File upload configuration
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'svg', 'webp'}
    
    # Content data folders
    DATA_FOLDER = os.path.join(os.path.dirname(__file__), 'data')
    PAGES_FOLDER = os.path.join(DATA_FOLDER, 'pages')
    SERVICES_FOLDER = os.path.join(DATA_FOLDER, 'services')
    CASES_FOLDER = os.path.join(DATA_FOLDER, 'case-studies')
    COMPONENTS_FOLDER = os.path.join(DATA_FOLDER, 'components')
    
    # Database
    DATABASE = os.path.join(os.path.dirname(__file__), 'users.db')
    
    # Admin credentials (initial setup)
    DEFAULT_ADMIN_EMAIL = 'admin@philanthroforge.com'
    DEFAULT_ADMIN_PASSWORD = 'ChangeMe123!'  # User will change on first login

    # Unsplash API Configuration
    UNSPLASH_ACCESS_KEY = os.environ.get('UNSPLASH_ACCESS_KEY') or '0uRLpYAEQbLf1qw5DIN1IYy0oRdBX3Uh8ayzoO7Hyfg'
    UNSPLASH_SECRET_KEY = os.environ.get('UNSPLASH_SECRET_KEY') or '3whfR8dCArWtdGDYZKA5IsOEFTnFSMqaj3JE4zY_6hU'
