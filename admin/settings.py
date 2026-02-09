"""
Settings Module

Manages site-wide settings, admin preferences, backup/restore functionality,
and password management for the PhilanthroForge Admin Panel.
"""

import os
import json
import zipfile
import shutil
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from config import Config


def get_site_settings():
    """Get site settings from JSON file"""
    settings_file = os.path.join(Config.DATA_FOLDER, 'settings.json')
    
    if not os.path.exists(settings_file):
        # Create default settings if file doesn't exist
        default_settings = create_settings_template()
        save_site_settings(default_settings)
        return default_settings
    
    try:
        with open(settings_file, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading settings: {e}")
        return create_settings_template()


def save_site_settings(data):
    """Save site settings to JSON file"""
    settings_file = os.path.join(Config.DATA_FOLDER, 'settings.json')
    
    # Ensure data folder exists
    os.makedirs(Config.DATA_FOLDER, exist_ok=True)
    
    # Add timestamp
    data['updated_at'] = datetime.now().isoformat()
    
    try:
        with open(settings_file, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving settings: {e}")
        return False


def create_settings_template():
    """Create default settings structure"""
    return {
        "site": {
            "name": "PhilanthroForge",
            "tagline": "Forging the Next Era of Fundraising",
            "description": "Nonprofit Growth Consultants specializing in fundraising strategy and digital transformation",
            "keywords": ["nonprofit", "fundraising", "consultant", "philanthropy", "donation"]
        },
        "contact": {
            "email": "info@philanthroforge.com",
            "phone": "+1 (555) 123-4567",
            "address": "123 Main Street, City, State 12345",
            "business_hours": "Monday - Friday, 9:00 AM - 5:00 PM EST"
        },
        "social": {
            "linkedin": "https://linkedin.com/company/philanthroforge",
            "twitter": "",
            "facebook": "",
            "instagram": "",
            "youtube": ""
        },
        "seo": {
            "meta_description": "PhilanthroForge: Expert nonprofit fundraising consultants helping organizations transform their fundraising strategy",
            "google_analytics": "",
            "og_image": "",
            "sitemap_enabled": True
        },
        "admin": {
            "session_timeout": 30,
            "auto_save": True,
            "items_per_page": 20,
            "email_notifications": False
        },
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }


def get_admin_user():
    """Get admin user details from users database"""
    # Import here to avoid circular import
    import auth
    
    # Get first (and only) user
    user = auth.get_user_by_id(1)  # Admin user has ID 1
    if user:
        return {
            "id": user.id,
            "username": user.username,
            "created_at": None  # auth module doesn't track created_at
        }
    return None


def update_password(username, current_password, new_password):
    """
    Update admin password with verification
    
    Args:
        username: Email address (we call it username in settings context)
        current_password: Current password to verify
        new_password: New password to set
    
    Returns:
        tuple: (success: bool, message: str)
    """
    # Import here to avoid circular import
    import auth
    import sqlite3
    
    # Get user by email (username is email in auth module)
    user = auth.get_user_by_email(username)
    if not user:
        return False, "User not found"
    
    # Get password hash to verify
    conn = sqlite3.connect(Config.DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT password_hash FROM users WHERE id = ?', (user.id,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return False, "User not found"
    
    # Verify current password
    if not auth.verify_password(current_password, row[0]):
        return False, "Current password is incorrect"
    
    # Validate new password
    if len(new_password) < 8:
        return False, "New password must be at least 8 characters long"
    
    # Check password complexity
    has_upper = any(c.isupper() for c in new_password)
    has_lower = any(c.islower() for c in new_password)
    has_digit = any(c.isdigit() for c in new_password)
    
    if not(has_upper and has_lower and has_digit):
        return False, "Password must contain uppercase, lowercase, and numbers"
    
    # Update password
    try:
        success = auth.update_password(user.id, new_password)
        if success:
            return True, "Password updated successfully"
        else:
            return False, "Failed to update password"
    except Exception as e:
        return False, f"Error updating password: {str(e)}"


def get_system_stats():
    """Get system statistics for dashboard"""
    stats = {
        "pages": 0,
        "services": 0,
        "case_studies": 0,
        "images": 0,
        "total_size": 0,
        "last_edited": None
    }
    
    # Count pages
    pages_folder = os.path.join(Config.DATA_FOLDER, 'pages')
    if os.path.exists(pages_folder):
        stats["pages"] = len([f for f in os.listdir(pages_folder) if f.endswith('.json')])
    
    # Count services
    if os.path.exists(Config.SERVICES_FOLDER):
        stats["services"] = len([f for f in os.listdir(Config.SERVICES_FOLDER) if f.endswith('.json')])
    
    # Count case studies
    if os.path.exists(Config.CASES_FOLDER):
        stats["case_studies"] = len([f for f in os.listdir(Config.CASES_FOLDER) if f.endswith('.json')])
    
    # Count images and calculate size
    upload_folder = Config.UPLOAD_FOLDER
    if os.path.exists(upload_folder):
        image_count = 0
        total_size = 0
        
        for root, dirs, files in os.walk(upload_folder):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp')):
                    image_count += 1
                    file_path = os.path.join(root, file)
                    total_size += os.path.getsize(file_path)
        
        stats["images"] = image_count
        stats["total_size"] = total_size
    
    # Get last edited file
    all_json_files = []
    for folder in [pages_folder, Config.SERVICES_FOLDER, Config.CASES_FOLDER]:
        if os.path.exists(folder):
            for file in os.listdir(folder):
                if file.endswith('.json'):
                    file_path = os.path.join(folder, file)
                    all_json_files.append((file_path, os.path.getmtime(file_path)))
    
    if all_json_files:
        latest_file = max(all_json_files, key=lambda x: x[1])
        stats["last_edited"] = datetime.fromtimestamp(latest_file[1]).isoformat()
    
    return stats


def create_backup():
    """
    Create a backup ZIP file of all data
    
    Returns:
        str: Path to created backup file, or None on error
    """
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    backup_filename = f'backup_{timestamp}.zip'
    backup_folder = os.path.join(os.path.dirname(Config.DATA_FOLDER), 'backups')
    
    # Create backups folder if it doesn't exist
    os.makedirs(backup_folder, exist_ok=True)
    
    backup_path = os.path.join(backup_folder, backup_filename)
    
    try:
        with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add data folder contents
            if os.path.exists(Config.DATA_FOLDER):
                for root, dirs, files in os.walk(Config.DATA_FOLDER):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, os.path.dirname(Config.DATA_FOLDER))
                        zipf.write(file_path, arcname)
            
            # Add manifest
            manifest = {
                "backup_date": timestamp,
                "version": "1.0",
                "stats": get_system_stats()
            }
            zipf.writestr('manifest.json', json.dumps(manifest, indent=2))
        
        return backup_path
    except Exception as e:
        print(f"Error creating backup: {e}")
        return None


def restore_backup(zip_file_path):
    """
    Restore data from a backup ZIP file
    
    Args:
        zip_file_path: Path to the backup ZIP file
    
    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        # Validate ZIP file
        if not zipfile.is_zipfile(zip_file_path):
            return False, "Invalid backup file"
        
        # Create backup of current data first
        current_backup = create_backup()
        if not current_backup:
            return False, "Failed to create safety backup of current data"
        
        # Extract backup
        with zipfile.ZipFile(zip_file_path, 'r') as zipf:
            # Check for manifest
            if 'manifest.json' not in zipf.namelist():
                return False, "Invalid backup file: missing manifest"
            
            # Read manifest
            manifest_data = zipf.read('manifest.json')
            manifest = json.loads(manifest_data)
            
            # Extract data folder
            data_base = os.path.dirname(Config.DATA_FOLDER)
            for member in zipf.namelist():
                if member != 'manifest.json':
                    zipf.extract(member, data_base)
        
        return True, f"Backup restored successfully from {manifest.get('backup_date', 'unknown date')}"
    
    except Exception as e:
        return False, f"Error restoring backup: {str(e)}"


def format_file_size(size_bytes):
    """Format file size in human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"
