"""
Security Module

Implements various security features for the PhilanthroForge Admin Panel
including CSRF protection (Flask built-in), rate limiting, and secure headers.
"""

from functools import wraps
from time import time
from flask import request, abort
import error_handler

# Rate limiting storage (in-memory, for production use Redis or similar)
login_attempts = {}
RATE_LIMIT_WINDOW = 900  # 15 minutes in seconds
MAX_LOGIN_ATTEMPTS = 5


def check_rate_limit(email):
    """
    Check if user has exceeded login rate limit
    
    Returns:
        bool: True if rate limit exceeded, False otherwise
    """
    now = time()
    
    if email not in login_attempts:
        login_attempts[email] = []
    
    # Remove old attempts outside the time window
    login_attempts[email] = [
        attempt_time for attempt_time in login_attempts[email]
        if now - attempt_time < RATE_LIMIT_WINDOW
    ]
    
    # Check if limit exceeded
    if len(login_attempts[email]) >= MAX_LOGIN_ATTEMPTS:
        error_handler.log_error(f"Rate limit exceeded for {email}")
        return True
    
    return False


def record_login_attempt(email):
    """Record a  login attempt for rate limiting"""
    if email not in login_attempts:
        login_attempts[email] = []
    login_attempts[email].append(time())


def add_security_headers(response):
    """Add security headers to response"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.tailwindcss.com https://cdn.tiny.cloud https://cdnjs.cloudflare.com; img-src 'self' data: https:;"
    return response


def validate_file_upload(file, allowed_extensions={'png', 'jpg', 'jpeg', 'gif', 'webp', 'svg'}, max_size_mb=10):
    """
    Validate uploaded file
    
    Args:
        file: FileStorage object from Flask
        allowed_extensions: Set of allowed file extensions
        max_size_mb: Maximum file size in megabytes
    
    Returns:
        tuple: (is_valid: bool, error_message: str or None)
    """
    if not file or file.filename == '':
        return False, "No file provided"
    
    # Check extension
    if '.' not in file.filename:
        return False, "File has no extension"
    
    ext = file.filename.rsplit('.', 1)[1].lower()
    if ext not in allowed_extensions:
        return False, f"File type .{ext} not allowed. Allowed types: {', '.join(allowed_extensions)}"
    
    # Check file size
    file.seek(0, 2)  # Seek to end
    size = file.tell()
    file.seek(0)  # Reset to beginning
    
    max_size = max_size_mb * 1024 * 1024
    if size > max_size:
        return False, f"File size ({size / 1024 / 1024:.1f}MB) exceeds maximum allowed size ({max_size_mb}MB)"
    
    return True, None


def sanitize_filename(filename):
    """
    Sanitize filename to prevent directory traversal
    
    Args:
        filename: Original filename
    
    Returns:
        str: Sanitized filename
    """
    # Remove any directory components
    filename = filename.split('/')[-1].split('\\')[-1]
    
    # Allow only alphanumeric, dash, underscore, and dot
    import re
    filename = re.sub(r'[^\w\-.]', '_', filename)
    
    return filename


def require_admin(f):
    """
    Decorator to require admin privileges
    (Currently all authenticated users are admin, but this allows for future expansion)
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from flask_login import current_user
        if not current_user.is_authenticated:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function
