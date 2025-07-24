# AGENTS.md - Development Commands & Guidelines

## Build & Test Commands
```bash
bundle exec jekyll serve --livereload  # Local dev server
bundle exec jekyll build --watch       # Build only
python -m http.server 8000            # Static server fallback
```

## Code Style Guidelines
- **HTML**: Semantic tags, 2-space indentation, kebab-case for classes/ids
- **CSS**: CSS custom properties, BEM-like naming, mobile-first responsive
- **JS**: CamelCase variables, async/await, no console.log in production
- **Python**: PEP 8, snake_case, type hints, f-strings, proper error handling
- **YAML**: 2-space indentation, consistent quotes, no trailing spaces

## File Organization
- Static pages: root *.html files
- Blog: _posts/*.md with YAML frontmatter
- Assets: assets/, gallery/, one_page_websites/
- Scripts: *.py files for content management
- Config: _config.yml, Gemfile, .gitignore

## Testing & Validation
- Jekyll build must pass without errors
- All external links validated
- Mobile responsive on 320px+ screens
- SEO meta tags present on all pages
- Theme switching works across all pages