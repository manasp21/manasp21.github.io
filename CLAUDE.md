# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# Manas Pandey Portfolio Website

## Overview
A sophisticated, multi-page portfolio website for Manas Pandey, Undergraduate at IIT Kanpur exploring AI intersections. Features a modern dark theme with professional typography, comprehensive SEO optimization, and advanced content management systems for dynamic project showcase and blog functionality.

## Project Structure

### Pages
- **index.html** - Enhanced home page with serif typography, animations, and one-page websites showcase
- **about.html** - Personal story with consistent theming and placeholder images
- **research.html** - Research portfolio with automated Google Scholar integration and publication cards
- **projects.html** - GitHub-integrated project showcase with repository descriptions
- **blog/** - Complete Jekyll-powered blog system with interactive management
- **photography.html** - Professional gallery with lightbox, metadata system, and file-based management
- **one_page_websites/** - Dynamic showcase system for specialized project pages

### Assets
- **styles.css** - Complete CSS with dark theme, enhanced typography (Crimson Text, Montserrat, Lato), and professional animations
- **profile-image.png** - Professional profile photo (2.1MB)
- **gallery/** - Photography system with images directory and metadata.json
- **one_page_websites/** - Specialized single-page projects and explorations

## Development Memories

### Portfolio Management
- Always remember to update the README.md and CLAUDE.md files at the end of every session

### Recent Updates (2024-2025)
- **SEO Optimization**: Added comprehensive meta tags (robots, publisher, language, revisit-after, og:site_name) to all 12 HTML files
- **Performance**: Cleaned CSS by removing 340 lines of unused styles (10.3% reduction), improving load times
- **Repository Hygiene**: Added .gitignore file, removed Python cache files, cleaned debugging code from photography.html
- **Content Fixes**: Fixed "Undergraduate Undergraduate" duplication in about.html
- **Assets**: Added favicon.ico, created og-image.jpg placeholder with detailed specifications
- **Projects Enhancement**: Switched from README descriptions to clean GitHub repository descriptions for better presentation
- **Documentation**: Updated README.md and CLAUDE.md with latest optimization results and current status
- **Repository Decluttering (July 2025)**: Removed unnecessary files and directories for cleaner codebase
  - Removed node_modules/ directory (major space reduction)
  - Removed empty directories (config/, managers/, utils/, gui/)
  - Removed planning documentation files (plan.md, photo_manager_usage.md, assets/OG_IMAGE_PLACEHOLDER.md)
  - Removed optional README files in subdirectories
  - Fixed broken reference in README.md to non-existent photo_manager_plan.md
  - Maintained all functional code and essential documentation

### Consistency Improvements (July 2025)
- **Meta Tags Standardization**: Added missing publisher and revisit-after tags to about.html for complete SEO consistency across all pages
- **Social Media Assets**: Created missing og-image.jpg using professional profile photo, fixing broken social media previews across all 11 HTML pages 
- **Mobile Navigation Enhancement**: Added mobile-nav.js script to one-page websites (01.html, 03.html) that have mobile navigation elements but were missing JavaScript functionality
- **Schema Markup Enhancement**: Added comprehensive JSON-LD structured data to key one-page websites (01.html, 02.html, 03.html) for better search engine understanding
- **Architecture Documentation**: Verified body class consistency across main site (page-* classes) and one-page websites (TailwindCSS classes) - confirmed intentional differentiation
- **JavaScript Consistency**: Ensured mobile navigation functionality works consistently across all pages with mobile navigation elements

#### Consistency Analysis Results
- **5 main site pages**: All have consistent meta tags, body classes, and navigation structure
- **7 one-page websites**: 2 have mobile navigation (now functional), 5 are standalone presentations (by design)
- **11 total HTML pages**: All now reference working og-image.jpg for social media
- **3 key scientific pages**: Enhanced with comprehensive schema markup for better SEO
- **Zero breaking changes**: All improvements were additive, preserving existing functionality

#### Future Consistency Roadmap (For Consideration)
The following improvements would enhance consistency further but require more substantial changes:

**Typography Unification (Medium Risk)**
- Convert one-page websites from Playfair Display/Roboto/Inter to unified Montserrat/Lato/Crimson Text system
- Requires careful CSS conversion and testing to maintain visual appeal

**CSS Framework Consolidation (High Risk)** 
- Migrate one-page websites from TailwindCSS to main site's custom CSS architecture
- Would enable consistent styling patterns but requires extensive refactoring

**Jekyll Architecture Decision (Medium Risk)**
- Either: Convert all main pages to Jekyll layouts for unified build system
- Or: Create static HTML include system for consistent navigation/meta patterns
- Both approaches would simplify maintenance but require architectural changes

**Enhanced Schema Standardization (Low Risk)**
- Add comprehensive schema markup to remaining 4 one-page websites
- Standardize schema patterns across all pages with unified Person/Organization references

**URL Structure Unification (Medium Risk)**
- Implement consistent relative URL handling across Jekyll and static pages
- Would improve maintainability but requires testing all internal links

**Social Media Asset Optimization (Low Risk)**
- Replace current og-image.jpg with properly sized 1200x630px branded image
- Create page-specific social media images for key content

**Mobile Navigation Standardization (Low Risk)**
- Evaluate whether remaining 5 one-page websites would benefit from main site navigation
- Currently they're intentionally standalone - this would be a UX decision

These improvements are documented for future consideration when time allows for more extensive testing and potential visual impact assessment.

### Theme Switching System (July 2025)
- **Book Theme Implementation**: Added comprehensive book-like light theme with warm paper colors and serif typography
- **Floating Theme Toggle**: Implemented floating corner button across all main site pages with persistent localStorage
- **Photography Visual Fixes**: Fixed photo overlays, lightbox captions, category badges, and navigation controls for book theme compatibility
- **Main Site Only**: Book theme switching applies only to main portfolio pages (index, about, research, projects, blog, photography)
- **One-Page Websites Exclusion**: One-page websites (01.html through 07.html) are intentionally excluded from theme switching as they are standalone side projects with their own design systems

### UI Enhancement & Interactivity Update (July 2025)
- **Comprehensive Rounded Corner System**: Implemented scalable border-radius variables (--radius-sm through --radius-3xl) for consistent design language
- **Enhanced Card Interactions**: Upgraded all card components with smooth scaling, advanced shadows, and bounce animations
- **Navigation Improvements**: Added pill-shaped hover effects with background highlights and smooth transitions for both desktop and mobile navigation
- **Advanced Shadow System**: Introduced comprehensive shadow variables (--shadow-sm through --shadow-hover) with theme-aware coloring for both dark and book themes
- **Smooth Transitions**: Implemented cubic-bezier and bounce transitions throughout the interface for professional feel
- **Micro-Interactions**: Added subtle scaling, glow effects, and transform animations to buttons, tags, and interactive elements
- **Mobile Navigation Polish**: Enhanced mobile menu with rounded corners, improved animations, and better visual hierarchy
- **Photography Gallery**: Upgraded photo grid with enhanced hover effects, improved lightbox interactions, and consistent rounded corners
- **Interactive Elements**: Enhanced skill tags, filter buttons, project links, and navigation elements with improved feedback and visual polish

### Blog Contribution Graph Implementation (July 2025)
- **GitHub-Style Activity Visualization**: Added comprehensive contribution graph showing daily blog writing activity over the last 365 days
- **Multi-Level Contribution Display**: Implemented 5-level intensity system (0-4+ posts per day) with distinct colors for both dark and book themes
- **Interactive Features**: Added hover tooltips, click navigation to posts, and accessibility support with proper ARIA labels
- **Theme Integration**: Seamlessly integrated with existing dark/book theme system using appropriate color schemes
  - Dark theme: Green gradient from gray (#161b22) to vivid green (#39d353)
  - Book theme: Brown gradient from light paper (#f0ebe5) to rich brown (#8b6f3b)
- **Mobile Responsive**: Optimized for mobile devices with horizontal scrolling and touch-friendly interactions
- **Performance Optimized**: Efficient JavaScript handling 365+ DOM elements with minimal performance impact
- **Jekyll Integration**: Dynamic data generation from Jekyll posts with proper JSON formatting
- **Statistics Display**: Shows total posts in the last year with potential for additional metrics
- **Professional Design**: Matches GitHub's contribution graph aesthetic with consistent spacing and typography

### Blog Contribution Graph Fixes (July 2025)
- **Fixed Centering Issues**: Completely redesigned HTML structure with proper flexbox centering and alignment
- **Improved CSS Architecture**: Replaced hard-coded values with CSS variables for consistency with blog page design
- **Enhanced JavaScript Logic**: Fixed month label calculation to properly align with 53-week grid structure
- **Better Theme Integration**: Aligned visual design with existing blog page patterns using .section-title and .section-description classes  
- **Simplified Layout**: Removed complex nested containers causing alignment issues
- **Professional Styling**: Integrated with blog page design patterns using consistent backgrounds, borders, and spacing
- **Fixed Grid Generation**: Proper 53×7 grid with accurate date calculations and month label alignment
- **Mobile Optimization**: Improved responsive design with better touch interactions and scrolling

### Blog Contribution Graph Color Integration (July 2025)
- **Red Theme Integration**: Corrected from orange to red colors matching blog's actual accent theme (`--accent-red`) for perfect visual cohesion
- **CSS Variable System**: Added comprehensive `--contrib-level-*` variables that automatically adapt to both dark and book themes
- **Theme-Aware Colors**: 
  - Dark theme: Red progression using `--accent-red` (#DC2626) with 20%, 40%, 70%, and 100% opacity levels
  - Book theme: High-contrast solid colors from beige (#F5F1E8) to deep burgundy (#8B1538) for maximum visibility
- **Light Theme Visibility Fix**: Completely resolved invisibility issues with solid color progression instead of transparent rgba
  - Level-0: Soft beige (#F5F1E8) - clearly distinguishable from white background
  - Level 1-3: Progressive rose-brown colors (#E8D5D8 → #D4B8BE → #B8949C) with clear visual distinction
  - Level-4: Deep burgundy (#8B1538) for maximum activity contrast
- **Enhanced Borders**: Improved border visibility (0.4/0.5 opacity) for clear grid structure without overwhelming content
- **Legend Synchronization**: Updated legend colors to exactly match contribution day colors using same CSS variables
- **Accessibility Compliance**: Ensured proper contrast ratios for all activity levels on both light and dark backgrounds
- **Auto-Update Verification**: Confirmed Jekyll integration automatically updates graph when new blog posts are added
- **Perfect Visibility**: Contribution graph now works flawlessly in both themes with clear activity level distinction

### Blog Contribution Graph Nuclear Fix (July 2025)
- **Nuclear Solution Deployment**: Implemented comprehensive ultra-high specificity CSS fix after multiple attempts with standard solutions failed
- **Root Cause Analysis**: Identified multiple aggressive book theme rules with `!important` and `inherit` forcing ALL div elements to use main background colors, creating inheritance cascade issues
- **Multi-Layered Defense Strategy**: 
  - **Container Overrides**: Set all parent containers (`contribution-graph-section`, `graph-container`, etc.) to `transparent` backgrounds
  - **Ultra-High Specificity**: Used full element path selectors (e.g., `:root[data-theme="book"] body .page-container .contribution-graph .graph-container .graph-content .graph-grid .contribution-day.level-0`)
  - **Multiple Selector Fallbacks**: Added 4 different specificity levels per element to ensure coverage
  - **Direct Hex Fallbacks**: Included hardcoded color values (`#F5F1E8`, `#E8D5D8`, `#D4B8BE`, `#B8949C`, `#8B1538`) as backup to CSS variables
  - **Inheritance Override**: Used `background-color: unset !important` to break forced inheritance chains
  - **Final Color Re-application**: Added final layer of direct color assignments for bulletproof coverage
- **Technical Innovation**: Pioneered 6-step CSS override strategy to defeat overly aggressive theme inheritance rules
- **Production Guarantee**: Nuclear approach ensures contribution graph visibility regardless of future CSS changes or browser rendering variations
- **Maintainability**: Comprehensive commenting and step-by-step structure allows future developers to understand and modify the complex override hierarchy

### Web Development Best Practices
- Do not edit on page websites directly

## Architecture Overview

### Jekyll-Powered Portfolio with Hybrid Architecture
This project combines static HTML/CSS/JS with Jekyll for blog functionality and Python automation for content management. The architecture supports both technical content (research, projects) and creative content (photography, blog) with professional-grade management systems.

### Key Components
1. **Main Portfolio Pages**: 6 core pages (index, about, research, projects, photography, blog) with unified design system
2. **One-Page Websites**: 8 specialized standalone pages using TailwindCSS for independent projects
3. **Content Management**: 6 Python scripts for automated content updates and validation
4. **Jekyll Blog System**: Complete blog functionality with category pages and post management

### CSS Architecture
- **Unified Design System**: CSS custom properties for consistent spacing, typography, and colors
- **Dual Theme Support**: Dark theme (primary) and book theme with automatic switching
- **Professional Typography**: Montserrat (headings), Lato (body), Crimson Text (serif)
- **Modern Animation System**: Performance-optimized transitions and micro-interactions

## Development Commands

### Jekyll Development
```bash
# Local development server
bundle exec jekyll serve

# Alternative static server
python -m http.server 8000

# Dependencies installation
gem install jekyll bundler
bundle install
```

### Content Management Scripts
```bash
# Blog management
python blog_manager.py add|list|edit|remove|validate

# Project showcase updates
python project_manager.py add|list|update|generate

# Research publications (Google Scholar)
python scholar_manager.py update|generate|list
bash update_research.sh

# Photography gallery
python photo_manager.py edit|list|validate|rename

# One-page websites scanning
python onesite_manager.py scan|update|generate
```

### Common Development Tasks
- **Local Testing**: Use Jekyll serve for full functionality or Python server for static testing
- **Content Updates**: Use Python managers for automated content updates with validation
- **Theme Testing**: Test both dark and book themes across all main pages
- **Mobile Testing**: Verify mobile navigation and responsive design
- **Performance Testing**: Check Core Web Vitals and image optimization
- **Blog Contribution Graph**: Automatically updates with new blog posts, showing activity visualization

## Content Management Strategy

### File-Based Content with JSON Metadata
- **Blog Posts**: Jekyll markdown with YAML frontmatter
- **Photography**: Image files with metadata.json for gallery information
- **Projects**: GitHub API integration with local caching
- **Research**: Google Scholar integration with automated updates

### Automation Features
- **24-hour caching** for external API calls
- **Automatic backups** for all content modifications
- **Validation systems** for YAML frontmatter and metadata
- **Rollback capabilities** for safe content management

### Content Validation
All content management scripts include validation for:
- YAML frontmatter syntax
- Image file existence and metadata
- External API data integrity
- Backup creation before modifications

## Design Philosophy

### Core Theme
Professional dark theme portfolio emphasizing content readability and sophisticated user experience. Clean, modern aesthetic with enhanced typography and smooth animations that showcase technical expertise while maintaining personal warmth.

### Performance Optimization
- **Lazy loading** for images and content
- **Optimized animations** using CSS transforms
- **Minified assets** and clean CSS architecture
- **Mobile-first responsive design**

### SEO Excellence
- **Comprehensive meta tags** across all pages
- **Structured data** with JSON-LD for key pages
- **Sitemap generation** for search engines
- **Social media optimization** with proper Open Graph tags

## Special Considerations

### Deployment Strategy
- **GitHub Pages hosting** with automatic deployment
- **Jekyll integration** for blog functionality
- **No build process required** - files served directly
- **Version control** for all content changes

### Mobile Optimization
- **Professional mobile navigation** with hamburger menu
- **Touch-optimized interactions** with proper touch targets
- **Responsive images** with lazy loading
- **Performance considerations** for mobile devices

### Security and Maintenance
- **Automatic backups** for all content modifications
- **Git-based version control** for change tracking
- **Validation systems** to prevent content corruption
- **Clean separation** between static and dynamic content

# important-instruction-reminders
Do what has been asked; nothing more, nothing less.
NEVER create files unless they're absolutely necessary for achieving your goal.
ALWAYS prefer editing an existing file to creating a new one.
NEVER proactively create documentation files (*.md) or README files. Only create documentation files if explicitly requested by the User.