#!/usr/bin/env python3
"""
Asset Organization Script
Analyzes current asset usage and generates renaming plan
"""

import os
import re
from pathlib import Path
from collections import defaultdict

BASE_DIR = Path("/Users/bipashahalder/Documents/Philanthroforge_Complete_Clone")
ASSETS_DIR = BASE_DIR / "assets"

# Mapping old names to new organized names
ASSET_MAPPING = {
    # Branding
    "Folder/Philanthro logo.png": "branding/logo.png",
    
    # Home page assets
    "index_content_img.jpg": "home/hero-background.jpg",
    "index_digital_fundraising_strategywe_audit_you_philanthroforge_nonprofit_digital_fundra.jpg": "home/service-digital-strategy.jpg",
    "index_fundraising_consultancy_advisory_philanthroforge_fundraising_advisory_exp.jpg": "home/service-consultancy.jpg",
    "index_fundraising_campaign_journey_design_philanthroforge_professional_nonprofit_f.jpg": "home/service-campaign.jpg",
    "index_website_donation_ux_optimization_philanthroforge_fundraising_advisory_exp.jpg": "home/service-website-ux.jpg",
    "index_csr_major_donor_support_philanthroforge_nonprofit_fundraising_ad.jpg": "home/service-csr.jpg",
    "index_rewarding_generosity_unlocks_new_givingg_philanthroforge_nonprofit_fundraising_co.jpg": "home/case-rewarding-generosity.jpg",
    
    # About page
    "about_content_img.jpg": "about/hero-background.jpg",
    "about_build_implement_philanthroforge_how_to_get_more_donation.jpg": "about/process-implement.jpg",
    "about_linkedin_philanthroforge_md_shane_ali_fundraising.jpg": "about/team-founder.jpg",
    "about_over_the_last_4_years_we_haveworked_with_philanthroforge_worked_with_platforms_an.jpg": "about/platforms-logos.jpg",
    
    # Services main page
    "services_content_img.jpg": "services/hero-background.jpg",
    "services_listen_deeply_to_donors_and_data_img.jpg": "services/donor-analysis-graphic.jpg",
    "services_design_systems_not_just_campaigns_philanthroforge_nonprofit_fundraising_ex.jpg": "services/systems-design.jpg",
    
    # Digital Fundraising Strategy service
    "service-digital-strategy_content_img.jpg": "services/digital-strategy/hero.jpg",
    "service-digital-strategy_comprehensive_auditwebsite_structure_and_img.jpg": "services/digital-strategy/audit-section.jpg",
    "service-digital-strategy_strategic_analysis_improvements_img.jpg": "services/digital-strategy/analysis.jpg",
    
    # Consultancy service
    "service-consultancy_content_img.jpg": "services/consultancy/hero.jpg",
    "service-consultancy_decision_making_support_img.jpg": "services/consultancy/decision-support.jpg",
    "service-consultancy_strategic_review_sessionsregular_engagem_img.jpg": "services/consultancy/review-sessions.jpg",
    
    # Campaign Design service
    "service-campaign-design_content_img.jpg": "services/campaign-design/hero.jpg",
    "service-campaign-design_campaign_strategyclear_positioning_of_ca_img.jpg": "services/campaign-design/strategy.jpg",
    "service-campaign-design_creative_content_img.jpg": "services/campaign-design/creative-content.jpg",
    
    # Donor Analysis service
    "service-donor-analysis_content_img.jpg": "services/donor-analysis/hero.jpg",
    "service-donor-analysis_revenue_performance_assessment_img.jpg": "services/donor-analysis/revenue-assessment.jpg",
    "service-donor-analysis_supporter_behaviour_analysisacquisition__img.jpg": "services/donor-analysis/behaviour-analysis.jpg",
    
    # Website Optimization service
    "service-website-optimization_content_img.jpg": "services/website-optimization/hero.jpg",
    "service-website-optimization_donation_experience_designstreamlined_wo_img.jpg": "services/website-optimization/donation-design.jpg",
    "service-website-optimization_key_page_optimization_img.jpg": "services/website-optimization/page-optimization.jpg",
    
    # Donation Form service
    "service-donation-form_content_img.jpg": "services/donation-form/hero.jpg",
    "service-donation-form_form_redesign_img.jpg": "services/donation-form/form-redesign.jpg",
    "service-donation-form_form_audit_and_analysiscomprehensive_rev_img.jpg": "services/donation-form/audit-analysis.jpg",
    
    # CSR Support service
    "service-csr-support_content_img.jpg": "services/csr-support/hero.jpg",
    "service-csr-support_csr_partnership_materialsstrategic_posit_img.jpg": "services/csr-support/partnership-materials.jpg",
    "service-csr-support_major_donor_and_grant_narratives_img.jpg": "services/csr-support/donor-narratives.jpg",
    
    # Brand Identity service
    "service-brand-identity_content_img.jpg": "services/brand-identity/hero.jpg",
    "service-brand-identity_visual_identity_system_img.jpg": "services/brand-identity/visual-system.jpg",
    "service-brand-identity_brand_strategy_and_positioningwebsite_st_img.jpg": "services/brand-identity/brand-strategy.jpg",
    
    # Case Studies
    "case-rewarding-generosity_content_img.jpg": "case-studies/rewarding-generosity/hero.jpg",
    "case-integrated-ecosystems_content_img.jpg": "case-studies/integrated-ecosystems/hero.jpg",
    "case-turning-supporters_content_img.jpg": "case-studies/turning-supporters/hero.jpg",
    
    # Contact/Let's Talk
    "contact_content_img.jpg": "pages/lets-talk-hero.jpg",
    
    # Legal pages
    "privacy_content_img.jpg": "pages/privacy-hero.jpg",
    "terms_content_img.jpg": "pages/terms-hero.jpg",
}

