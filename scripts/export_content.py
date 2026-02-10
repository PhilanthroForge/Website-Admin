
import os
import json
from bs4 import BeautifulSoup

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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
        if block.get('type') == 'text':
            # It's a raw HTML block or WYSIWYG content
            new_html_content += block.get('content', '') + "\n"
        elif block.get('type') == 'hero':
             # Fallback for structured blocks if we add them later
             new_html_content += f"<section class='hero'>{block.get('heading')}</section>\n"
        # Add other types as needed
        
    # Read existing HTML Template
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        original_html = f.read()
        
    soup = BeautifulSoup(original_html, 'html.parser')
    
    # We need to replace ALL sections between Navbar and Footer with new_html_content
    # Strategy: Find the first section, insert new content before it, then remove all old sections.
    # OR: Identify a wrapper.
    # index.html doesn't have a wrapper. We should probably wrap it first.
    
    # Let's clean up: remove all existing <section> tags
    for section in soup.find_all('section'):
        section.decompose()
        
    # Insert new content
    # We need to find WHERE to insert. 
    # After the mobile menu navigation or navbar placeholder.
    # Looking at index.html, the hero comes after line 441 </nav>
    
    # Find the nav element or the mobile menu panel
    anchor = soup.find('nav', {'aria-label': 'Mobile navigation'})
    if anchor:
        # The nav is inside #mobile-menu-panel
        parent = anchor.find_parent('div', id='mobile-menu-panel')
        if parent:
             # The mobile menu panel is a sibling of the hero?
             # No, hero is line 443. #mobile-menu-panel is line 347.
             # Actually, simpler: Insert after content container or body start?
             # The file structure is: body > navbar > ... > mobile-menu-panel > SECTION > SECTION
             pass
             
    # Fallback: Find body, append new content, but before footer?
    # Where is the footer?
    footer = soup.find('footer')
    
    full_new_soup = BeautifulSoup(new_html_content, 'html.parser')
    
    if footer:
        footer.insert_before(full_new_soup)
    else:
        # If no footer tag, append to body
        soup.body.append(full_new_soup)
        
    # Formatting
    # This might mess up indentation, but functionality is key.
    
    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(str(soup))
        
    print(f"Successfully exported {len(content_blocks)} blocks to index.html")

if __name__ == "__main__":
    export_content()
