
import os
import sys
# Add the current directory to path so imports work
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from flask import Flask, render_template, g
from werkzeug.local import LocalProxy

# Mock current_user
class MockUser:
    is_authenticated = True
    email = 'debug@admin.com'
    def get_id(self): return "1"

# Create a dummy Flask-Login extension style current_user
current_user = MockUser()

# Initialize app similar to admin/app.py
app = Flask(__name__, template_folder='admin/templates', static_folder='admin/assets')

# Mock config
class Config:
    SECRET_KEY = 'dev'
    UPLOAD_FOLDER = 'admin/uploads'
    PAGES_FOLDER = 'admin/data/pages'

app.config.from_object(Config)

# Register context processor to inject current_user
@app.context_processor
def inject_user():
    return dict(current_user=current_user)

# Import content module (adjust path as needed)
# We need to make sure 'admin' package is resolvable.
# Since we are in root, 'admin.content' should work if __init__.py exists, 
# but previous file views showed 'admin/content.py'. 
# Let's try direct import or ensure path is correct.

try:
    from admin import content
except ImportError:
    # Fallback if running from root and admin is a subdir
    sys.path.append('admin')
    import content

def debug_render():
    with app.app_context():
        try:
            print("--- Loading Content ---")
            page_content = content.get_page_content('home')
            print("Content Loaded. Type:", type(page_content))
            
            print("--- Loading Section Types ---")
            section_types = content.get_section_types()
            print("Section Types Loaded.")
            
            print("--- Rendering Template ---")
            # We explicitly render the edit_page.html
            # Note: We need to make sure 'macros/sidebar.html' is found relative to 'admin/templates'
            rendered = render_template('admin/edit_page.html', 
                                     page_id='home', 
                                     content=page_content,
                                     section_types=section_types)
            print("Render Success! Length:", len(rendered))
            
        except Exception as e:
            print("\n!!! ERROR DETECTED !!!")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    debug_render()
