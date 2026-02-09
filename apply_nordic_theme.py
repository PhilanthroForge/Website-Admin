#!/usr/bin/env python3
"""
Apply Nordic theme nav/footer to all HTML pages
"""

import os
import re

# Directory containing HTML files
html_dir = "/Users/bipashahalder/Documents/Philanthroforge_Complete_Clone"

# Patterns to replace
replacements = [
    # Nav patterns
    (
        r'<nav\s+class="bg-primary\s+text-white[^"]*"',
        '<nav class="nordic-nav sticky top-0 z-50 transition-all duration-300"'
    ),
    (
        r'<footer\s+class="bg-primary\s+text-white[^"]*"',
        '<footer class="nordic-footer py-16 mt-auto relative overflow-hidden"'
    ),
]

def update_html_file(filepath):
    """Update a single HTML file with Nordic theme"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Apply replacements
        for pattern, replacement in replacements:
            content = re.sub(pattern, replacement, content)
        
        # Only write if changes were made
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Updated: {os.path.basename(filepath)}")
            return True
        else:
            print(f"- No changes needed: {os.path.basename(filepath)}")
            return False
    except Exception as e:
        print(f"✗ Error updating {filepath}: {e}")
        return False

def main():
    """Main function to update all HTML files"""
    updated_count = 0
    
    # Walk through all directories
    for root, dirs, files in os.walk(html_dir):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                if update_html_file(filepath):
                    updated_count += 1
    
    print(f"\n{'='*50}")
    print(f"Updated {updated_count} HTML files with Nordic theme")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()
