#!/usr/bin/env python3
"""
Admin Panel Data Migration Script

Migrates content from the JSON data folder to the admin panel's data structure.
This includes pages, services, case studies, components, and images.
"""

import os
import json
import shutil
from datetime import datetime

# Paths
SOURCE_DATA = "/Users/bipashahalder/Downloads/Philanthroforge_JSON_Data"
ADMIN_DATA = "/Users/bipashahalder/Documents/Philanthroforge_Complete_Clone/admin/data"
SOURCE_ASSETS = "/Users/bipashahalder/Documents/Philanthroforge_Complete_Clone/assets"
ADMIN_ASSETS = "/Users/bipashahalder/Documents/Philanthroforge_Complete_Clone/admin/uploads"

def ensure_directories():
    """Create necessary admin data directories"""
    os.makedirs(f"{ADMIN_DATA}/pages", exist_ok=True)
    os.makedirs(f"{ADMIN_DATA}/services", exist_ok=True)
    os.makedirs(f"{ADMIN_DATA}/case-studies", exist_ok=True)
    os.makedirs(f"{ADMIN_DATA}/components", exist_ok=True)
    os.makedirs(ADMIN_ASSETS, exist_ok=True)
    print("✓ Created admin data directories")

def migrate_pages():
    """Migrate page JSON files"""
    print("\n📄 Migrating Pages...")
    
    page_files = {
        'index.json': 'home.json',
        'about.json': 'about.json',
        'services.json': 'services.json',
        'case-studies.json': 'case-studies.json',
        'lets-talk.json': 'lets-talk.json',
        'privacy-policy.json': 'privacy-policy.json',
        'terms-and-conditions.json': 'terms-and-conditions.json'
    }
    
    for source_name, dest_name in page_files.items():
        source_path = f"{SOURCE_DATA}/{source_name}"
        dest_path = f"{ADMIN_DATA}/pages/{dest_name}"
        
        if os.path.exists(source_path):
            shutil.copy2(source_path, dest_path)
            print(f"  ✓ {source_name} → {dest_name}")
        else:
            print(f"  ✗ {source_name} not found")
    
    print(f"✓ Migrated {len([f for f in page_files.values() if os.path.exists(f'{ADMIN_DATA}/pages/{f}')])} pages")

def migrate_services():
    """Migrate service JSON files"""
    print("\n🛠️  Migrating Services...")
    
    service_files = [
        'services_brand-identity-impact-messaging.json',
        'services_consultancy-advisory.json',
        'services_csr-major-donor-support.json',
        'services_digital-fundraising-strategy.json',
        'services_donation-form-optimization.json',
        'services_donor-behaviour-analysis-revenue-growth.json',
        'services_fundraising-campaign-design.json',
        'services_website-donation-optimization.json'
    ]
    
    count = 0
    for filename in service_files:
        source_path = f"{SOURCE_DATA}/{filename}"
        # Remove 'services_' prefix from destination
        dest_name = filename.replace('services_', '')
        dest_path = f"{ADMIN_DATA}/services/{dest_name}"
        
        if os.path.exists(source_path):
            shutil.copy2(source_path, dest_path)
            print(f"  ✓ {filename}")
            count += 1
        else:
            print(f"  ✗ {filename} not found")
    
    print(f"✓ Migrated {count} services")

def migrate_case_studies():
    """Migrate case study JSON files"""
    print("\n📋 Migrating Case Studies...")
    
    case_study_files = [
        'case-studies_integrated-ecosystems.json',
        'case-studies_rewarding-generosity.json',
        'case-studies_turning-supporters-into-champions.json'
    ]
    
    count = 0
    for filename in case_study_files:
        source_path = f"{SOURCE_DATA}/{filename}"
        # Remove 'case-studies_' prefix from destination
        dest_name = filename.replace('case-studies_', '')
        dest_path = f"{ADMIN_DATA}/case-studies/{dest_name}"
        
        if os.path.exists(source_path):
            shutil.copy2(source_path, dest_path)
            print(f"  ✓ {filename}")
            count += 1
        else:
            print(f"  ✗ {filename} not found")
    
    print(f"✓ Migrated {count} case studies")

