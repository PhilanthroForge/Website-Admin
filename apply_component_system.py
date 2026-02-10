#!/usr/bin/env python3
"""
Script to replace hardcoded nav/footer with component placeholders
"""

import os
import re
from pathlib import Path

# Base directory
BASE_DIR = Path("/Users/bipashahalder/Documents/Philanthroforge_Complete_Clone")

# HTML files to process
HTML_FILES = [
    "index.html",
    "about.html",
    "services.html",
    "case-studies.html",
    "lets-talk.html",
    "privacy-policy.html",
    "terms-and-conditions.html",
    "404.html",
    # Service pages
    "services/digital-fundraising-strategy.html",
    "services/consultancy-advisory.html",
    "services/donation-form-optimization.html",
    "services/website-donation-optimization.html",
    "services/fundraising-campaign-journey-design.html",
    "services/donor-behaviour-analysis-revenue-growth.html",
    "services/brand-identity-impact-communication.html",
    "services/csr-major-donor-support.html",
    # Case studies
    "case-studies/rewarding-generosity.html",
    "case-studies/integrated-ecosystems.html",
    "case-studies/turning-supporters-into-fundraisers.html",
]

def get_script_src(filepath):
    """Determine correct path to components.js based on file location"""
    if '/' in filepath:
        return "../js/components.js"
    return "js/components.js"

def process_html_file(filepath):
    """Replace nav and footer with component placeholders"""
    full_path = BASE_DIR / filepath
    
    if not full_path.exists():
        print(f"❌ File not found: {filepath}")
        return False
    
    print(f"📝 Processing: {filepath}")
    
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_length = len(content)
        
        # Replace nav section - find opening <nav> and closing </nav>
        # Look for nav with class containing 'nordic-nav' or 'nav' followed by content until closing </nav>
        nav_pattern = r'<nav[^>]*>.*?</nav>\s*'
        nav_replacement = '    <!-- Navigation Component -->\n    <div id="navbar-placeholder"></div>\n\n'
        
        content = re.sub(nav_pattern, nav_replacement, content, flags=re.DOTALL)
        
        # Replace footer section - find opening <footer> and closing </footer>
        footer_pattern = r'<footer[^>]*>.*?</footer>\s*'
        footer_replacement = '    <!-- Footer Component -->\n    <div id="footer-placeholder"></div>\n\n'
        
        content = re.sub(footer_pattern, footer_replacement, content, flags=re.DOTALL)
        
        # Add component loader script before closing </body> if not already present
        script_src = get_script_src(filepath)
        component_script = f'<script src="{script_src}"></script>'
        
        if component_script not in content:
            # Find </body> and insert before it
            content = content.replace('</body>', f'    {component_script}\n</body>')
        
        # Remove duplicate mobile-menu.js script references
        content = re.sub(r'\s*<script src="\.\.?/mobile-menu\.js"></script>', '', content)
        content = re.sub(r'\s*<script src="mobile-menu\.js"></script>', '', content)
        
        new_length = len(content)
        reduction = original_length - new_length
        
        # Write back
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ {filepath}: Reduced by {reduction} characters ({reduction // 1024}KB)")
        return True
        
    except Exception as e:
        print(f"❌ Error processing {filepath}: {e}")
        return False

def main():
    print("=" * 60)
    print("Component System Implementation")
    print("=" * 60)
    print(f"\nProcessing {len(HTML_FILES)} HTML files...\n")
    
    success_count = 0
    for filepath in HTML_FILES:
        if process_html_file(filepath):
            success_count += 1
    
    print("\n" + "=" * 60)
    print(f"✅ Successfully processed: {success_count}/{len(HTML_FILES)} files")
    print("=" * 60)
    
    print("\n📊 Summary:")
    print(f"  • Navigation: Now loaded from /components/navbar.html")
    print(f"  • Footer: Now loaded from /components/footer.html")
    print(f"  • Loader: components.js injected in all pages")
    print(f"\n💡 To update nav/footer site-wide:")
    print(f"  • Edit: /components/navbar.html")
    print(f"  • Edit: /components/footer.html")
    print(f"  • Changes reflect automatically on all {len(HTML_FILES)} pages!")

if __name__ == "__main__":
    main()