def analyze_assets():
    """Analyze current asset usage"""
    print("=" * 70)
    print("ASSET ANALYSIS")
    print("=" * 70)
    
    # Get all image files
    image_extensions = {'.jpg', '.jpeg', '.png', '.svg', '.gif', '.webp'}
    all_images = []
    
    for root, dirs, files in os.walk(ASSETS_DIR):
        for file in files:
            if Path(file).suffix.lower() in image_extensions:
                rel_path = Path(root).relative_to(ASSETS_DIR) / file
                all_images.append(str(rel_path))
    
    print(f"\n📊 Total Images: {len(all_images)}")
    print(f"📊 Mapped for Renaming: {len(ASSET_MAPPING)}")
    print(f"📊 Unmapped: {len(all_images) - len(ASSET_MAPPING)}")
    
    # Group by category
    categories = defaultdict(int)
    for old_path in ASSET_MAPPING.values():
        category = old_path.split('/')[0]
        categories[category] += 1
    
    print(f"\n📁 Asset Distribution:")
    for cat, count in sorted(categories.items()):
        print(f"   {cat:25} {count:3} files")
    
    return all_images

def create_directory_structure():
    """Create organized directory structure"""
    print("\n" + "=" * 70)
    print("CREATING DIRECTORY STRUCTURE")
    print("=" * 70)
    
    directories = {
        "branding",
        "home",
        "about",
        "services",
        "services/digital-strategy",
        "services/consultancy",
        "services/campaign-design",
        "services/donor-analysis",
        "services/website-optimization",
        "services/donation-form",
        "services/csr-support",
        "services/brand-identity",
        "case-studies",
        "case-studies/rewarding-generosity",
        "case-studies/integrated-ecosystems",
        "case-studies/turning-supporters",
        "pages",
    }
    
    for dir_name in sorted(directories):
        dir_path = ASSETS_DIR / dir_name
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"✅ Created: assets/{dir_name}/")
        else:
            print(f"ℹ️  Exists:  assets/{dir_name}/")

