
import os
import json
from bs4 import BeautifulSoup

BASE_DIR = '/Users/bipashahalder/Documents/Philanthroforge_Complete_Clone'
HTML_FILE = os.path.join(BASE_DIR, 'index.html')
JSON_FILE = os.path.join(BASE_DIR, 'admin', 'data', 'pages', 'home.json')

def export_content():
    if not os.path.exists(JSON_FILE):
        print(f"Error: {JSON_FILE} not found")
        return

    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    content_blocks = data.get('content_blocks', [])
    
    # Generate HTML from blocks
    new_html_content = ""
    for block in content_blocks:
        content = block.get('content', '')
        # Ensure we don't duplicate section tags if user added them manually in WYSIWYG
        if content:
             new_html_content += content + "\n"
        # Since we import as full HTML, we export as full HTML
        
    # Read existing HTML Template
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        original_html = f.read()
        
    soup = BeautifulSoup(original_html, 'html.parser')
    
    # Remove existing sections
    # Note: This removes ALL sections. If header/footer use section tags, they will be removed!
    # index.html header uses <div id="navbar-placeholder"> or similar? No, <nav> component.
    # index.html footer uses <footer>
    # So removing <section> is safe for main content.
    
    sections = soup.find_all('section')
    if not sections:
        print("Warning: No existing sections found to replace. Appending to body.")
    
    for section in sections:
        section.decompose()
        
    # Insert new content
    full_new_soup = BeautifulSoup(new_html_content, 'html.parser')
    
    # Find insertion point: After Navigation
    # We look for the Mobile Menu Panel div which is arguably end of header
    mobile_menu = soup.find('div', id='mobile-menu-panel')
    
    if mobile_menu:
        mobile_menu.insert_after(full_new_soup)
    else:
        # Fallback: Before footer
        footer = soup.find('footer')
        if footer:
            footer.insert_before(full_new_soup)
        else:
            if not soup.body:
                soup.append(soup.new_tag("body"))
            
            soup.body.clear()
            
            # Append elements from the new soup individually
            # We need to list() the contents because modifying the tree while iterating can be problematic
            for element in list(full_new_soup.contents):
                # We need to extract the element from its current parent (full_new_soup) before appending
                # but append() usually handles reparenting. Let's try appending directly.
                soup.body.append(element)

    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(str(soup))
        
    print(f"Successfully exported {len(content_blocks)} blocks to index.html")

if __name__ == "__main__":
    export_content()
