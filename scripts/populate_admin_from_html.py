import os
import json
import re
from pathlib import Path
from html.parser import HTMLParser

# Base directory setup: Assumes script is in /scripts/
BASE_DIR = Path(__file__).resolve().parent.parent
ADMIN_DATA_DIR = BASE_DIR / 'admin' / 'data'
PAGES_DIR = ADMIN_DATA_DIR / 'pages'
SERVICES_DIR = ADMIN_DATA_DIR / 'services'
CASES_DIR = ADMIN_DATA_DIR / 'case-studies'

# Ensure directories exist
for d in [PAGES_DIR, SERVICES_DIR, CASES_DIR]:
    d.mkdir(parents=True, exist_ok=True)
    (PAGES_DIR / 'services').mkdir(parents=True, exist_ok=True)
    (PAGES_DIR / 'case-studies').mkdir(parents=True, exist_ok=True)

class SimpleHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.title = ""
        self.h1 = ""
        self.hero_image = ""
        self.capture_title = False
        self.capture_h1 = False
        
    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)
        attrs_dict = dict(attrs)
        
        if tag == 'title':
            self.capture_title = True
        elif tag == 'h1':
            self.capture_h1 = True
        
        # Try to find hero image
        if tag == 'img' and not self.hero_image:
            # Heuristic: first large image or one with 'hero' in src/alt/class
            src = attrs_dict.get('src', '')
            alt = attrs_dict.get('alt', '').lower()
            cls = attrs_dict.get('class', '').lower()
            if 'hero' in src.lower() or 'hero' in alt or 'hero' in cls:
                self.hero_image = src
            elif not self.hero_image and ('banner' in src.lower() or 'header' in src.lower()):
                 self.hero_image = src

    def handle_endtag(self, tag):
        if self.tags:
            self.tags.pop()
        if tag == 'title':
            self.capture_title = False
        elif tag == 'h1':
            self.capture_h1 = False
            
    def handle_data(self, data):
        if self.capture_title:
            self.title += data.strip() + " "
        elif self.capture_h1:
            self.h1 += data.strip() + " "

def extract_metadata(html_content):
    parser = SimpleHTMLParser()
    try:
        parser.feed(html_content)
    except Exception as e:
        print(f"Error parsing HTML metadata: {e}")
        
    return {
        'title': parser.title.strip(),
        'subtitle': parser.h1.strip(),
        'image': parser.hero_image
    }

def split_into_sections(html_content):
    """
    Split HTML into logical sections for content_blocks.
    Returns a list of dicts: {'type': '...', 'content': '...'}
    """
    blocks = []
    
    # 1. Header
    header_match = re.search(r'(<header.*?</header>)', html_content, re.DOTALL)
    if header_match:
        blocks.append({
            'type': 'HEADER', 
            'heading': 'Page Header',
            'content': '<div id="navbar-placeholder"></div>\n' + header_match.group(1),
            'images': [] 
        })
    else:
        # If no explicit header tag, looks for navbar placeholder
        if 'navbar-placeholder' in html_content:
             blocks.append({
                'type': 'HEADER',
                'heading': 'Navigation',
                'content': '<div id="navbar-placeholder"></div>',
                'images': []
            })
    
    # 2. Main Sections
    # Find all <section> tags
    section_matches = re.finditer(r'(<section.*?</section>)', html_content, re.DOTALL)
    for i, match in enumerate(section_matches):
        section_content = match.group(1)
        # Try to find a heading for the block
        heading_match = re.search(r'<h[23][^>]*>(.*?)</h[23]>', section_content)
        heading = heading_match.group(1) if heading_match else f"Section {i+1}"
        
        # Clean heading
        heading = re.sub(r'<[^>]+>', '', heading).strip()
        
        blocks.append({
            'type': 'SECTION',
            'heading': heading,
            'content': section_content,
            'images': [] 
        })
    
    # 3. Footer
    blocks.append({
        'type': 'FOOTER',
        'heading': 'Footer',
        'content': '<div id="footer-placeholder"></div>',
        'images': []
    })
    
    return blocks

def process_file(file_path):
    print(f"Processing {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return

    meta = extract_metadata(content)
    sections = split_into_sections(content)
    
    # Determine type and slug
    filename = file_path.name
    stem = file_path.stem
    
    if 'services' in str(file_path.parent):
        category = 'services'
        slug = f"services/{stem}"
    elif 'case-studies' in str(file_path.parent):
        category = 'case-studies'
        slug = f"case-studies/{stem}"
    else:
        category = None
        slug = stem if stem != 'index' else 'home'
    
    # 1. Generate Page JSON (for Page Builder)
    page_data = {
        "metadata": {
            "url": f"https://www.philanthroforge.com/{slug}.html" if slug != 'home' else "https://www.philanthroforge.com/",
            "title": meta['title'],
            "slug": slug
        },
        "content_blocks": sections
    }
    
    # Determine output path for Page JSON
    if category:
        out_dir = PAGES_DIR / category
        out_json = out_dir / f"{stem}.json"
    else:
        out_json = PAGES_DIR / f"{slug}.json"
        
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(page_data, f, indent=4)
        print(f"  -> Page JSON: {out_json.relative_to(BASE_DIR)}")

    # 2. Generate Module JSON (Services/Cases)
    if category:
        # Extract a description (first P after H1 roughly)
        description = ""
        # Improved description extraction: Find first substantial paragraph in first section
        # or use metadata description if available (parsed from meta tag? - not implemented yet)
        
        # Heuristic: First <p> tag in the file that isn't in header/nav?
        # Or just use the one after H1.
        h1_match = re.search(r'<h1.*?>(.*?)</h1>', content, re.DOTALL)
        if h1_match:
            end_h1 = h1_match.end()
            p_match = re.search(r'<p[^>]*>(.*?)</p>', content[end_h1:], re.DOTALL)
            if p_match:
                description = re.sub(r'<[^>]+>', '', p_match.group(1)).strip()
        
        item_data = {
            "id": stem,
            "title": meta['title'].split(' - ')[0].strip(),
            "subtitle": meta['subtitle'].replace('  ', ' ').strip(),
            "description": description,
            "image": meta['image'],
            "url": f"{slug}.html",
            "status": "published",
            "order": 0,
            "features": [],
        }
        
        if category == 'case-studies':
            item_data.update({
                'client': "Client Name",
                'industry': "Non-Profit",
                'challenge': "Challenge details...",
                'solution': "Solution details...",
                'results': []
            })
            out_path = CASES_DIR / f"{stem}.json"
        else:
            out_path = SERVICES_DIR / f"{stem}.json"
            
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(item_data, f, indent=4)
            print(f"  -> Module JSON: {out_path.relative_to(BASE_DIR)}")

def main():
    print("Starting Admin Data Population...")
    
    # 1. Root Pages
    for f in BASE_DIR.glob('*.html'):
        if f.name in ['404.html']: continue
        process_file(f)
        
    # 2. Services
    for f in (BASE_DIR / 'services').glob('*.html'):
        process_file(f)

    # 3. Case Studies
    for f in (BASE_DIR / 'case-studies').glob('*.html'):
        process_file(f)
        
    print("Done.")

if __name__ == "__main__":
    main()
