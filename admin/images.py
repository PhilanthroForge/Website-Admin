"""
Image Management Module
Handles image uploads, optimization, and file operations
"""
import os
from PIL import Image
from werkzeug.utils import secure_filename
from config import Config
import shutil

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def optimize_image(image_path, max_width=1920, quality=85):
    """
    Optimize image by resizing and compressing
    
    Args:
        image_path: Path to the image file
        max_width: Maximum width in pixels
        quality: JPEG quality (1-100)
    """
    try:
        with Image.open(image_path) as img:
            # Convert RGBA to RGB if necessary
            if img.mode == 'RGBA':
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[3])
                img = background
            
            # Resize if too large
            if img.width > max_width:
                ratio = max_width / img.width
                new_height = int(img.height * ratio)
                img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
            
            # Save optimized
            if image_path.lower().endswith(('.jpg', '.jpeg')):
                img.save(image_path, 'JPEG', quality=quality, optimize=True)
            elif image_path.lower().endswith('.png'):
                img.save(image_path, 'PNG', optimize=True)
            elif image_path.lower().endswith('.webp'):
                img.save(image_path, 'WEBP', quality=quality, optimize=True)
            
        return True
    except Exception as e:
        print(f"Error optimizing image: {e}")
        return False

def save_uploaded_file(file, folder=''):
    """
    Save uploaded file to assets directory
    
    Args:
        file: FileStorage object from request.files
        folder: Subdirectory within assets (e.g., 'home', 'branding')
    
    Returns:
        dict with success status and file info or error
    """
    if not file:
        return {'success': False, 'error': 'No file provided'}
    
    if not allowed_file(file.filename):
        return {'success': False, 'error': 'File type not allowed'}
    
    # Secure the filename
    filename = secure_filename(file.filename)
    
    # Create target directory
    target_dir = os.path.join(Config.UPLOAD_FOLDER, folder) if folder else Config.UPLOAD_FOLDER
    os.makedirs(target_dir, exist_ok=True)
    
    # Full path
    filepath = os.path.join(target_dir, filename)
    
    # Check if file exists
    if os.path.exists(filepath):
        # Add number to filename
        name, ext = os.path.splitext(filename)
        counter = 1
        while os.path.exists(filepath):
            filename = f"{name}_{counter}{ext}"
            filepath = os.path.join(target_dir, filename)
            counter += 1
    
    try:
        # Save file
        file.save(filepath)
        
        # Get file size (before optimization)
        original_size = os.path.getsize(filepath)
        
        # Optimize if it's an image
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
            optimize_image(filepath)
        
        # Get optimized size
        optimized_size = os.path.getsize(filepath)
        
        # Get relative path
        rel_path = os.path.relpath(filepath, Config.BASE_DIR)
        
        return {
            'success': True,
            'filename': filename,
            'path': rel_path,
            'folder': folder,
            'size': optimized_size,
            'original_size': original_size,
            'saved_bytes': original_size - optimized_size
        }
    
    except Exception as e:
        return {'success': False, 'error': f'Failed to save file: {str(e)}'}

def delete_image(filepath):
    """
    Delete an image file
    
    Args:
        filepath: Relative path to the image
    
    Returns:
        dict with success status
    """
    try:
        full_path = os.path.join(Config.BASE_DIR, filepath)
        
        if not os.path.exists(full_path):
            return {'success': False, 'error': 'File not found'}
        
        # Security check: make sure it's in assets folder
        if not full_path.startswith(Config.UPLOAD_FOLDER):
            return {'success': False, 'error': 'Invalid file path'}
        
        os.remove(full_path)
        return {'success': True, 'message': 'File deleted successfully'}
    
    except Exception as e:
        return {'success': False, 'error': f'Failed to delete file: {str(e)}'}

