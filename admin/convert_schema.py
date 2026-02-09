#!/usr/bin/env python3
"""
Data Schema Converter for Admin Panel

Converts the scraped JSON structure to match the admin panel's expected schema.
This will properly populate all fields in services, case studies, and fix page structure.
"""

import os
import json
from datetime import datetime

# Paths
ADMIN_DATA = "/Users/bipashahalder/Documents/Philanthroforge_Complete_Clone/admin/data"

def convert_service_schema(filename):
    """Convert service JSON to admin panel schema"""
    filepath = os.path.join(ADMIN_DATA, "services", filename)
    
    if not os.path.exists(filepath):
        print(f"  ✗ {filename} not found")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Extract service ID from filename
        service_id = filename.replace('.json', '')
        
        # Parse metadata
        metadata = data.get('metadata', {})
        title = metadata.get('title', service_id.replace('-', ' ').title())
        
        # Extract content from content_blocks
        content_blocks = data.get('content_blocks', [])
        subtitle = ""
        description = ""
        features = []
        
        # Parse content blocks
        for block in content_blocks:
            block_type = block.get('type', '')
            heading = block.get('heading', '')
            text = block.get('text', '')
            
            # Use first section as subtitle
            if not subtitle and heading and block_type == 'section':
                subtitle = heading
            
            # Collect text for description
            if text:
                description += text + "\n\n"
            
            # Collect features/headings
            if heading and block_type == 'section' and heading not in [subtitle, title]:
                features.append({
                    "title": heading,
                    "description": text.split('\n')[0] if text else ""
                })
        
        # Create admin panel schema
        admin_schema = {
            "service_id": service_id,
            "title": title,
            "subtitle": subtitle.strip(),
            "description": description.strip(),
            "features": features[:6],  # Limit to 6 features
            "icon": "",
            "image": "",
            "status": "published",
            "order": 0,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        # Save converted schema
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(admin_schema, f, indent=2, ensure_ascii=False)
        
        print(f"  ✓ {filename} → {title}")
        return True
        
    except Exception as e:
        print(f"  ✗ Error converting {filename}: {e}")
        return False

def convert_case_study_schema(filename):
    """Convert case study JSON to admin panel schema"""
    filepath = os.path.join(ADMIN_DATA, "case-studies", filename)
    
    if not os.path.exists(filepath):
        print(f"  ✗ {filename} not found")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Extract case study ID from filename
        case_study_id = filename.replace('.json', '')
        
        # Parse metadata
        metadata = data.get('metadata', {})
        title = metadata.get('title', case_study_id.replace('-', ' ').title())
        
        # Extract content from content_blocks
        content_blocks = data.get('content_blocks', [])
        client = ""
        challenge = ""
        solution = ""
        results = ""
        
        # Parse content blocks
        for block in content_blocks:
            heading = block.get('heading', '').lower()
            text = block.get('text', '')
            
            if 'challenge' in heading or 'problem' in heading:
                challenge = text
            elif 'solution' in heading or 'approach' in heading:
                solution = text
            elif 'result' in heading or 'impact' in heading or 'outcome' in heading:
                results = text
            elif not client and text:
                # Use first significant text as client/description
                client = heading if heading else text.split('\n')[0]
        
        # Create admin panel schema
        admin_schema = {
            "case_study_id": case_study_id,
            "title": title,
            "client": client.strip(),
            "challenge": challenge.strip() if challenge else "Details coming soon",
            "solution": solution.strip() if solution else "Details coming soon",
            "results": results.strip() if results else "Details coming soon",
            "testimonial": {
                "quote": "",
                "author": "",
                "position": ""
            },
            "image": "",
            "status": "published",
            "order": 0,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        # Save converted schema
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(admin_schema, f, indent=2, ensure_ascii=False)
        
        print(f"  ✓ {filename} → {title}")
        return True
        
    except Exception as e:
        print(f"  ✗ Error converting {filename}: {e}")
        return False

def main():
    """Main conversion function"""
    print("\n" + "="*60)
    print("Admin Panel - Data Schema Converter")
    print("="*60)
    
    # Convert services
    print("\n🛠️  Converting Services...")
    services_dir = os.path.join(ADMIN_DATA, "services")
    service_count = 0
    
    for filename in os.listdir(services_dir):
        if filename.endswith('.json') and filename != 'test-service.json':
            if convert_service_schema(filename):
                service_count += 1
    
    print(f"✓ Converted {service_count} services")
    
    # Convert case studies
    print("\n📋 Converting Case Studies...")
    case_studies_dir = os.path.join(ADMIN_DATA, "case-studies")
    case_study_count = 0
    
    for filename in os.listdir(case_studies_dir):
        if filename.endswith('.json'):
            if convert_case_study_schema(filename):
                case_study_count += 1
    
    print(f"✓ Converted {case_study_count} case studies")
    
    print("\n" + "="*60)
    print(f"Conversion Complete!")
    print(f"  Services: {service_count}")
    print(f"  Case Studies: {case_study_count}")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
