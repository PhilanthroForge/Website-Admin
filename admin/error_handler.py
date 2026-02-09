"""
Error Handling Module

Provides centralized error handling, logging, and custom error pages
for the PhilanthroForge Admin Panel.
"""

import os
import logging
from datetime import datetime
from functools import wraps
from flask import render_template, flash, redirect, url_for, request
from werkzeug.exceptions import HTTPException

# Configure logging
LOG_FOLDER = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(LOG_FOLDER, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(LOG_FOLDER, 'admin.log')),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def log_error(error, context=None):
    """Log an error with optional context"""
    error_msg = f"Error: {str(error)}"
    if context:
        error_msg += f" | Context: {context}"
    logger.error(error_msg)


def log_info(message):
    """Log informational message"""
    logger.info(message)


def log_auth_attempt(email, success):
    """Log authentication attempts"""
    status = "SUCCESS" if success else "FAILED"
    logger.info(f"Auth attempt: {email} - {status} - IP: {request.remote_addr}")


def log_content_change(user_id, action, content_type, content_id):
    """Log content changes for audit trail"""
    logger.info(f"User {user_id} {action} {content_type}: {content_id}")


def handle_errors(f):
    """
    Decorator to handle errors in route functions
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except HTTPException:
            # Let HTTP exceptions pass through (404, 403, etc.)
            raise
        except Exception as e:
            log_error(e, context=f"Route: {request.endpoint}")
            flash(f'An error occurred: {str(e)}', 'error')
            return redirect(url_for('dashboard'))
    return decorated_function


def register_error_handlers(app):
    """Register error handlers with the Flask  app"""
    
    @app.errorhandler(404)
    def not_found_error(error):
        """Handle 404 errors"""
        log_error(f"404 Not Found: {request.url}")
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors"""
        log_error(f"500 Internal Error: {str(error)}")
        return render_template('errors/500.html'), 500
    
    @app.errorhandler(403)
    def forbidden_error(error):
        """Handle 403 errors"""
        log_error(f"403 Forbidden: {request.url}")
        return render_template('errors/403.html'), 403
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        """Handle all other exceptions"""
        if isinstance(error, HTTPException):
            return error
        
        log_error(error, context="Unhandled exception")
        return render_template('errors/500.html'), 500
