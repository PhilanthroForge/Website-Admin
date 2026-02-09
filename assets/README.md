# Asset Organization Reference

## Naming Convention

Format: `{page}-{section}-{description}.{ext}`

### Examples:
- ✅ `home-hero-background.jpg`
- ✅ `services-digital-strategy-hero.jpg`
- ✅ `about-team-founder.jpg`
- ✅ `case-studies-rewarding-generosity-hero.jpg`

---

## Directory Structure

```
/assets/
├── branding/
│   └── logo.png
├── home/
│   ├── hero-background.jpg
│   ├── service-digital-strategy.jpg
│   ├── service-consultancy.jpg
│   ├── service-campaign.jpg
│   └── case-rewarding-generosity.jpg
├── about/
│   ├── hero-background.jpg
│   ├── process-implement.jpg
│   └── team-founder.jpg
├── services/
│   ├── hero-background.jpg
│   ├── digital-strategy/
│   │   ├── hero.jpg
│   │   └── audit-section.jpg
│   ├── consultancy/
│   ├── campaign-design/
│   ├── donor-analysis/
│   ├── website-optimization/
│   ├── donation-form/
│   ├── csr-support/
│   └── brand-identity/
├── case-studies/
│   ├── rewarding-generosity/
│   ├── integrated-ecosystems/
│   └── turning-supporters/
└── pages/
    ├── lets-talk-hero.jpg
    ├── privacy-hero.jpg
    └── terms-hero.jpg
```

---

## Quick Reference

| Old Location | New Location | Usage |
|--------------|--------------|-------|
| `Folder/Philanthro logo.png` | `branding/logo.png` | Site-wide logo |
| `index_content_img.jpg` | `home/hero-background.jpg` | Homepage hero |
| `about_content_img.jpg` | `about/hero-background.jpg` | About page hero |
| `service-*_content_img.jpg` | `services/*/hero.jpg` | Service page heroes |

---

## Scripts

### 1. Analysis
```bash
python3 analyze_assets.py
```
Analyzes current assets, creates directories, generates renaming scripts.

### 2. Rename Assets
```bash
./rename_assets.sh
```
Copies files to new organized structure.

### 3. Update References
```bash
python3 update_asset_references.py
```
Updates all HTML files with new asset paths.

---

## Benefits

1. **Easy to Find:** `assets/services/digital-strategy/hero.jpg` vs `index_digital_fundraising_strategywe_audit_you_philanthroforge_nonprofit_digital_fundra.jpg`

2. **Organized by Context:** All service images in `/services/`, all case studies in `/case-studies/`

3. **Scalable:** Add new service? Create `services/new-service/` folder

4. **Clear Dependencies:** Know exactly which images belong to which pages

5. **Better Git Diffs:** Renamed files are obvious in version control
