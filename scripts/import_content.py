
import os
import json
import re
from bs4 import BeautifulSoup

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML_FILE = os.path.join(BASE_DIR, 'index.html')
JSON_FILE = os.path.join(BASE_DIR, 'admin', 'data', 'pages', 'home.json')

def import_content():
    if not os.path.exists(HTML_FILE):
        print(f"Error: {HTML_FILE} not found")
        return

    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Identify content sections
    # We assume content starts after the navbar and ends before the footer
    # Navbar has id "navbar-placeholder" or class "nav" or similar. 
    # In this file, we see <!-- Navigation Component --> and <!-- Mobile Menu -->
    # The first <section> is the Hero.
    
    sections = soup.find_all('section')
    
    content_blocks = []
    
    for i, section in enumerate(sections):
        # Determine a heading for the block
        heading = "Section " + str(i+1)
        h_tag = section.find(['h1', 'h2', 'h3'])
        if h_tag:
            heading = h_tag.get_text(strip=True)[:50]
            
        # We save the entire section HTML as a "code" or "raw" block if possible, 
        # but the current builder supports 'hero', 'text', 'images'.
        # To preserve exact design, we might need to store it as a 'text' block with the HTML.
        # However, the CSS classes need to optionally be preserved.
        # The 'text' block in existing content.py puts content in a 'wysiwyg' field.
        
        block = {
            "type": "text", # Generic type that supports HTML
            "heading": heading,
            "content": str(section), # Save the full HTML of the section
            "images": []
        }
        content_blocks.append(block)

    # Save to JSON
    data = {
        "metadata": {
            "url": "https://www.philanthroforge.com/home",
            "title": "PhilanthroForge - Home",
            "slug": "index",
            "parent_section": "root" 
        },
        "content_blocks": content_blocks
    }
    
    os.makedirs(os.path.dirname(JSON_FILE), exist_ok=True)
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
        
    print(f"Successfully imported {len(content_blocks)} sections from index.html to home.json")

if __name__ == "__main__":
    import_content()
