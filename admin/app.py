"""
PhilanthroForge Admin Panel
Flask application for content management
"""
import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_from_directory
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from config import Config
import auth
import content as content_module
import images as images_module
import components as components_module
import portfolio as portfolio_module
import settings as settings_module
import error_handler

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access the admin panel.'

@login_manager.user_loader
def load_user(user_id):
    return auth.get_user_by_id(int(user_id))

# Create necessary folders
os.makedirs(Config.DATA_FOLDER, exist_ok=True)
os.makedirs(Config.PAGES_FOLDER, exist_ok=True)
os.makedirs(Config.SERVICES_FOLDER, exist_ok=True)
os.makedirs(Config.CASES_FOLDER, exist_ok=True)
os.makedirs(Config.COMPONENTS_FOLDER, exist_ok=True)

# Initialize database
auth.init_db()

# Register error handlers
error_handler.register_error_handlers(app)
error_handler.log_info("Admin panel started successfully")

# ============================================================================
# Routes
# ============================================================================

@app.route('/')
def index():
    """Redirect root to admin dashboard"""
    return redirect(url_for('dashboard'))

@app.route('/admin')
@app.route('/admin/')
def admin_redirect():
    """Redirect /admin to dashboard"""
    return redirect(url_for('dashboard'))

@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember', False)
        
        # Import security module
        import security
        
        # Check rate limit
        if security.check_rate_limit(email):
            error_handler.log_error(f"Rate limit exceeded for {email}")
            flash('Too many login attempts. Please try again later.', 'error')
            return render_template('admin/login.html')
        
        # Record login attempt
        security.record_login_attempt(email)
        
        user = auth.authenticate_user(email, password)
        
        if user:
            login_user(user, remember=remember)
            error_handler.log_auth_attempt(email, True)
            flash('Login successful!', 'success')
            
            # Redirect to next page or dashboard
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            error_handler.log_auth_attempt(email, False)
            flash('Invalid email or password.', 'error')
    
    return render_template('admin/login.html')

