# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# Manas Pandey Portfolio Website

## Overview
A hybrid Jekyll + static HTML portfolio for Manas Pandey (IIT Kanpur). Main pages share a unified dark theme with book-mode light theme toggle. One-page websites are standalone TailwindCSS pages — **do not edit them directly**.

## Development Commands

```bash
# Full local dev (Jekyll blog + static pages)
bundle exec jekyll serve

# Static-only preview (no Jekyll features)
python -m http.server 8000

# Install Ruby deps
gem install jekyll bundler && bundle install
```

Python managers require a virtual environment:
```bash
python blog_manager.py add|list|edit|remove|validate   # Blog posts + hero images
python project_manager.py add|list|update|generate     # GitHub project cards
python scholar_manager.py update|generate|list         # Google Scholar publications
python photo_manager.py edit|list|validate|rename      # Photography gallery
python onesite_manager.py scan|update|generate         # One-page website registry
python linkedin_manager.py                             # LinkedIn profile sync
```

## Architecture

### Page Types
- **Main portfolio pages** (`index.html`, `about.html`, `research.html`, `projects.html`, `photography.html`, `books.html`): Use `styles.css`, `body.page-*` class conventions, theme toggle, and shared JS.
- **Blog** (`blog/index.html`, `_posts/`, `blog/categories/`): Jekyll-powered; posts in `_posts/YYYY-MM-DD-title.md` with YAML frontmatter; categories auto-generate pages under `blog/categories/`.
- **One-page websites** (`one_page_websites/01–08.html`): Standalone TailwindCSS pages for independent projects. Do not edit these directly.

### CSS Architecture (`styles.css`)
Single file with CSS custom properties. Two themes toggled via `data-theme="book"` on `<html>`:
- **Dark** (default): near-black backgrounds, `--accent-red: #FF2D55` as primary accent.
- **Book**: warm paper tones, burgundy accents. Theme preference stored in `localStorage`.

The contribution graph in `blog/index.html` uses ultra-high-specificity CSS overrides (long selector chains with `!important`) because aggressive book-theme inheritance rules force color inheritance on all `div` elements. Do not simplify those selectors — they are intentional.

### JavaScript Files (root level)
- `animations.js` — scroll/entrance animations across main pages
- `mobile-nav.js` — hamburger menu logic (included by main pages and select one-page websites)
- `blog-contribution-graph.js` — GitHub-style activity grid on blog index
- `mouse-effects.js` / `particle-ripple.js` — cursor visual effects

### Content Data Files
- `gallery/metadata.json` — photography metadata
- `onesites.json` — one-page website registry
- `linkedin_profile.json` — LinkedIn data
- `.projects_cache.json` / `.onesites_cache.json` — 24-hour API caches (auto-generated, gitignored)

### Jekyll Config Key Points (`_config.yml`)
- Blog permalink: `/blog/:year/:month/:day/:title/`
- Default layout for posts: `post`; default for all other pages: `default`
- `<!--more-->` is the excerpt separator
- `*.json` files and Python scripts are excluded from the Jekyll build

### Blog Post Frontmatter
```yaml
---
layout: post
title: "Post Title"
date: YYYY-MM-DD HH:MM:SS +0530
categories: [category1, category2]
author: Manas Pandey
hero_image: /blog/images/posts/YYYY/post-slug-hero.jpg  # optional
hero_alt: "Alt text"                                      # optional
---
```

## Key Constraints
- **Author**: Always `Manas Pandey` in all content and frontmatter.
- **One-page websites**: Do not edit `one_page_websites/*.html` directly.
- **Theme scope**: Theme toggle applies only to main portfolio pages; one-page websites have their own design systems.
- **Cache files**: `.projects_cache.json`, `.onesites_cache.json` are auto-generated — do not commit them.
- **Backups**: `.unified_backups/` holds zip backups — do not delete.
- **Session close**: Update `README.md` and `CLAUDE.md` at the end of every session.

# important-instruction-reminders
Do what has been asked; nothing more, nothing less.
NEVER create files unless they're absolutely necessary for achieving your goal.
ALWAYS prefer editing an existing file to creating a new one.
NEVER proactively create documentation files (*.md) or README files. Only create documentation files if explicitly requested by the User.
