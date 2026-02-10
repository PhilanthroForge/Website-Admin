import os

template_path = '/Users/bipashahalder/Documents/Philanthroforge_Complete_Clone/services/digital-fundraising-strategy.html'
base_dir = '/Users/bipashahalder/Documents/Philanthroforge_Complete_Clone'

pages = [
    # Services
    {
        'path': 'services/consultancy-advisory.html',
        'title': 'Consultancy & Advisory - PhilanthroForge',
        'h1': 'Fundraising Consultancy & Advisory',
        'desc': 'Strategic guidance to navigate complex fundraising challenges.'
    },
    {
        'path': 'services/website-donation-optimization.html',
        'title': 'Website & Donation Optimization - PhilanthroForge',
        'h1': 'Website & Donation UX Optimization',
        'desc': 'Turn your website into a high-converting engine.'
    },
    {
        'path': 'services/donation-form-optimization.html',
        'title': 'Donation Form Optimization - PhilanthroForge',
        'h1': 'Donation Form Optimization',
        'desc': 'Optimize forms to reduce friction and increase conversion.'
    },
    {
        'path': 'services/fundraising-campaign-design.html',
        'title': 'Fundraising Campaign Design - PhilanthroForge',
        'h1': 'Fundraising Campaign & Journey Design',
        'desc': 'Create compelling campaigns that resonate with donors.'
    },
    {
        'path': 'services/donor-behaviour-analysis-revenue-growth.html',
        'title': 'Donor Behaviour Analysis - PhilanthroForge',
        'h1': 'Donor Behaviour Analysis & Revenue Growth',
        'desc': 'Data-driven insights to maximize donor lifetime value.'
    },
    {
        'path': 'services/csr-major-donor-support.html',
        'title': 'CSR & Major Donor Support - PhilanthroForge',
        'h1': 'CSR & Major Donor Support',
        'desc': 'Strategize your approach to high-impact funding.'
    },
    {
        'path': 'services/brand-identity-impact-messaging.html',
        'title': 'Brand Identity - PhilanthroForge',
        'h1': 'Brand, Identity & Impact Communication',
        'desc': 'Clarify your message and visualize your impact.'
    },
    # Case Studies
    {
        'path': 'case-studies/rewarding-generosity.html',
        'title': 'Rewarding Generosity - PhilanthroForge Case Study',
        'h1': 'Rewarding Generosity',
        'desc': 'How we helped a non-profit unlock new giving potential.'
    },
    {
        'path': 'case-studies/turning-supporters-into-champions.html',
        'title': 'Turning Supporters Into Champions - PhilanthroForge Case Study',
        'h1': 'Turning Supporters Into Champions',
        'desc': 'Building a community of dedicated advocates.'
    },
    {
        'path': 'case-studies/integrated-ecosystems.html',
        'title': 'Integrated Ecosystems - PhilanthroForge Case Study',
        'h1': 'Integrated Ecosystems',
        'desc': 'Unifying data and tools for a seamless donor experience.'
    }
]

with open(template_path, 'r') as f:
    template_content = f.read()

for page in pages:
    new_content = template_content.replace('Digital Fundraising Strategy - PhilanthroForge', page['title'])
    new_content = new_content.replace('<h1 class="text-4xl font-bold text-primary mb-6">Digital Fundraising Strategy</h1>', f'<h1 class="text-4xl font-bold text-primary mb-6">{page["h1"]}</h1>')
    new_content = new_content.replace('<p class="text-xl text-gray-600 mb-8">We audit your digital fundraising engine to identify growth opportunities.</p>', f'<p class="text-xl text-gray-600 mb-8">{page["desc"]}</p>')
    
    # Fix active state if I had one (I didn't really, but good to be careful)
    
    target_path = os.path.join(base_dir, page['path'])
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    with open(target_path, 'w') as f:
        f.write(new_content)
    print(f"Created {page['path']}")
