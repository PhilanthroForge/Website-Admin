"""
Component Management Module
Handles navbar and footer component editing
"""
import os
import json
from config import Config

def get_navbar_config():
    """Load navbar configuration"""
    filepath = os.path.join(Config.COMPONENTS_FOLDER, 'navbar.json')
    
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    
    # Default navbar structure
    return {
        'logo': {
            'text': 'PhilanthroForge',
            'link': '/'
        },
        'menu_items': [
            {
                'text': 'About',
                'link': '/about.html',
                'type': 'link'
            },
            {
                'text': 'Services',
                'link': '#',
                'type': 'dropdown',
                'submenu': [
                    {'text': 'Digital Fundraising Strategy', 'link': '/services/digital-fundraising-strategy.html'},
                    {'text': 'Website & Donation Optimization', 'link': '/services/website-donation-optimization.html'},
                    {'text': 'Fundraising Campaign Design', 'link': '/services/fundraising-campaign-journey-design.html'},
                    {'text': 'Donation Form Optimization', 'link': '/services/donation-form-optimization.html'},
                    {'text': 'Donor Behaviour Analysis', 'link': '/services/donor-behaviour-analysis-revenue-growth.html'},
                    {'text': 'Brand Identity & Impact Messaging', 'link': '/services/brand-identity-impact-messaging.html'},
                    {'text': 'CSR & Major Donor Support', 'link': '/services/csr-major-donor-support.html'},
                    {'text': 'Consultancy & Advisory', 'link': '/services/consultancy-advisory.html'}
                ]
            },
            {
                'text': 'Case Studies',
                'link': '/case-studies.html',
                'type': 'link'
            }
        ],
        'cta': {
            'text': "Let's Talk",
            'link': '/lets-talk.html'
        }
    }

def save_navbar_config(data):
    """Save navbar configuration"""
    filepath = os.path.join(Config.COMPONENTS_FOLDER, 'navbar.json')
    os.makedirs(Config.COMPONENTS_FOLDER, exist_ok=True)
    
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
    
    return {'success': True, 'message': 'Navbar configuration saved'}

def get_footer_config():
    """Load footer configuration"""
    filepath = os.path.join(Config.COMPONENTS_FOLDER, 'footer.json')
    
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    
    # Default footer structure
    return {
        'brand': {
            'name': 'PhilanthroForge',
            'tagline': 'Forging the Next Era of Non-Profit Fundraising'
        },
        'quick_links': [
            {'text': 'About', 'link': '/about.html'},
            {'text': 'Services', 'link': '/services.html'},
            {'text': 'Case Studies', 'link': '/case-studies.html'},
            {'text': 'Let\'s Talk', 'link': '/lets-talk.html'}
        ],
        'services': [
            {'text': 'Digital Fundraising Strategy', 'link': '/services/digital-fundraising-strategy.html'},
            {'text': 'Website Optimization', 'link': '/services/website-donation-optimization.html'},
            {'text': 'Campaign Design', 'link': '/services/fundraising-campaign-journey-design.html'},
            {'text': 'Consultancy', 'link': '/services/consultancy-advisory.html'}
        ],
        'contact': {
            'email': 'hello@philanthroforge.com',
            'phone': '+44 (0) 20 1234 5678',
            'address': 'London, United Kingdom'
        },
        'social': [
            {'platform': 'LinkedIn', 'url': 'https://linkedin.com/company/philanthroforge', 'icon': 'linkedin'},
            {'platform': 'Twitter', 'url': 'https://twitter.com/philanthroforge', 'icon': 'twitter'}
        ],
        'legal': [
            {'text': 'Privacy Policy', 'link': '/privacy-policy.html'},
            {'text': 'Terms & Conditions', 'link': '/terms-and-conditions.html'}
        ],
        'copyright': '© 2024 PhilanthroForge. All rights reserved.'
    }

def save_footer_config(data):
    """Save footer configuration"""
    filepath = os.path.join(Config.COMPONENTS_FOLDER, 'footer.json')
    os.makedirs(Config.COMPONENTS_FOLDER, exist_ok=True)
    
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
    
    return {'success': True, 'message': 'Footer configuration saved'}
