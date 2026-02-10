# PhilanthroForge Website

Modern, CMS-powered fundraising consultancy website built with Next.js, TinaCMS, and GSAP animations.

## 🚀 Features

- **Next.js 15** - React framework with App Router
- **TinaCMS** - Git-based headless CMS for content management
- **Tailwind CSS v4** - Utility-first CSS framework
- **GSAP** - Professional scroll animations and micro-interactions
- **TypeScript** - Type-safe development
- **Fully Responsive** - Mobile-first design

## 📁 Project Structure

```
philanthroforge-nextjs/
├── app/                    # Next.js app directory
│   ├── page.tsx           # Homepage
│   ├── services/          # Service pages
│   ├── case-studies/      # Case study pages
│   └── ...
├── components/            # Reusable React components
│   ├── Navbar.tsx
│   ├── Footer.tsx
│   ├── AnimatedSection.tsx
│   └── ServiceCard.tsx
├── content/               # MDX content files
│   ├── pages/            # General pages
│   ├── services/         # Service content
│   └── case-studies/     # Case study content
├── lib/                   # Utility functions
│   ├── animations.ts     # GSAP helpers
│   └── tina.ts           # TinaCMS data fetching
├── hooks/                 # Custom React hooks
│   └── useScrollAnimation.ts
├── public/
│   └── images/           # Static images (134 files)
├── tina/                  # TinaCMS configuration
│   └── config.ts         # CMS schema
└── scripts/
    └── migrate-content.js # JSON to MDX converter
```

## 🛠️ Local Development

### Prerequisites

- Node.js 18+ 
- npm or yarn

### Installation

```bash
# Install dependencies
npm install

# Copy environment variables
cp .env.example .env.local

# Add your TinaCMS credentials to .env.local
# Get them from https://app.tina.io
```

### Running Locally

```bash
# Start development server
npm run dev

# Open browser
open http://localhost:3000

# Access TinaCMS admin
open http://localhost:3000/admin/index.html
```

## 📝 Content Management

### Admin Panel

Access the CMS at `/admin/index.html` to edit:
- **Pages** - Homepage, About, Contact, etc.
- **Services** - Service offerings (8 total)
- **Case Studies** - Client success stories (3 total)

### Content Structure

All content is stored as MDX files in the `/content` directory:
- Editable through TinaCMS admin panel
- Version controlled in Git
- Supports rich text, images, and custom components

## 🎨 Animations

GSAP-powered animations throughout the site:
- **Scroll Animations** - Fade-in, stagger, scale effects
- **Hover Effects** - Card lift, button interactions
- **Performance** - Optimized for 60fps

## 🚀 Deployment

### Deploy to Vercel

1. Push code to GitHub
2. Import project in [Vercel](https://vercel.com)
3. Add environment variables:
   - `NEXT_PUBLIC_TINA_CLIENT_ID`
   - `TINA_TOKEN`
   - `NEXT_PUBLIC_TINA_BRANCH`
4. Deploy!

### TinaCMS Cloud Setup

1. Sign up at [app.tina.io](https://app.tina.io)
2. Connect your GitHub repository
3. Get your credentials
4. Add to Vercel environment variables

## 📦 Build Commands

```bash
# Development
npm run dev

# Production build
npm run build

# Start production server
npm start

# Type checking
npm run type-check

# Linting
npm run lint
```

## 🎯 Key Pages

- **Homepage** (`/`) - Hero, services overview, featured case study
- **Services** (`/services`) - All service offerings
- **Service Detail** (`/services/[slug]`) - Individual service pages
- **Case Studies** (`/case-studies`) - Success stories listing
- **Case Study Detail** (`/case-studies/[slug]`) - Individual case studies
- **About** (`/about`) - Company information
- **Contact** (`/lets-talk`) - Contact form

## 🔧 Tech Stack

- **Framework**: [Next.js 15](https://nextjs.org/)
- **CMS**: [TinaCMS](https://tina.io/)
- **Styling**: [Tailwind CSS v4](https://tailwindcss.com/)
- **Animations**: [GSAP](https://greensock.com/gsap/)
- **Language**: [TypeScript](https://www.typescriptlang.org/)
- **Deployment**: [Vercel](https://vercel.com/)

## 📄 License

© 2026 PhilanthroForge. All rights reserved.

## 🤝 Support

For questions or support, contact: hello@philanthroforge.com