def migrate_components():
    """Extract and migrate navbar and footer from HTML components"""
    print("\n🧩 Migrating Components...")
    
    # For now, create basic component structures
    # These will need to be manually populated or extracted from HTML
    
    navbar_data = {
        "logo": {
            "text": "PhilanthroForge",
            "image": ""
        },
        "links": [
            {"text": "Home", "url": "/"},
            {"text": "About", "url": "/about.html"},
            {"text": "Services", "url": "/services.html", "hasDropdown": True},
            {"text": "Case Studies", "url": "/case-studies.html"},
            {"text": "Contact", "url": "/lets-talk.html"}
        ],
        "cta": {
            "text": "Let's Talk",
            "url": "/lets-talk.html"
        },
        "updated_at": datetime.now().isoformat()
    }
    
    footer_data = {
        "company": {
            "name": "PhilanthroForge",
            "tagline": "Forging the Next Era of Fundraising",
            "description": "Expert nonprofit fundraising consultants helping organizations transform their fundraising strategy."
        },
        "contact": {
            "email": "info@philanthroforge.com",
            "phone": "+1 (555) 123-4567",
            "address": "123 Main Street, City, State 12345"
        },
        "social": {
            "linkedin": "https://linkedin.com/company/philanthroforge",
            "twitter": "",
            "facebook": "",
            "instagram": ""
        },
        "links": {
            "services": [
                {"text": "Digital Fundraising", "url": "/services/digital-fundraising-strategy.html"},
                {"text": "Donor Analysis", "url": "/services/donor-behaviour-analysis-revenue-growth.html"},
                {"text": "Website Optimization", "url": "/services/website-donation-optimization.html"}
            ],
            "company": [
                {"text": "About Us", "url": "/about.html"},
                {"text": "Case Studies", "url": "/case-studies.html"},
                {"text": "Contact", "url": "/lets-talk.html"}
            ],
            "legal": [
                {"text": "Privacy Policy", "url": "/privacy-policy.html"},
                {"text": "Terms & Conditions", "url": "/terms-and-conditions.html"}
            ]
        },
        "copyright": f"© {datetime.now().year} PhilanthroForge. All rights reserved.",
        "updated_at": datetime.now().isoformat()
    }
    
    # Save components
    with open(f"{ADMIN_DATA}/components/navbar.json", 'w') as f:
        json.dump(navbar_data, f, indent=2)
    print("  ✓ navbar.json created")
    
    with open(f"{ADMIN_DATA}/components/footer.json", 'w') as f:
        json.dump(footer_data, f, indent=2)
    print("  ✓ footer.json created")
    
    print("✓ Migrated 2 components")

def migrate_images():
    """Copy images from assets to admin uploads folder"""
    print("\n🖼️  Migrating Images...")
    
    if not os.path.exists(SOURCE_ASSETS):
        print("  ✗ Source assets folder not found")
        return
    
    count = 0
    total_size = 0
    
    # Copy all images from assets folder
    for root, dirs, files in os.walk(SOURCE_ASSETS):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg')):
                source_path = os.path.join(root, file)
                # Maintain relative directory structure
                rel_path = os.path.relpath(root, SOURCE_ASSETS)
                dest_dir = os.path.join(ADMIN_ASSETS, rel_path) if rel_path != '.' else ADMIN_ASSETS
                
                os.makedirs(dest_dir, exist_ok=True)
                dest_path = os.path.join(dest_dir, file)
                
                shutil.copy2(source_path, dest_path)
                file_size = os.path.getsize(source_path)
                total_size += file_size
                count += 1
    
    print(f"✓ Migrated {count} images ({total_size / (1024*1024):.2f} MB)")

def create_summary():
    """Create a migration summary"""
    print("\n" + "="*60)
    print("MIGRATION SUMMARY")
    print("="*60)
    
    # Count migrated items
    pages = len([f for f in os.listdir(f"{ADMIN_DATA}/pages") if f.endswith('.json')])
    services = len([f for f in os.listdir(f"{ADMIN_DATA}/services") if f.endswith('.json')])
    case_studies = len([f for f in os.listdir(f"{ADMIN_DATA}/case-studies") if f.endswith('.json')])
    components = len([f for f in os.listdir(f"{ADMIN_DATA}/components") if f.endswith('.json')])
    
    # Count images
    images = 0
    total_size = 0
    if os.path.exists(ADMIN_ASSETS):
        for root, dirs, files in os.walk(ADMIN_ASSETS):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg')):
                    images += 1
                    total_size += os.path.getsize(os.path.join(root, file))
    
    print(f"\n📄 Pages: {pages}")
    print(f"🛠️  Services: {services}")
    print(f"📋 Case Studies: {case_studies}")
    print(f"🧩 Components: {components}")
    print(f"🖼️  Images: {images} ({total_size / (1024*1024):.2f} MB)")
    print("\n✅ Migration complete!")
    print("\nYou can now view and edit this content in the admin panel:")
    print("👉 http://localhost:5000/admin/dashboard")
    print("="*60 + "\n")

def main():
    """Main migration function"""
    print("\n" + "="*60)
    print("PhilanthroForge Admin Panel - Data Migration")
    print("="*60)
    
    try:
        ensure_directories()
        migrate_pages()
        migrate_services()
        migrate_case_studies()
        migrate_components()
        migrate_images()
        create_summary()
    except Exception as e:
        print(f"\n❌ Error during migration: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
