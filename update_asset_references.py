#!/usr/bin/env python3
"""
Update HTML asset references to new paths
"""
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Old path -> New path mapping
REPLACEMENTS = {
    "assets/Folder/Philanthro logo.png": "assets/branding/logo.png",
    "assets/about_build_implement_philanthroforge_how_to_get_more_donation.jpg": "assets/about/process-implement.jpg",
    "assets/about_content_img.jpg": "assets/about/hero-background.jpg",
    "assets/about_linkedin_philanthroforge_md_shane_ali_fundraising.jpg": "assets/about/team-founder.jpg",
    "assets/about_over_the_last_4_years_we_haveworked_with_philanthroforge_worked_with_platforms_an.jpg": "assets/about/platforms-logos.jpg",
    "assets/case-integrated-ecosystems_content_img.jpg": "assets/case-studies/integrated-ecosystems/hero.jpg",
    "assets/case-rewarding-generosity_content_img.jpg": "assets/case-studies/rewarding-generosity/hero.jpg",
    "assets/case-turning-supporters_content_img.jpg": "assets/case-studies/turning-supporters/hero.jpg",
    "assets/contact_content_img.jpg": "assets/pages/lets-talk-hero.jpg",
    "assets/index_content_img.jpg": "assets/home/hero-background.jpg",
    "assets/index_csr_major_donor_support_philanthroforge_nonprofit_fundraising_ad.jpg": "assets/home/service-csr.jpg",
    "assets/index_digital_fundraising_strategywe_audit_you_philanthroforge_nonprofit_digital_fundra.jpg": "assets/home/service-digital-strategy.jpg",
    "assets/index_fundraising_campaign_journey_design_philanthroforge_professional_nonprofit_f.jpg": "assets/home/service-campaign.jpg",
    "assets/index_fundraising_consultancy_advisory_philanthroforge_fundraising_advisory_exp.jpg": "assets/home/service-consultancy.jpg",
    "assets/index_rewarding_generosity_unlocks_new_givingg_philanthroforge_nonprofit_fundraising_co.jpg": "assets/home/case-rewarding-generosity.jpg",
    "assets/index_website_donation_ux_optimization_philanthroforge_fundraising_advisory_exp.jpg": "assets/home/service-website-ux.jpg",
    "assets/privacy_content_img.jpg": "assets/pages/privacy-hero.jpg",
    "assets/service-brand-identity_brand_strategy_and_positioningwebsite_st_img.jpg": "assets/services/brand-identity/brand-strategy.jpg",
    "assets/service-brand-identity_content_img.jpg": "assets/services/brand-identity/hero.jpg",
    "assets/service-brand-identity_visual_identity_system_img.jpg": "assets/services/brand-identity/visual-system.jpg",
    "assets/service-campaign-design_campaign_strategyclear_positioning_of_ca_img.jpg": "assets/services/campaign-design/strategy.jpg",
    "assets/service-campaign-design_content_img.jpg": "assets/services/campaign-design/hero.jpg",
    "assets/service-campaign-design_creative_content_img.jpg": "assets/services/campaign-design/creative-content.jpg",
    "assets/service-consultancy_content_img.jpg": "assets/services/consultancy/hero.jpg",
    "assets/service-consultancy_decision_making_support_img.jpg": "assets/services/consultancy/decision-support.jpg",
    "assets/service-consultancy_strategic_review_sessionsregular_engagem_img.jpg": "assets/services/consultancy/review-sessions.jpg",
    "assets/service-csr-support_content_img.jpg": "assets/services/csr-support/hero.jpg",
    "assets/service-csr-support_csr_partnership_materialsstrategic_posit_img.jpg": "assets/services/csr-support/partnership-materials.jpg",
    "assets/service-csr-support_major_donor_and_grant_narratives_img.jpg": "assets/services/csr-support/donor-narratives.jpg",
    "assets/service-digital-strategy_comprehensive_auditwebsite_structure_and_img.jpg": "assets/services/digital-strategy/audit-section.jpg",
    "assets/service-digital-strategy_content_img.jpg": "assets/services/digital-strategy/hero.jpg",
    "assets/service-digital-strategy_strategic_analysis_improvements_img.jpg": "assets/services/digital-strategy/analysis.jpg",
    "assets/service-donation-form_content_img.jpg": "assets/services/donation-form/hero.jpg",
    "assets/service-donation-form_form_audit_and_analysiscomprehensive_rev_img.jpg": "assets/services/donation-form/audit-analysis.jpg",
    "assets/service-donation-form_form_redesign_img.jpg": "assets/services/donation-form/form-redesign.jpg",
    "assets/service-donor-analysis_content_img.jpg": "assets/services/donor-analysis/hero.jpg",
    "assets/service-donor-analysis_revenue_performance_assessment_img.jpg": "assets/services/donor-analysis/revenue-assessment.jpg",
    "assets/service-donor-analysis_supporter_behaviour_analysisacquisition__img.jpg": "assets/services/donor-analysis/behaviour-analysis.jpg",
    "assets/service-website-optimization_content_img.jpg": "assets/services/website-optimization/hero.jpg",
    "assets/service-website-optimization_donation_experience_designstreamlined_wo_img.jpg": "assets/services/website-optimization/donation-design.jpg",
    "assets/service-website-optimization_key_page_optimization_img.jpg": "assets/services/website-optimization/page-optimization.jpg",
    "assets/services_content_img.jpg": "assets/services/hero-background.jpg",
    "assets/services_design_systems_not_just_campaigns_philanthroforge_nonprofit_fundraising_ex.jpg": "assets/services/systems-design.jpg",
    "assets/services_listen_deeply_to_donors_and_data_img.jpg": "assets/services/donor-analysis-graphic.jpg",
    "assets/terms_content_img.jpg": "assets/pages/terms-hero.jpg",
}

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
    print("\n✅ Done!")
