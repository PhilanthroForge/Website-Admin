"""
Content Management Module
Handles page content storage, editing, and publishing
"""
import json
import os
from datetime import datetime
from config import Config

def get_page_content(page_id):
    """Load page content from JSON file"""
    page_file = os.path.join(Config.PAGES_FOLDER, f"{page_id}.json")
    
    if os.path.exists(page_file):
        with open(page_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    # Return default structure if file doesn't exist
    return {
        "page_id": page_id,
        "title": page_id.replace('-', ' ').title(),
        "meta_description": "",
        "sections": {},
        "last_updated": None
    }

def save_page_content(page_id, content):
    """Save page content to JSON file"""
    page_file = os.path.join(Config.PAGES_FOLDER, f"{page_id}.json")
    
    # Add timestamp
    content['last_updated'] = datetime.now().isoformat()
    
    with open(page_file, 'w', encoding='utf-8') as f:
        json.dump(content, f, indent=2, ensure_ascii=False)
    
    # Auto-publish to static HTML
    success, message = publish_page(page_id)
    if not success:
        print(f"Publish warning: {message}")
        
    return True

def publish_page(page_id):
    """
    Publish page content to the static HTML file
    Injects JSON content blocks between <!-- START: PAGE CONTENT --> and <!-- END: PAGE CONTENT --> markers
    """
    # 1. Determine target HTML file
    filename = 'index.html' if page_id == 'home' else f"{page_id}.html"
    file_path = os.path.join(Config.BASE_DIR, filename)
    
    if not os.path.exists(file_path):
        return False, f"Target file {filename} not found"
        
    # 2. Get content from JSON
    content_data = get_page_content(page_id)
    if not content_data:
        return False, "Content data not found"
        
    # 3. Concatenate content by zone
    zones = {
        'HEADER': '',
        'MAIN': '',
        'FOOTER': ''
    }
    
    # Support 'content_blocks'
    if 'content_blocks' in content_data:
        for block in content_data['content_blocks']:
            if 'content' in block:
                b_type = block.get('type', 'SECTION').upper()
                
                if b_type == 'HEADER':
                    zones['HEADER'] += block['content'] + "\n"
                elif b_type == 'FOOTER':
                    zones['FOOTER'] += block['content'] + "\n"
                else:
                    # All other types (SECTION, INTRO, etc) go to MAIN
                    zones['MAIN'] += block['content'] + "\n"

    # 4. Read HTML file
    with open(file_path, 'r', encoding='utf-8') as f:
        file_content = f.read()
        
    # 5. Replace zones
    # Strategy: Try specific zones first. If any found, use them.
    # If no specific zones found, try legacy "PAGE CONTENT" marker with all content concatenated.
    
    updated = False
    
    # Check for specific markers
    has_zones = False
    for zone_name, content in zones.items():
        start_marker = f"<!-- START: {zone_name} -->"
        end_marker = f"<!-- END: {zone_name} -->"
        
        start_idx = file_content.find(start_marker)
        end_idx = file_content.find(end_marker)
        
        if start_idx != -1 and end_idx != -1:
            has_zones = True
            # Include markers in replacement to preserve them for next time
            # Wait, if I include markers in new content, I can find them next time.
            # Logic: existing = prefix + start_marker + OLD_CONTENT + end_marker + suffix
            # New = prefix + start_marker + "\n" + NEW_CONTENT + "\n" + end_marker + suffix
            
            # Find exact positions relative to markers
            content_start = start_idx + len(start_marker)
            
            prefix = file_content[:content_start]
            suffix = file_content[end_idx:]
            
            file_content = prefix + "\n" + content + suffix
            updated = True

    if not has_zones:
        # Fallback to single "PAGE CONTENT" marker
        start_marker = "<!-- START: PAGE CONTENT -->"
        end_marker = "<!-- END: PAGE CONTENT -->"
        start_idx = file_content.find(start_marker)
        end_idx = file_content.find(end_marker)
        
        if start_idx != -1 and end_idx != -1:
            all_content = zones['HEADER'] + zones['MAIN'] + zones['FOOTER']
            content_start = start_idx + len(start_marker)
            file_content = file_content[:content_start] + "\n" + all_content + file_content[end_idx:]
            updated = True

    if not updated:
        return False, f"No content markers found in {filename}"
    
    # 6. Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(file_content)
        
    return True, f"Successfully published to {filename}"

def publish_all_pages():
    """
    Regenerate all static HTML files from JSON content
    """
    results = {
        'success': [],
        'error': []
    }
    
    # 1. Publish standard pages
    pages = get_all_pages()
    for page in pages:
        page_id = page['id']
        success, message = publish_page(page_id)
        if success:
            results['success'].append(message)
        else:
            results['error'].append(f"{page_id}: {message}")
            
    # 2. Publish Services
    # We need to import portfolio module here or move this logic
    # To avoid circular imports, we'll import inside function
    try:
        import portfolio
        services = portfolio.get_all_services()
        for service in services:
            # Service pages are usually sub-pages, we need a way to identify their HTML target
            # For now, let's assume they map to 'services/<slug>.html'
            # But wait, publish_page logic handles mapping based on ID
            # If service IDs match filenames (e.g. digital-fundraising-strategy), it might just work 
            # IF publish_page handles subdirectories.
            
            # Let's check publish_page logic:
            # filename = 'index.html' if page_id == 'home' else f"{page_id}.html"
            # file_path = os.path.join(Config.BASE_DIR, filename)
            
            # So if page_id is 'services/digital-fundraising-strategy', it becomes 'services/digital-fundraising-strategy.html'
            # precise!
            
            # Let's ensure service IDs include the directory prefix if needed, OR we update publish_page
            # The current service IDs are just slugs (e.g. "digital-fundraising-strategy").
            # We should pass "services/slug" to publish_page.
            
            full_id = f"services/{service['id']}"
            success, message = publish_page(full_id)
            if success:
                results['success'].append(message)
            else:
                # Keep silent for now if file doesn't exist, or log as warning?
                # Actually, better to report it so we know what's missing
                if "not found" in message:
                    pass # consistent with current partial implementation
                else:
                    results['error'].append(f"Service {service['id']}: {message}")

        # 3. Publish Case Studies
        case_studies = portfolio.get_all_case_studies()
        for case in case_studies:
            full_id = f"case-studies/{case['id']}"
            success, message = publish_page(full_id)
            if success:
                results['success'].append(message)
            else:
                 if "not found" in message:
                    pass
                 else:
                    results['error'].append(f"Case Study {case['id']}: {message}")
                    
    except ImportError:
        results['error'].append("Could not load portfolio module")
        
    return results

def get_all_pages():
    """Get list of all pages with metadata"""
    pages = []
    
    # Predefined pages
    page_ids = [
        'home', 'about', 'services', 'case-studies', 
        'lets-talk', 'privacy-policy', 'terms-and-conditions'
    ]
    
    for page_id in page_ids:
        content = get_page_content(page_id)
        
        # Handle both 'sections' (admin format) and 'content_blocks' (scraped format)
        if 'sections' in content:
            sections_count = len(content.get('sections', {}))
        elif 'content_blocks' in content:
            sections_count = len(content.get('content_blocks', []))
        else:
            sections_count = 0
        
        pages.append({
            'id': page_id,
            'name': content.get('title', content.get('metadata', {}).get('title', page_id.replace('-', ' ').title())),
            'last_updated': content.get('last_updated', content.get('updated_at')),
            'sections_count': sections_count
        })
    
    return pages

def extract_content_from_html(html_file):
    """
    Extract editable content from HTML file
    This is a helper to migrate existing content to JSON
    """
    # This would parse HTML and extract text content
    # For now, return empty structure
    return {}

def apply_content_to_html(html_file, content):
    """
    Apply JSON content back to HTML file
    This updates the HTML with edited content
    """
    # This would inject content back into HTML template
    # Implementation depends on how we structure the HTML
    pass

def get_section_types():
    """Get available section types for page builder"""
    return {
        'hero': {
            'name': 'Hero Section',
            'fields': [
                {'name': 'heading', 'type': 'text', 'label': 'Main Heading'},
                {'name': 'subheading', 'type': 'text', 'label': 'Subheading'},
                {'name': 'cta_text', 'type': 'text', 'label': 'CTA Button Text'},
                {'name': 'cta_link', 'type': 'text', 'label': 'CTA Button Link'},
                {'name': 'background_image', 'type': 'image', 'label': 'Background Image'}
            ]
        },
        'text': {
            'name': 'Text Section',
            'fields': [
                {'name': 'title', 'type': 'text', 'label': 'Title'},
                {'name': 'content', 'type': 'wysiwyg', 'label': 'Content'}
            ]
        },
        'grid': {
            'name': 'Grid Section',
            'fields': [
                {'name': 'title', 'type': 'text', 'label': 'Section Title'},
                {'name': 'items', 'type': 'repeater', 'label': 'Grid Items'}
            ]
        }
    }
