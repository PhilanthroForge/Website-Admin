"""
Services and Case Studies Management Module
Handles CRUD operations for services and case studies
"""
import os
import json
from datetime import datetime
from config import Config

# ============================================================================
# Services Management
# ============================================================================

def get_all_services():
    """Get all services"""
    services = []
    
    if not os.path.exists(Config.SERVICES_FOLDER):
        os.makedirs(Config.SERVICES_FOLDER, exist_ok=True)
        return services
    
    for filename in os.listdir(Config.SERVICES_FOLDER):
        if filename.endswith('.json'):
            filepath = os.path.join(Config.SERVICES_FOLDER, filename)
            with open(filepath, 'r') as f:
                service = json.load(f)
                service['id'] = filename.replace('.json', '')
                services.append(service)
    
    # Sort by order if available, otherwise by title
    services.sort(key=lambda x: (x.get('order', 999), x.get('title', '')))
    return services

def get_service(service_id):
    """Get a specific service by ID"""
    filepath = os.path.join(Config.SERVICES_FOLDER, f'{service_id}.json')
    
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            service = json.load(f)
            service['id'] = service_id
            return service
    
    return None

def save_service(service_id, data):
    """Save or update a service"""
    os.makedirs(Config.SERVICES_FOLDER, exist_ok=True)
    
    # Add metadata
    if not data.get('created_at'):
        data['created_at'] = datetime.now().isoformat()
    data['updated_at'] = datetime.now().isoformat()
    
    filepath = os.path.join(Config.SERVICES_FOLDER, f'{service_id}.json')
    
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
    
    return {'success': True, 'message': f'Service "{data.get("title", service_id)}" saved'}

def delete_service(service_id):
    """Delete a service"""
    filepath = os.path.join(Config.SERVICES_FOLDER, f'{service_id}.json')
    
    if os.path.exists(filepath):
        os.remove(filepath)
        return {'success': True, 'message': 'Service deleted'}
    
    return {'success': False, 'error': 'Service not found'}

def create_service_slug(title):
    """Create a URL-friendly slug from title"""
    import re
    slug = title.lower()
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    slug = slug.strip('-')
    return slug

# ============================================================================
# Case Studies Management
# ============================================================================

def get_all_case_studies():
    """Get all case studies"""
    case_studies = []
    
    if not os.path.exists(Config.CASES_FOLDER):
        os.makedirs(Config.CASES_FOLDER, exist_ok=True)
        return case_studies
    
    for filename in os.listdir(Config.CASES_FOLDER):
        if filename.endswith('.json'):
            filepath = os.path.join(Config.CASES_FOLDER, filename)
            with open(filepath, 'r') as f:
                case_study = json.load(f)
                case_study['id'] = filename.replace('.json', '')
                case_studies.append(case_study)
    
    # Sort by order if available, otherwise by title
    case_studies.sort(key=lambda x: (x.get('order', 999), x.get('title', '')))
    return case_studies

def get_case_study(case_id):
    """Get a specific case study by ID"""
    filepath = os.path.join(Config.CASES_FOLDER, f'{case_id}.json')
    
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            case_study = json.load(f)
            case_study['id'] = case_id
            return case_study
    
    return None

def save_case_study(case_id, data):
    """Save or update a case study"""
    os.makedirs(Config.CASES_FOLDER, exist_ok=True)
    
    # Add metadata
    if not data.get('created_at'):
        data['created_at'] = datetime.now().isoformat()
    data['updated_at'] = datetime.now().isoformat()
    
    filepath = os.path.join(Config.CASES_FOLDER, f'{case_id}.json')
    
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
    
    return {'success': True, 'message': f'Case study "{data.get("title", case_id)}" saved'}

def delete_case_study(case_id):
    """Delete a case study"""
    filepath = os.path.join(Config.CASES_FOLDER, f'{case_id}.json')
    
    if os.path.exists(filepath):
        os.remove(filepath)
        return {'success': True, 'message': 'Case study deleted'}
    
    return {'success': False, 'error': 'Case study not found'}

def create_case_study_template():
    """Create a default case study template"""
    return {
        'title': '',
        'subtitle': '',
        'client': '',
        'industry': '',
        'challenge': '',
        'solution': '',
        'results': [],
        'image': '',
        'url': '',
        'order': 0,
        'featured': False,
        'status': 'draft'
    }

def create_service_template():
    """Create a default service template"""
    return {
        'title': '',
        'subtitle': '',
        'description': '',
        'features': [],
        'benefits': [],
        'image': '',
        'icon': '',
        'url': '',
        'order': 0,
        'featured': False,
        'status': 'published'
    }
