
import os
import json
from bs4 import BeautifulSoup

BASE_DIR = '/Users/bipashahalder/Documents/Philanthroforge_Complete_Clone'
ADMIN_DATA_DIR = os.path.join(BASE_DIR, 'admin', 'data', 'pages')

def get_html_path_from_json(json_path):
    """
    Converts a JSON file path to its corresponding HTML file path.
    e.g., .../admin/data/pages/home.json -> .../index.html
    e.g., .../admin/data/pages/about.json -> .../about.html
    e.g., .../admin/data/pages/services/digital.json -> .../services/digital.html
    """
    rel_path = os.path.relpath(json_path, ADMIN_DATA_DIR)
    
    if rel_path == 'home.json':
        return os.path.join(BASE_DIR, 'index.html')
    
    html_rel_path = rel_path.replace('.json', '.html')
    return os.path.join(BASE_DIR, html_rel_path)

def export_single_page(json_file):
    html_file = get_html_path_from_json(json_file)
    
    if not os.path.exists(html_file):
        print(f"Skipping {os.path.basename(json_file)}: Corresponding HTML {os.path.basename(html_file)} not found.")
        return

    print(f"Exporting: {os.path.basename(json_file)} -> {os.path.basename(html_file)}")

    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    content_blocks = data.get('content_blocks', [])
    
    # Generate HTML from blocks
    new_html_content = ""
    for block in content_blocks:
        content = block.get('content', '')
        if content:
             new_html_content += content + "\n"
        
    # Read existing HTML
    with open(html_file, 'r', encoding='utf-8') as f:
        original_html = f.read()
        
    soup = BeautifulSoup(original_html, 'html.parser')
    
    # Remove existing sections (Main Content)
    sections = soup.find_all('section')
    if not sections:
         # Some pages might use main instead of section
         main = soup.find('main')
         if main:
             # If using main, we might clear its content instead of removing sections
             # But for consistency with previous logic, let's see.
             # The previous logic removed all sections.
             pass
    
    for section in sections:
        section.decompose()
        
    # Insert new content
    full_new_soup = BeautifulSoup(new_html_content, 'html.parser')
    
    # Find insertion point
    # 1. Try Mobile Menu Panel (Header end)
    mobile_menu = soup.find('div', id='mobile-menu-panel')
    
    if mobile_menu:
        mobile_menu.insert_after(full_new_soup)
    else:
        # 2. Try Navbar Placeholder
        nav_placeholder = soup.find('div', id='navbar-placeholder')
        if nav_placeholder:
             nav_placeholder.insert_after(full_new_soup)
        else:
            # 3. Fallback: Before footer
            footer = soup.find('footer')
            if not footer:
                footer = soup.find('div', id='footer-placeholder')
            
            if footer:
                footer.insert_before(full_new_soup)
            else:
                # 4. Body append
                if not soup.body:
                    soup.append(soup.new_tag("body"))
                
                # Careful not to wipe scripts if we clear body.
                # Previous logic cleared body. Let's try to be smarter.
                # If we couldn't find an insertion point, we probably shouldn't wipe everything.
                # But for now, let's stick to the established pattern but safer.
                
                # Append elements from the new soup individually
                for element in list(full_new_soup.contents):
                    soup.body.append(element)

    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(str(soup))

def export_all():
    count = 0
    for root, dirs, files in os.walk(ADMIN_DATA_DIR):
        for file in files:
            if file.endswith('.json'):
                json_path = os.path.join(root, file)
                export_single_page(json_path)
                count += 1
    print(f"\nExport complete! Processed {count} pages.")

if __name__ == "__main__":
    export_all()
