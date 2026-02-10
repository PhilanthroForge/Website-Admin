
import os
import json
import re

BASE_DIR = '/Users/bipashahalder/Documents/Philanthroforge_Complete_Clone'
ADMIN_DATA_DIR = os.path.join(BASE_DIR, 'admin', 'data', 'pages')

NAV_PLACEHOLDER = '<div id="navbar-placeholder"></div>'
FOOTER_PLACEHOLDER = '<div id="footer-placeholder"></div>'

def process_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    modified = False
    content_blocks = data.get('content_blocks', [])
    
    for block in content_blocks:
        # Check for Header
        if block.get('type') == 'HEADER':
            current_content = block.get('content', '')
            # If it doesn't already have the placeholder, or has raw header tags
            if 'id="navbar-placeholder"' not in current_content or '<header' in current_content:
                print(f"Updating HEADER in {os.path.basename(file_path)}")
                # Retain the placeholder, remove hardcoded header if possible, or just force the placeholder
                # Simples approach: Just set it to the placeholder. 
                # BUT: The Home page had a hero section inside the header block in previous edits.
                # Let's check if it's the home page or not.
                # Actually, for most pages, the header block IS the navigation.
                # For Home, the "HEADER" block contained the Hero as well.
                
                if 'home.json' in file_path:
                     # For home, we want placeholder + hero content. 
                     # We already fixed home.json manually.
                     pass 
                else:
                    # For other pages, "HEADER" is usually just the nav bar area.
                    # Let's see what about.json had.
                    # It had: <div class="container..." ... <a href="index.html">...
                    # We should replace all that with just the placeholder.
                    block['content'] = NAV_PLACEHOLDER
                    modified = True
                    
        # Check for Footer
        if block.get('type') == 'FOOTER':
            current_content = block.get('content', '')
            if 'id="footer-placeholder"' not in current_content or '<footer' in current_content:
                print(f"Updating FOOTER in {os.path.basename(file_path)}")
                block['content'] = FOOTER_PLACEHOLDER
                modified = True

    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        print(f"Saved updates to {os.path.basename(file_path)}")

def main():
    for root, dirs, files in os.walk(ADMIN_DATA_DIR):
        for file in files:
            if file.endswith('.json'):
                process_json_file(os.path.join(root, file))

if __name__ == "__main__":
    main()
