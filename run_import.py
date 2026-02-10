
import os
import json
import re
from bs4 import BeautifulSoup

# Use absolute path to avoid ambiguity
BASE_DIR = '/Users/bipashahalder/Documents/Philanthroforge_Complete_Clone'
HTML_FILE = os.path.join(BASE_DIR, 'index.html')
JSON_FILE = os.path.join(BASE_DIR, 'admin', 'data', 'pages', 'home.json')

import os
import json
import re
from bs4 import BeautifulSoup

# Use absolute path to avoid ambiguity
BASE_DIR = '/Users/bipashahalder/Documents/Philanthroforge_Complete_Clone'
ADMIN_DATA_DIR = os.path.join(BASE_DIR, 'admin', 'data', 'pages')

SKIP_DIRS = {'.git', '.agent', 'admin', 'node_modules', '.gemini', '.vscode'}

def import_all_pages():
    print(f"Starting import from {BASE_DIR}...")
    count = 0
    
    for root, dirs, files in os.walk(BASE_DIR):
        # Prune skip dirs
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        
        for file in files:
            if file.endswith('.html'):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, BASE_DIR)
                
                # Calculate slug (remove .html, handle index)
                slug = rel_path.replace('.html', '')
                if slug.endswith('index'):
                    slug = slug[:-5] if slug != 'index' else 'home' # index -> home, sub/index -> sub/
                    slug = slug.rstrip('/')
                
                # Handle root index specifically as 'home'
                if rel_path == 'index.html':
                    slug = 'home'
                
                import_single_page(full_path, slug)
                count += 1
                
    print(f"\nImport complete! Processed {count} pages.")

def import_single_page(filepath, slug):
    print(f"Processing {slug} ({filepath})...")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    
    content_blocks = []
    
    # 1. Capture Header (Custom logic for index.html structure)
    # The header is in a div with "container mx-auto px-6 py-4 flex justify-between items-center relative"
    # But checking for 'header' tag first is safer if we move to semantic HTML.
    header = soup.find('header')
    if not header:
        # Look for the specific nav container
        # <div class="container mx-auto px-6 py-4 ..."> containing <a href="index.html">...<img ... Philanthro logo>
        for div in soup.find_all('div', class_='container'):
            if div.find('img', alt=re.compile('Philanthro', re.I)):
                # This is likely the navbar container
                # Check if it is inside the body directly or close to it
                header = div.parent if div.parent.name == 'div' and 'navbar-placeholder' in str(div.parent.previous_sibling) else div
                break
    
    if header:
         content_blocks.append({
            "type": "HEADER", 
            "heading": "Page Header / Navigation",
            "content": str(header), 
            "images": [{"src": img['src'], "alt": img.get('alt','')} for img in header.find_all('img') if img.get('src')]
        })

    sections = soup.find_all('section')
    if not sections:
        # Fallback: maybe it's just a div container?
        main_content = soup.find('main')
        if main_content:
            sections = main_content.find_all('section') or [main_content]
            
    for i, section in enumerate(sections):
        # Determine a heading for the block
        heading = f"Section {i+1}"
        type_label = "SECTION"
        
        # Try finding a heading tag
        h_tag = section.find(['h1', 'h2', 'h3'])
        if h_tag:
            heading = h_tag.get_text(strip=True)[:50]
        
        # Check if it has a specific ID or class to clue us in
        if section.get('id'):
            heading += f" ({section.get('id')})"
        
        # Extract images for the block metadata (optional, but good for UI)
        imgs = []
        for img in section.find_all('img'):
            src = img.get('src')
            if src:
                # Ensure src is relative to root or absolute
                if not src.startswith('/') and not src.startswith('http'):
                     # content is strictly HTML, the browser resolves relative to current URL.
                     # But admin panel is at /admin/pages/..., so relative links break.
                     # We should probably ensure src starts with /.
                     # However, 'assets/...' in the content refers to root.
                     pass
                imgs.append({'src': src, 'alt': img.get('alt', '')})

        block = {
            "type": type_label, 
            "heading": heading,
            "content": str(section), 
            "images": imgs
        }
        content_blocks.append(block)
        
    # 2. Capture Footer
    footer = soup.find('footer')
    if footer:
        content_blocks.append({
            "type": "FOOTER",
            "heading": "Page Footer",
            "content": str(footer),
            "images": []
        })

    # Save to JSON
    json_path = os.path.join(ADMIN_DATA_DIR, f"{slug}.json")
    os.makedirs(os.path.dirname(json_path), exist_ok=True)
    
    data = {
        "metadata": {
            "url": f"https://www.philanthroforge.com/{slug.replace('home', '')}",
            "title": soup.title.string if soup.title else slug,
            "slug": slug
        },
        "content_blocks": content_blocks
    }
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    import_all_pages()
