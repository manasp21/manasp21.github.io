# Manas Pandey - Professional Portfolio Website

> *A sophisticated, multi-page portfolio website showcasing the intersection of experimental physics, artificial intelligence, and creative expression. Built with modern web technologies and comprehensive content management systems.*

## 🌟 Live Demo

**Visit the live website**: [https://manasp21.github.io](https://manasp21.github.io)

---

## ✨ Features Overview

### 🎨 **Professional Design System**
- **Enhanced Typography**: Sophisticated serif/sans-serif mix with Crimson Text, Montserrat, and Lato
- **Animated Interface**: Smooth fade-in animations, hover effects, and interactive elements
- **Dark Theme**: Professional dark aesthetic with red accent colors
- **Glass Morphism**: Modern backdrop blur effects and translucent surfaces
- **Responsive Design**: Mobile-first approach with adaptive layouts

### 🔧 **Advanced Management Systems**
- **Blog Management**: Complete Python-based Jekyll blog system with interactive editing
- **Projects Management**: Automatic GitHub integration with README-powered descriptions
- **One-Page Websites**: Dynamic showcase system for specialized project pages
- **Photography Gallery**: Professional lightbox gallery with comprehensive photo management
- **LinkedIn Integration**: Automatic profile data parsing and about page generation
- **Photo Management**: Enterprise-grade photo organization with metadata editing
- **Research Publications**: Automated Google Scholar integration with publication cards

### 🚀 **SEO & Performance**
- **Complete SEO Suite**: robots.txt, XML sitemap, structured data, meta tags
- **Performance Optimized**: Lazy loading, optimized animations, caching systems
- **Accessibility Compliant**: ARIA labels, keyboard navigation, screen reader support
- **Search Engine Ready**: JSON-LD structured data, Open Graph, Twitter Cards

---

## 🏗️ Project Architecture

```
manasp21.github.io/
├── 📄 Core Pages
│   ├── index.html              # Enhanced home page with animations
│   ├── about.html              # Personal story and background
│   ├── research.html           # Research portfolio with Google Scholar integration
│   ├── projects.html           # GitHub projects showcase
│   ├── photography.html        # Professional photo gallery
│   └── blog/index.html         # Jekyll-powered blog
│
├── 🎨 Design & Assets
│   ├── styles.css              # Complete styling with animations
│   ├── profile-image.png       # Profile photo
│   └── gallery/                # Photography collection
│       ├── images/             # Photo files
│       └── metadata.json       # Photo metadata
│
├── 🤖 Management Systems
│   ├── blog_manager.py         # Complete blog management
│   ├── project_manager.py      # GitHub projects integration
│   ├── onesite_manager.py      # One-page websites manager
│   ├── photo_manager.py        # Professional photo management
│   ├── linkedin_manager.py     # LinkedIn profile integration
│   ├── scholar_manager.py      # Google Scholar publications manager
│   ├── update_research.sh      # Automated research update script
│   └── photo_manager_plan.md   # Photo management documentation
│
├── 🌐 One-Page Websites
│   └── one_page_websites/
│       └── 1.html              # AI in Physics exploration
│
├── 📊 SEO & Configuration
│   ├── robots.txt              # Search engine directives
│   ├── sitemap.xml             # Site structure for crawlers
│   ├── _config.yml             # Jekyll configuration
│   ├── onesites.json           # One-page sites config
│   ├── projects.json           # Projects configuration
│   └── scholar_config.json     # Google Scholar configuration
│
├── 📝 Content Management
│   ├── _posts/                 # Blog posts (Markdown)
│   ├── _layouts/               # Jekyll templates
│   ├── _includes/              # Reusable components
│   └── assets/images/posts/    # Blog post images
│
└── 🔧 Development
    ├── .backups/               # Automatic backup system
    ├── CLAUDE.md               # Development documentation
    └── README.md               # This file
```

---

## 🚀 Quick Start

### Prerequisites
```bash
# Required software
- Python 3.8+
- Jekyll 4.0+
- Modern web browser
- Git
```

### Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/manasp21/manasp21.github.io.git
   cd manasp21.github.io
   ```

2. **Install dependencies**
   ```bash
   # Jekyll for blog functionality
   gem install jekyll bundler
   bundle install
   
   # Python dependencies for management tools
   pip install pyyaml requests
   ```

3. **Serve locally**
   ```bash
   # Full Jekyll server (recommended)
   bundle exec jekyll serve
   
   # Alternative: Simple HTTP server
   python -m http.server 8000
   ```

4. **Access the website**
   - Jekyll: `http://localhost:4000`
   - HTTP server: `http://localhost:8000`

---

## 🛠️ Management Systems

### 🔬 **Research Publications Management**

Automated Google Scholar integration system for displaying academic publications with professional cards.

#### Features:
- ✅ **Automatic Fetching**: Scrapes publications directly from Google Scholar profile
- ✅ **Professional Display**: Beautiful publication cards with titles, authors, venues, citations
- ✅ **Smart Caching**: 24-hour cache system for performance optimization
- ✅ **Manual Management**: Add/remove publications manually when needed
- ✅ **Featured System**: Highlights top publications automatically
- ✅ **Responsive Design**: Mobile-optimized publication showcase

#### Commands:
```bash
# Fetch latest publications from Google Scholar
python scholar_manager.py update

# Update research.html with publication cards
python scholar_manager.py generate

# List all cached publications
python scholar_manager.py list

# Validate research system
python scholar_manager.py validate

# Manually add a publication
python scholar_manager.py add

# Automated daily update (for cron scheduling)
bash update_research.sh

# Update DOI and external links for existing publications
python scholar_manager.py links
```

#### Configuration:
The system uses `scholar_config.json` for settings:
```json
{
  "profile": {
    "user_id": "3cqkF08AAAAJ",
    "profile_url": "https://scholar.google.com/citations?user=3cqkF08AAAAJ&hl=en"
  },
  "settings": {
    "cache_duration": 86400,
    "sort_by": "year"
  }
}
```

### 📝 **Blog Management System**

Complete Python-based tool for managing Jekyll blog posts with interactive interface.

#### Features:
- ✅ **Interactive Creation**: Guided post creation with tag/category suggestions
- ✅ **Smart Editing**: Modify any aspect of existing posts with validation
- ✅ **Safety Features**: Automatic backups, confirmation prompts, rollback capability
- ✅ **Content Management**: External editor support, reading time calculation
- ✅ **Validation**: YAML frontmatter checking, consistency verification

#### Commands:
```bash
# Create new blog post
python blog_manager.py add

# List all posts with metadata
python blog_manager.py list

# Edit existing posts (title, content, tags, etc.)
python blog_manager.py edit

# Preview post content
python blog_manager.py preview

# Remove posts (with backup)
python blog_manager.py remove

# Validate all posts
python blog_manager.py validate
```

#### Blog Post Structure:
```yaml
---
layout: post
title: "Your Post Title"
date: 2024-06-19 15:30:00 +0530
categories: [research, technical]
tags: [quantum computing, ai, physics]
excerpt: "Brief description..."
reading_time: 8
---

Your markdown content here...
```

### 🚀 **Projects Management System**

Advanced GitHub integration system with automatic README description extraction.

#### Features:
- ✅ **GitHub Integration**: Automatic repository data fetching via GitHub API
- ✅ **README Parsing**: Smart extraction of project descriptions from README files
- ✅ **Metadata Collection**: Stars, forks, language, last updated, topics
- ✅ **Caching System**: 24-hour cache for improved performance
- ✅ **Auto-Generation**: Automatic HTML generation for projects showcase

#### Commands:
```bash
# Add new GitHub project
python project_manager.py add <github-url>

# List all projects with details
python project_manager.py list

# Update project metadata
python project_manager.py update [--force]

# Generate HTML for projects page
python project_manager.py generate

# Validate configuration
python project_manager.py validate
```

#### Configuration (projects.json):
```json
{
  "projects": [
    "https://github.com/manasp21/MagTrace"
  ],
  "settings": {
    "auto_update": true,
    "cache_duration": 86400
  }
}
```

### 🌐 **One-Page Websites System**

Dynamic showcase system for specialized single-page projects and explorations.

#### Features:
- ✅ **Automatic Detection**: Scans numbered HTML files (1.html, 2.html, etc.)
- ✅ **Title Extraction**: Automatically extracts titles from HTML `<title>` tags
- ✅ **Smart Descriptions**: Intelligent content extraction from page body
- ✅ **Dynamic Showcase**: Automatic integration into main website
- ✅ **Professional Cards**: Animated cards with launch buttons

#### Commands:
```bash
# Scan for new one-page websites
python onesite_manager.py scan

# List all detected sites
python onesite_manager.py list

# Update metadata
python onesite_manager.py update [--force]

# Generate showcase section
python onesite_manager.py generate

# Validate system
python onesite_manager.py validate
```

#### Usage:
1. Add numbered HTML files to `one_page_websites/` folder
2. Run `python onesite_manager.py update && python onesite_manager.py generate`
3. New sites automatically appear in the showcase section

### 📸 **Photography Management System**

Enterprise-grade photo organization with professional metadata management and SEO-friendly naming.

#### Features:
- ✅ **Interactive Editing**: Complete metadata editing (captions, titles, tags, camera settings)
- ✅ **Smart Renaming**: Transform device names to SEO-friendly professional filenames
- ✅ **Bulk Operations**: Update multiple photos with automated title and caption generation
- ✅ **Validation System**: Comprehensive integrity checks and quality assurance
- ✅ **Safety Features**: Automatic backups, validation, and rollback capabilities

#### Commands:
```bash
# Interactive caption and metadata editing
python photo_manager.py edit [--photo ID]

# View all photos with metadata
python photo_manager.py list [--category urban] [--featured]

# Validate system integrity
python photo_manager.py validate

# Smart batch renaming with SEO-friendly names
python photo_manager.py rename [--preview]

# Fix consistency issues automatically
python photo_manager.py fix

# Bulk enhance titles and captions
python photo_manager.py bulk-titles
python photo_manager.py bulk-captions

# Add new photos with full metadata collection
python photo_manager.py add /path/to/photo.jpg
```

#### Photo Transformation Examples:
```
Before: PXL_20240621_192621681-EFFECTS.jpg
After:  2024-06-21-urban-cityscape.jpg

Titles: "Image 1" → "Urban Cityscape Golden Hour"
Captions: "Image Caption" → "Urban photography capturing cityscape, golden hour, architecture captured in European City."
```

### 💼 **LinkedIn Integration System**

Automatic LinkedIn profile data parsing and professional about page generation.

#### Features:
- ✅ **Profile Parsing**: Extract experience, education, and skills from LinkedIn data
- ✅ **Interactive Management**: Edit and enhance professional information
- ✅ **HTML Generation**: Automatic about page content generation with professional styling
- ✅ **Skills Categorization**: Organize skills into Technical, Management, Creative categories
- ✅ **Timeline Display**: Professional experience timeline with hover effects

#### Commands:
```bash
# Interactive LinkedIn profile management
python linkedin_manager.py interactive

# Parse LinkedIn data and create profile
python linkedin_manager.py parse

# Update about.html with latest profile data
python linkedin_manager.py update

# Preview generated HTML sections
python linkedin_manager.py preview

# Show extracted skills summary
python linkedin_manager.py skills
```

---

## 🎨 Design System

### **Typography**
```css
--font-family-primary: 'Lato', sans-serif;          /* Body text */
--font-family-heading: 'Montserrat', sans-serif;    /* Headings */
--font-family-serif: 'Crimson Text', serif;         /* Elegant accents */
```

### **Color Palette**
```css
--bg-primary: #121212;        /* Dark background */
--bg-secondary: #1a1a1a;      /* Secondary background */
--text-primary: #EAEAEA;      /* Primary text */
--text-secondary: #b0b0b0;    /* Secondary text */
--accent-red: #DC2626;        /* Primary accent */
```

### **Animation System**
- **Fade-in animations**: Staggered content appearance
- **Hover effects**: Interactive element responses
- **Smooth transitions**: Professional micro-interactions
- **Performance optimized**: 60fps animations with mobile adaptations

---

## 📱 Page Overview

| Page | Status | Features | Management |
|------|--------|----------|------------|
| **Home** | ✅ Complete | Enhanced typography, animations, hero section, one-page showcase | Static content |
| **About** | ✅ Complete | LinkedIn integration, professional timeline, skills matrix | `linkedin_manager.py` |
| **Research** | 🔄 Placeholder | Research interests, vision statements | Static content |
| **Projects** | ✅ Complete | GitHub integration, README descriptions | `project_manager.py` |
| **Blog** | ✅ Complete | Jekyll posts, interactive management | `blog_manager.py` |
| **Photography** | ✅ Complete | Professional gallery, enterprise photo management | `photo_manager.py` |
| **One-Page Sites** | ✅ Complete | Dynamic showcase, automatic detection | `onesite_manager.py` |

---

## 🔍 SEO & Performance

### **Search Engine Optimization**
- ✅ **robots.txt**: Proper crawler directives and sitemap reference
- ✅ **XML Sitemap**: Dynamic Jekyll-generated sitemap with priorities
- ✅ **Structured Data**: JSON-LD Person and Website schemas
- ✅ **Meta Tags**: Complete Open Graph and Twitter Card implementation
- ✅ **Canonical URLs**: Proper URL canonicalization across all pages

### **Performance Features**
- ✅ **Lazy Loading**: Images and content load as needed
- ✅ **Caching System**: Management scripts use intelligent caching
- ✅ **Optimized Animations**: Hardware-accelerated CSS transforms
- ✅ **Responsive Images**: Adaptive loading based on screen size
- ✅ **Minified Assets**: Optimized CSS and reduced file sizes

### **Core Web Vitals**
- **Largest Contentful Paint (LCP)**: < 2.5s
- **First Input Delay (FID)**: < 100ms
- **Cumulative Layout Shift (CLS)**: < 0.1

---

## 🌐 Deployment

### **GitHub Pages (Current)**
- **Automatic deployment** from `main` branch
- **Custom domain support** available
- **Jekyll integration** for blog functionality
- **CDN delivery** via GitHub's infrastructure

### **Manual Deployment Steps**
```bash
# 1. Update all content systems
python blog_manager.py validate
python project_manager.py update
python onesite_manager.py update && python onesite_manager.py generate
python photo_manager.py validate
python linkedin_manager.py update

# 2. Commit changes
git add .
git commit -m "Update content and systems"
git push origin main

# 3. Verify deployment
# Check https://manasp21.github.io after ~5 minutes
```

---

## 🔧 Development Workflow

### **Adding New Blog Posts**
```bash
python blog_manager.py add
# Follow interactive prompts
# Post automatically appears in blog section
```

### **Adding New GitHub Projects**
```bash
python project_manager.py add https://github.com/username/repo
python project_manager.py generate
# Project appears in projects section with README description
```

### **Adding One-Page Websites**
```bash
# 1. Create numbered HTML file
cp template.html one_page_websites/2.html

# 2. Update content and title
# Edit one_page_websites/2.html

# 3. Update showcase
python onesite_manager.py update
python onesite_manager.py generate
# New site appears in One Page Websites section
```

### **Managing Photography Portfolio**
```bash
# Add new photos with full metadata collection
python photo_manager.py add /path/to/photo.jpg

# Enhance existing photos with better titles and captions
python photo_manager.py bulk-titles
python photo_manager.py bulk-captions

# Interactive editing of individual photos
python photo_manager.py edit --photo 5

# Smart rename files to SEO-friendly format
python photo_manager.py rename
```

### **Managing LinkedIn Profile**
```bash
# Update about page with latest LinkedIn data
python linkedin_manager.py interactive

# Parse new LinkedIn information
python linkedin_manager.py parse

# Generate updated about page content
python linkedin_manager.py update
```

---

## 🛡️ Safety & Backup Systems

### **Automatic Backups**
- ✅ **File Backups**: All management tools create timestamped backups
- ✅ **Configuration Safety**: Settings validated before changes
- ✅ **Rollback Capability**: Easy restoration from backups
- ✅ **Change Tracking**: Clear modification logs

### **Validation Systems**
- ✅ **Content Validation**: YAML frontmatter and structure checking
- ✅ **Link Verification**: Internal and external link validation
- ✅ **Image Optimization**: Size and format recommendations
- ✅ **SEO Compliance**: Meta tag and structure validation

---

## 📊 Analytics & Monitoring

### **Performance Monitoring**
- Google PageSpeed Insights integration
- Core Web Vitals tracking
- Mobile performance optimization
- SEO ranking monitoring

### **Content Analytics**
- Blog post performance tracking
- Project showcase engagement
- Photography gallery interactions
- One-page website launches

---

## 🤝 Contributing

This is a personal portfolio website, but feedback and suggestions are welcome!

### **Reporting Issues**
1. Check existing issues for duplicates
2. Provide detailed reproduction steps
3. Include browser and device information
4. Suggest potential solutions if possible

### **Feature Requests**
1. Explain the use case and benefits
2. Consider compatibility with existing systems
3. Propose implementation approach
4. Discuss maintenance implications

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 📞 Contact

**Manas Pandey**  
*Physics Student & AI Researcher at IIT Kanpur*

- 🌐 **Website**: [manasp21.github.io](https://manasp21.github.io)
- 💼 **LinkedIn**: [themanaspandey](https://linkedin.com/in/themanaspandey)
- 🐙 **GitHub**: [manasp21](https://github.com/manasp21)
- 🎭 **Poetry**: [manasp21.github.io/poetry_website](https://manasp21.github.io/poetry_website/)
- 📧 **Email**: manas@example.com

---

## 🙏 Acknowledgments

- **Design Inspiration**: Modern web standards and professional portfolios
- **Typography**: Google Fonts for beautiful, accessible typefaces
- **Performance**: Web.dev guidelines and Core Web Vitals standards
- **SEO**: Modern search engine optimization best practices
- **Accessibility**: WCAG 2.1 guidelines for inclusive design

---

## 🎯 Portfolio Success Metrics

### **Professional Transformation Achieved**
- ✅ **16 Photos Professionally Organized**: SEO-friendly filenames and rich metadata
- ✅ **5 Management Systems**: Complete automation for all content areas
- ✅ **LinkedIn Integration**: Professional about page with experience timeline
- ✅ **Enterprise-Grade Safety**: Comprehensive backup and validation systems
- ✅ **100% SEO Optimized**: Professional structure and performance standards

### **From Generic to Professional**
```
Before: PXL_20240621_192621681-EFFECTS.jpg | "Image 1" | "Image Caption"
After:  2024-06-21-urban-cityscape.jpg | "Urban Cityscape Golden Hour" | "Urban photography capturing cityscape, golden hour, architecture captured in European City."
```

**Result**: A sophisticated digital portfolio that bridges scientific precision with artistic expression, showcasing the multidisciplinary journey of a physicist through enterprise-grade content management and professional presentation.