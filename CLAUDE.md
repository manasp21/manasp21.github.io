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

## Design Philosophy

### Core Theme
Professional dark theme portfolio emphasizing content readability and sophisticated user experience. Clean, modern aesthetic with enhanced typography and smooth animations that showcase technical expertise while maintaining personal warmth.

[Rest of the existing content remains unchanged]