def rename_image(old_path, new_name):
    """
    Rename an image file
    
    Args:
        old_path: Current relative path
        new_name: New filename (without path)
    
    Returns:
        dict with success status and new path
    """
    try:
        old_full_path = os.path.join(Config.BASE_DIR, old_path)
        
        if not os.path.exists(old_full_path):
            return {'success': False, 'error': 'File not found'}
        
        # Security check
        if not old_full_path.startswith(Config.UPLOAD_FOLDER):
            return {'success': False, 'error': 'Invalid file path'}
        
        # Secure new name
        new_name = secure_filename(new_name)
        
        # Get directory
        directory = os.path.dirname(old_full_path)
        new_full_path = os.path.join(directory, new_name)
        
        # Check if new name already exists
        if os.path.exists(new_full_path):
            return {'success': False, 'error': 'File with this name already exists'}
        
        # Rename
        os.rename(old_full_path, new_full_path)
        
        # Get new relative path
        new_rel_path = os.path.relpath(new_full_path, Config.BASE_DIR)
        
        return {
            'success': True,
            'message': 'File renamed successfully',
            'new_path': new_rel_path,
            'new_name': new_name
        }
    
    except Exception as e:
        return {'success': False, 'error': f'Failed to rename file: {str(e)}'}

def replace_image(file, existing_path):
    """
    Replace an existing image with a new upload
    
    Args:
        file: FileStorage object from request.files
        existing_path: Relative path of the existing image to replace
    
    Returns:
        dict with success status
    """
    try:
        existing_full_path = os.path.join(Config.BASE_DIR, existing_path)
        
        if not os.path.exists(existing_full_path):
            return {'success': False, 'error': 'Existing file not found'}
        
        # Security check
        if not existing_full_path.startswith(Config.UPLOAD_FOLDER):
            return {'success': False, 'error': 'Invalid file path'}
        
        if not file:
            return {'success': False, 'error': 'No file provided'}
        
        if not allowed_file(file.filename):
            return {'success': False, 'error': 'File type not allowed'}
        
        # Get original filename from existing path
        original_filename = os.path.basename(existing_path)
        
        # Create a temporary path for the new file
        temp_path = existing_full_path + '.tmp'
        
        # Save new file to temporary location
        file.save(temp_path)
        
        #Get file sizes
        original_size = os.path.getsize(existing_full_path)
        new_size = os.path.getsize(temp_path)
        
        # Optimize the new image
        if temp_path.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
            optimize_image(temp_path)
        optimized_size = os.path.getsize(temp_path)
        
        # Remove the old file
        os.remove(existing_full_path)
        
        # Rename temp file to original name
        os.rename(temp_path, existing_full_path)
        
        return {
            'success': True,
            'message': f'Image replaced successfully',
            'filename': original_filename,
            'path': existing_path,
            'old_size': original_size,
            'new_size': optimized_size
        }
    
    except Exception as e:
        # Clean up temp file if it exists
        if 'temp_path' in locals() and os.path.exists(temp_path):
            os.remove(temp_path)
        return {'success': False, 'error': f'Failed to replace image: {str(e)}'}


def get_image_info(filepath):
    """
    Get detailed information about an image
    
    Args:
        filepath: Relative path to the image
    
    Returns:
        dict with image information
    """
    try:
        full_path = os.path.join(Config.BASE_DIR, filepath)
        
        if not os.path.exists(full_path):
            return None
        
        # Get file stats
        stats = os.stat(full_path)
        
        info = {
            'name': os.path.basename(filepath),
            'path': filepath,
            'size': stats.st_size,
            'size_formatted': format_file_size(stats.st_size),
            'modified': stats.st_mtime
        }
        
        # Get image dimensions if it's an image
        if filepath.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif')):
            try:
                with Image.open(full_path) as img:
                    info['width'] = img.width
                    info['height'] = img.height
                    info['format'] = img.format
            except:
                pass
        
        return info
    
    except Exception as e:
        return None

def format_file_size(size_bytes):
    """Format file size in human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"