@app.route('/admin/logout')
@login_required
def logout():
    """Logout"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/admin/dashboard')
@login_required
def dashboard():
    """Admin dashboard"""
    # Get stats
    stats = {
        'pages': count_files(Config.PAGES_FOLDER),
        'services': count_files(Config.SERVICES_FOLDER),
        'case_studies': count_files(Config.CASES_FOLDER),
        'images': count_images(Config.UPLOAD_FOLDER)
    }
    
    return render_template('admin/dashboard.html', stats=stats, user=current_user)

@app.route('/admin/pages')
@login_required
def pages_list():
    """List all pages"""
    pages = content_module.get_all_pages()
    return render_template('admin/pages.html', pages=pages)

@app.route('/admin/pages/<path:page_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_page(page_id):
    """Edit page content"""
    try:
        if request.method == 'POST':
            # Get form data
            data = request.get_json() if request.is_json else request.form
            
            # Save content
            content_module.save_page_content(page_id, dict(data))
            
            if request.is_json:
                return jsonify({'status': 'success', 'message': 'Page saved successfully'})
            else:
                flash('Page saved successfully!', 'success')
                return redirect(url_for('pages_list'))
        
        # Load existing content
        page_content = content_module.get_page_content(page_id)
        section_types = content_module.get_section_types()
        
        return render_template('admin/edit_page.html', 
                             page_id=page_id, 
                             content=page_content,
                             section_types=section_types)
    except Exception as e:
        import traceback
        return f"<h1>Error in edit_page</h1><pre>{traceback.format_exc()}</pre>", 500

@app.route('/admin/pages/publish-all', methods=['POST'])
@login_required
def publish_all():
    """Publish all pages"""
    try:
        results = content_module.publish_all_pages()
        
        success_count = len(results['success'])
        error_count = len(results['error'])
        
        message = f"Published {success_count} pages."
        if error_count > 0:
            message += f" {error_count} errors occurred."
            
        return jsonify({
            'success': True, 
            'message': message,
            'details': results
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/admin/images')
@login_required
def images():
    """Image manager"""
    folder = request.args.get('folder', '')
    images_list = images_module.get_images_in_folder(os.path.join(Config.UPLOAD_FOLDER, folder))
    folders = images_module.get_subfolders(Config.UPLOAD_FOLDER)
    
    return render_template('admin/images.html', images=images_list, folders=folders, current_folder=folder)

# ============================================================================
# Unsplash API Routes
# ============================================================================

@app.route('/admin/api/unsplash/search', methods=['GET'])
@login_required
def search_unsplash():
    """Proxy search requests to Unsplash"""
    query = request.args.get('query', '')
    page = request.args.get('page', 1)
    
    if not query:
        return jsonify({'results': []})
    
    try:
        from unsplash import search_photos
        data = search_photos(query, page)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin/api/unsplash/download', methods=['POST'])
@login_required
def download_unsplash():
    """Trigger download and save to local storage"""
    data = request.json
    download_location = data.get('download_location')
    photo_id = data.get('id')
    
    if not download_location:
         return jsonify({'error': 'Missing download location'}), 400
         
    try:
        from unsplash import download_photo
        local_path = download_photo(download_location, photo_id)
        
        if local_path:
            return jsonify({'success': True, 'path': local_path})
        else:
            return jsonify({'error': 'Download failed'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin/images/upload', methods=['POST'])
@login_required
def upload_image():
    """Handle image upload"""
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file provided'}), 400
    
    file = request.files['file']
    folder = request.form.get('folder', '')
    
    result = images_module.save_uploaded_file(file, folder)
    
    if result['success']:
        flash(f"Image uploaded successfully: {result['filename']}", 'success')
        return jsonify(result), 200
    else:
        return jsonify(result), 400

@app.route('/admin/images/delete', methods=['POST'])
@login_required
def delete_image():
    """Delete an image"""
    data = request.get_json()
    filepath = data.get('path')
    
    if not filepath:
        return jsonify({'success': False, 'error': 'No file path provided'}), 400
    
    result = images_module.delete_image(filepath)
    
    if result['success']:
        flash('Image deleted successfully', 'success')
    
    return jsonify(result)

@app.route('/admin/images/rename', methods=['POST'])
@login_required
def rename_image():
    """Rename an image"""
    data = request.get_json()
    old_path = data.get('old_path')
    new_name = data.get('new_name')
    
    if not old_path or not new_name:
        return jsonify({'success': False, 'error': 'Missing parameters'}), 400
    
    result = images_module.rename_image(old_path, new_name)
    
    if result['success']:
        flash(f"Image renamed to {result['new_name']}", 'success')
    
    return jsonify(result)

@app.route('/admin/images/replace', methods=['POST'])
@login_required
def replace_image():
    """Replace an existing image with a new file"""
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file provided'}), 400
    
    file = request.files['file']
    existing_path = request.form.get('existing_path')
    
    if not existing_path:
        return jsonify({'success': False, 'error': 'No target path specified'}), 400
    
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'}), 400
    
    result = images_module.replace_image(file, existing_path)
    return jsonify(result)


@app.route('/admin/settings')
@login_required
def settings():
    """Settings page"""
    site_settings = settings_module.get_site_settings()
    return render_template('admin/settings.html', settings=site_settings)

@app.route('/admin/settings/site', methods=['POST'])
@login_required
def save_settings():
    """Save site settings"""
    data = request.get_json() if request.is_json else request.form.to_dict()
    
    # Reconstruct nested structure from flat form data
    settings = settings_module.get_site_settings()
    
    # Update site section
    if 'site_name' in data:
        settings['site']['name'] = data.get('site_name', '')
        settings['site']['tagline'] = data.get('site_tagline', '')
        settings['site']['description'] = data.get('site_description', '')
        settings['site']['keywords'] = [k.strip() for k in data.get('site_keywords', '').split(',') if k.strip()]
    
    # Update contact section
    if 'contact_email' in data:
        settings['contact']['email'] = data.get('contact_email', '')
        settings['contact']['phone'] = data.get('contact_phone', '')
        settings['contact']['address'] = data.get('contact_address', '')
        settings['contact']['business_hours'] = data.get('contact_business_hours', '')
    
    # Update social section
    if 'social_linkedin' in data:
        settings['social']['linkedin'] = data.get('social_linkedin', '')
        settings['social']['twitter'] = data.get('social_twitter', '')
        settings['social']['facebook'] = data.get('social_facebook', '')
        settings['social']['instagram'] = data.get('social_instagram', '')
        settings['social']['youtube'] = data.get('social_youtube', '')
    
    # Update SEO section
    if 'seo_meta_description' in data:
        settings['seo']['meta_description'] = data.get('seo_meta_description', '')
        settings['seo']['google_analytics'] = data.get('seo_google_analytics', '')
        settings['seo']['og_image'] = data.get('seo_og_image', '')
        settings['seo']['sitemap_enabled'] = data.get('seo_sitemap_enabled') == 'true'
    
    # Update admin section
    if 'admin_session_timeout' in data:
        settings['admin']['session_timeout'] = int(data.get('admin_session_timeout', 30))
        settings['admin']['auto_save'] = data.get('admin_auto_save') == 'true'
        settings['admin']['items_per_page'] = int(data.get('admin_items_per_page', 20))
        settings['admin']['email_notifications'] = data.get('admin_email_notifications') == 'true'
    
    # Save settings
    if settings_module.save_site_settings(settings):
        result = {'success': True, 'message': 'Settings saved successfully'}
    else:
        result = {'success': False, 'message': 'Failed to save settings'}
    
    if request.is_json:
        return jsonify(result)
    else:
        flash(result['message'], 'success' if result['success'] else 'error')
        return redirect(url_for('settings'))

@app.route('/admin/settings/password', methods=['POST'])
@login_required
def change_password():
    """Change admin password"""
    data = request.get_json() if request.is_json else request.form.to_dict()
    
    current_password = data.get('current_password', '')
    new_password = data.get('new_password', '')
    confirm_password = data.get('confirm_password', '')
    
    # Validate passwords match
    if new_password != confirm_password:
        result = {'success': False, 'message': 'New passwords do not match'}
    else:
        success, message = settings_module.update_password(
            current_user.username,
            current_password,
            new_password
        )
        result = {'success': success, 'message': message}
    
    if request.is_json:
        return jsonify(result)
    else:
        flash(result['message'], 'success' if result['success'] else 'error')
        return redirect(url_for('settings'))

@app.route('/admin/settings/backup', methods=['GET'])
@login_required
def create_backup():
    """Create and download backup"""
    backup_path = settings_module.create_backup()
    
    if backup_path and os.path.exists(backup_path):
        directory = os.path.dirname(backup_path)
        filename = os.path.basename(backup_path)
        return send_from_directory(directory, filename, as_attachment=True)
    else:
        flash('Failed to create backup', 'error')
        return redirect(url_for('settings'))

@app.route('/admin/settings/restore', methods=['POST'])
@login_required
def restore_backup():
    """Restore from backup file"""
    if 'backup_file' not in request.files:
        flash('No file uploaded', 'error')
        return redirect(url_for('settings'))
    
    file = request.files['backup_file']
    
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('settings'))
    
    if not file.filename.endswith('.zip'):
        flash('Invalid file type. Please upload a ZIP file', 'error')
        return redirect(url_for('settings'))
    
    # Save uploaded file temporarily
    temp_path = os.path.join(Config.DATA_FOLDER, 'temp_backup.zip')
    file.save(temp_path)
    
    # Restore from backup
    success, message = settings_module.restore_backup(temp_path)
    
    # Clean up temp file
    if os.path.exists(temp_path):
        os.remove(temp_path)
    
    flash(message, 'success' if success else 'error')
    return redirect(url_for('settings'))

@app.route('/admin/api/stats')
@login_required
def api_stats():
    """API endpoint for dashboard statistics"""
    stats = settings_module.get_system_stats()
    return jsonify(stats)

@app.route('/admin/components')
@login_required
def components_list():
    """List components (navbar, footer)"""
    return render_template('admin/components.html')

@app.route('/admin/components/navbar', methods=['GET', 'POST'])
@login_required
def edit_navbar():
    """Edit navbar component"""
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form.to_dict()
        result = components_module.save_navbar_config(data)
        
        if request.is_json:
            return jsonify(result)
        else:
            flash('Navbar updated successfully!', 'success')
            return redirect(url_for('components_list'))
    
    config = components_module.get_navbar_config()
    return render_template('admin/edit_navbar.html', config=config)

@app.route('/admin/components/footer', methods=['GET', 'POST'])
@login_required
def edit_footer():
    """Edit footer component"""
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form.to_dict()
        result = components_module.save_footer_config(data)
        
        if request.is_json:
            return jsonify(result)
        else:
            flash('Footer updated successfully!', 'success')
            return redirect(url_for('components_list'))
    
    config = components_module.get_footer_config()
    return render_template('admin/edit_footer.html', config=config)

# ============================================================================
# Services Management
# ============================================================================

@app.route('/admin/services')
@login_required
def services_list():
    """List all services"""
    services = portfolio_module.get_all_services()
    return render_template('admin/services.html', services=services)

@app.route('/admin/services/new')
@login_required
def new_service():
    """Create a new service"""
    service = portfolio_module.create_service_template()
    return render_template('admin/edit_service.html', service=service, is_new=True)

@app.route('/admin/services/<service_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_service(service_id):
    """Edit a service"""
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form.to_dict()
        result = portfolio_module.save_service(service_id, data)
        
        if request.is_json:
            return jsonify(result)
        else:
            flash(result['message'], 'success')
            return redirect(url_for('services_list'))
    
    service = portfolio_module.get_service(service_id)
    if not service:
        flash('Service not found', 'error')
        return redirect(url_for('services_list'))
    
    return render_template('admin/edit_service.html', service=service, is_new=False)

@app.route('/admin/services/<service_id>/delete', methods=['POST'])
@login_required
def delete_service(service_id):
    """Delete a service"""
    result = portfolio_module.delete_service(service_id)
    
    if request.is_json:
        return jsonify(result)
    else:
        flash(result.get('message', result.get('error')), 'success' if result['success'] else 'error')
        return redirect(url_for('services_list'))

# ============================================================================
# Case Studies Management
# ============================================================================

@app.route('/admin/case-studies')
@login_required
def case_studies_list():
    """List all case studies"""
    case_studies = portfolio_module.get_all_case_studies()
    return render_template('admin/case_studies.html', case_studies=case_studies)

@app.route('/admin/case-studies/new')
@login_required
def new_case_study():
    """Create a new case study"""
    case_study = portfolio_module.create_case_study_template()
    return render_template('admin/edit_case_study.html', case_study=case_study, is_new=True)

@app.route('/admin/case-studies/<case_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_case_study(case_id):
    """Edit a case study"""
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form.to_dict()
        result = portfolio_module.save_case_study(case_id, data)
        
        if request.is_json:
            return jsonify(result)
        else:
            flash(result['message'], 'success')
            return redirect(url_for('case_studies_list'))
    
    case_study = portfolio_module.get_case_study(case_id)
    if not case_study:
        flash('Case study not found', 'error')
        return redirect(url_for('case_studies_list'))
    
    return render_template('admin/edit_case_study.html', case_study=case_study, is_new=False)

@app.route('/admin/case-studies/<case_id>/delete', methods=['POST'])
@login_required
def delete_case_study(case_id):
    """Delete a case study"""
    result = portfolio_module.delete_case_study(case_id)
    
    if request.is_json:
        return jsonify(result)
    else:
        flash(result.get('message', result.get('error')), 'success' if result['success'] else 'error')
        return redirect(url_for('case_studies_list'))


# ============================================================================
# Helper Functions
# ============================================================================

def count_files(folder):
    """Count JSON files in a folder"""
    if not os.path.exists(folder):
        return 0
    return len([f for f in os.listdir(folder) if f.endswith('.json')])

def count_images(folder):
    """Count images recursively"""
    if not os.path.exists(folder):
        return 0
    count = 0
    for root, dirs, files in os.walk(folder):
        count += len([f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp'))])
    return count

def get_all_pages():
    """Get list of all pages"""
    pages = []
    if os.path.exists(Config.PAGES_FOLDER):
        for filename in os.listdir(Config.PAGES_FOLDER):
            if filename.endswith('.json'):
                pages.append({
                    'id': filename.replace('.json', ''),
                    'name': filename.replace('.json', '').replace('-', ' ').title()
                })
    return pages

def get_images_in_folder(folder_path):
    """Get images in a specific folder"""
    if not os.path.exists(folder_path):
        return []
    
    images = []
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp')):
            images.append({
                'name': filename,
                'path': os.path.relpath(os.path.join(folder_path, filename), Config.BASE_DIR)
            })
    return images

def get_subfolders(folder_path):
    """Get subfolders in assets directory"""
    if not os.path.exists(folder_path):
        return []
    
    folders = []
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isdir(item_path) and not item.startswith('.'):
            folders.append(item)
    return sorted(folders)

# ============================================================================
# Static File Serving
# ============================================================================

@app.route('/assets/<path:filename>')
def serve_assets(filename):
    """Serve static files from assets directory"""
    return send_from_directory(Config.UPLOAD_FOLDER, filename)

# ============================================================================
# Security Headers
# ============================================================================

@app.after_request
def add_security_headers(response):
    """Add security headers to all responses"""
    import security
    return security.add_security_headers(response)


# ============================================================================
# Run Application
# ============================================================================

if __name__ == '__main__':
    port = int(os.environ.get('FLASK_RUN_PORT', 5001))
    
    # Print access info
    print("\n" + "="*60)
    print("PhilanthroForge Admin Panel")
    print("="*60)
    print(f"\n🌐 Admin Panel: http://localhost:{port}/admin")
    print(f"📧 Email: {Config.DEFAULT_ADMIN_EMAIL}")
    print(f"🔑 Password: {Config.DEFAULT_ADMIN_PASSWORD}")
    print(f"\n⚠️  CHANGE THE DEFAULT PASSWORD AFTER FIRST LOGIN!")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=port)