def generate_rename_script():
    """Generate bash script to rename files"""
    script_lines = [
        "#!/bin/bash",
        "# Asset Renaming Script",
        "# Auto-generated by analyze_assets.py",
        "",
        "cd /Users/bipashahalder/Documents/Philanthroforge_Complete_Clone/assets",
        "",
        "echo '====================================================='",
        "echo 'Renaming Assets'",
        "echo '====================================================='",
        ""
    ]
    
    for old_path, new_path in sorted(ASSET_MAPPING.items()):
        # Check if source exists
        old_full = ASSETS_DIR / old_path
        if old_full.exists():
            script_lines.append(f"# {old_path} -> {new_path}")
            script_lines.append(f'cp "{old_path}" "{new_path}"')
            script_lines.append("")
    
    script_lines.extend([
        "echo ''",
        "echo '====================================================='",
        "echo '✅ Asset reorganization complete!'",
        "echo '====================================================='",
    ])
    
    script_path = BASE_DIR / "rename_assets.sh"
    with open(script_path, 'w') as f:
        f.write('\n'.join(script_lines))
    
    # Make executable
    os.chmod(script_path, 0o755)
    
    print(f"\n✅ Generated: {script_path}")
    return script_path

def generate_update_references_script():
    """Generate Python script to update HTML references"""
    script_content = '''#!/usr/bin/env python3
"""
Update HTML asset references to new paths
"""
import re
from pathlib import Path

BASE_DIR = Path("/Users/bipashahalder/Documents/Philanthroforge_Complete_Clone")

# Old path -> New path mapping
REPLACEMENTS = {
'''
    
    for old_path, new_path in sorted(ASSET_MAPPING.items()):
        script_content += f'    "assets/{old_path}": "assets/{new_path}",\n'
    
    script_content += '''}

HTML_FILES = [
    "index.html", "about.html", "services.html", "case-studies.html",
    "lets-talk.html", "privacy-policy.html", "terms-and-conditions.html", "404.html",
    "services/digital-fundraising-strategy.html",
    "services/consultancy-advisory.html",
    "services/donation-form-optimization.html",
    "services/website-donation-optimization.html",
    "services/fundraising-campaign-journey-design.html",
    "services/donor-behaviour-analysis-revenue-growth.html",
    "services/brand-identity-impact-communication.html",
    "services/csr-major-donor-support.html",
    "case-studies/rewarding-generosity.html",
    "case-studies/integrated-ecosystems.html",
    "case-studies/turning-supporters-into-fundraisers.html",
]

def update_file(filepath):
    full_path = BASE_DIR / filepath
    if not full_path.exists():
        return
    
    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    changes = 0
    
    for old_path, new_path in REPLACEMENTS.items():
        if old_path in content:
            content = content.replace(old_path, new_path)
            changes += 1
    
    if content != original:
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ {filepath}: {changes} references updated")
    else:
        print(f"ℹ️  {filepath}: No changes needed")

if __name__ == "__main__":
    print("Updating HTML asset references...")
    for html_file in HTML_FILES:
        update_file(html_file)
    print("\\n✅ Done!")
'''
    
    script_path = BASE_DIR / "update_asset_references.py"
    with open(script_path, 'w') as f:
        f.write(script_content)
    
    os.chmod(script_path, 0o755)
    print(f"✅ Generated: {script_path}")
    return script_path

def main():
    print("\n")
    all_images = analyze_assets()
    create_directory_structure()
    rename_script = generate_rename_script()
    update_script = generate_update_references_script()
    
    print("\n" + "=" * 70)
    print("NEXT STEPS")
    print("=" * 70)
    print(f"\n1. Review the asset mapping above")
    print(f"2. Run: ./rename_assets.sh")
    print(f"3. Run: python3 update_asset_references.py")
    print(f"4. Test pages to verify images load correctly")
    print(f"\n💡 Organized structure:")
    print(f"   assets/branding/        - Logo, favicon")
    print(f"   assets/home/            - Homepage images")
    print(f"   assets/services/*/      - Service-specific images")
    print(f"   assets/case-studies/*/  - Case study images")
    print("\n")

if __name__ == "__main__":
    main()
