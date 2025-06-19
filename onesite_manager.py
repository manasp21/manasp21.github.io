#!/usr/bin/env python3
"""
One-Page Websites Manager
A tool for managing and showcasing one-page websites in your portfolio.

Usage:
    python onesite_manager.py scan              # Scan and detect all one-page sites
    python onesite_manager.py list              # Show all detected sites
    python onesite_manager.py update            # Update metadata for all sites
    python onesite_manager.py generate          # Generate HTML section for main website
    python onesite_manager.py validate          # Validate all sites and configurations
"""

import os
import sys
import json
import re
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
from html.parser import HTMLParser
import shutil

class TitleExtractor(HTMLParser):
    """HTML parser to extract title from HTML files."""
    
    def __init__(self):
        super().__init__()
        self.title = ""
        self.in_title = False
        self.in_head = True
        
    def handle_starttag(self, tag, attrs):
        if tag.lower() == 'title' and self.in_head:
            self.in_title = True
        elif tag.lower() == 'body':
            self.in_head = False
            
    def handle_endtag(self, tag):
        if tag.lower() == 'title':
            self.in_title = False
            
    def handle_data(self, data):
        if self.in_title:
            self.title += data.strip()

class DescriptionExtractor(HTMLParser):
    """HTML parser to extract meta description from HTML files."""
    
    def __init__(self):
        super().__init__()
        self.description = ""
        
    def handle_starttag(self, tag, attrs):
        if tag.lower() == 'meta':
            attr_dict = dict(attrs)
            if attr_dict.get('name', '').lower() == 'description':
                self.description = attr_dict.get('content', '')

class OnesiteManager:
    def __init__(self):
        self.base_dir = Path(".")
        self.onesite_dir = Path("one_page_websites")
        self.config_file = Path("onesites.json")
        self.cache_file = Path(".onesites_cache.json")
        self.index_file = Path("index.html")
        self.backup_dir = Path(".backups")
        self.backup_dir.mkdir(exist_ok=True)
        
        # Load configuration and cache
        self.config = self.load_config()
        self.cache = self.load_cache()
        
    def load_config(self) -> Dict:
        """Load onesites configuration."""
        if not self.config_file.exists():
            return self.create_default_config()
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
            return self.create_default_config()
    
    def create_default_config(self) -> Dict:
        """Create default configuration for onesites."""
        default_config = {
            "settings": {
                "auto_scan": True,
                "cache_duration": 86400,  # 24 hours
                "onesite_dir": "one_page_websites",
                "section_title": "One Page Websites",
                "section_description": "Interactive explorations and specialized projects"
            },
            "metadata": {
                "last_updated": None,
                "total_sites": 0,
                "version": "1.0.0"
            }
        }
        
        self.save_config(default_config)
        return default_config
    
    def save_config(self, config: Dict = None):
        """Save configuration to file."""
        if config is None:
            config = self.config
            
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def load_cache(self) -> Dict:
        """Load cache data."""
        if not self.cache_file.exists():
            return {}
        
        try:
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                cache = json.load(f)
            
            # Clean expired cache entries
            current_time = time.time()
            cache_duration = self.config.get('settings', {}).get('cache_duration', 86400)
            
            for site_file in list(cache.keys()):
                if 'cached_at' in cache[site_file]:
                    if current_time - cache[site_file]['cached_at'] > cache_duration:
                        del cache[site_file]
            
            return cache
        except Exception as e:
            print(f"Error loading cache: {e}")
            return {}
    
    def save_cache(self):
        """Save cache to file."""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving cache: {e}")
    
    def extract_title_from_html(self, file_path: Path) -> str:
        """Extract title from HTML file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Try to extract title using HTML parser
            parser = TitleExtractor()
            parser.feed(content)
            
            if parser.title:
                return parser.title.strip()
            
            # Fallback: use regex
            title_match = re.search(r'<title[^>]*>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
            if title_match:
                return title_match.group(1).strip()
            
            # Final fallback: use filename
            return f"Website {file_path.stem}"
            
        except Exception as e:
            print(f"Error extracting title from {file_path}: {e}")
            return f"Website {file_path.stem}"
    
    def extract_description_from_html(self, file_path: Path) -> str:
        """Extract meta description from HTML file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Try to extract description using HTML parser
            parser = DescriptionExtractor()
            parser.feed(content)
            
            if parser.description:
                return parser.description.strip()
            
            # Fallback: extract first meaningful paragraph from body content
            # Remove script, style, and other non-content tags first
            clean_content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL | re.IGNORECASE)
            clean_content = re.sub(r'<style[^>]*>.*?</style>', '', clean_content, flags=re.DOTALL | re.IGNORECASE)
            clean_content = re.sub(r'<head[^>]*>.*?</head>', '', clean_content, flags=re.DOTALL | re.IGNORECASE)
            
            # Extract text from body content only
            body_match = re.search(r'<body[^>]*>(.*?)</body>', clean_content, re.DOTALL | re.IGNORECASE)
            if body_match:
                body_content = body_match.group(1)
            else:
                body_content = clean_content
            
            # Remove HTML tags and clean up text
            text_content = re.sub(r'<[^>]+>', ' ', body_content)
            text_content = re.sub(r'\s+', ' ', text_content).strip()
            
            # Look for the first substantial paragraph
            paragraphs = text_content.split('\n')
            for paragraph in paragraphs:
                paragraph = paragraph.strip()
                # Skip common unwanted content
                if (len(paragraph) > 30 and 
                    not paragraph.lower().startswith(('the ', 'a ', 'an ')) and
                    '.' in paragraph and
                    not any(skip in paragraph.lower() for skip in ['font-family', 'css', 'javascript', 'html', 'doctype'])):
                    
                    # Get first sentence or reasonable length
                    sentences = paragraph.split('.')
                    first_sentence = sentences[0].strip()
                    if len(first_sentence) > 50:
                        return first_sentence[:200] + ("..." if len(first_sentence) > 200 else ".")
            
            # Alternative: look for first text after headers
            lines = text_content.split('\n')
            for i, line in enumerate(lines):
                line = line.strip()
                if (len(line) > 40 and 
                    not any(skip in line.lower() for skip in ['font-family', 'css', 'javascript', 'navigation', 'menu']) and
                    '.' in line):
                    return line[:200] + ("..." if len(line) > 200 else "")
            
            return "Interactive one-page website exploring specialized topics"
            
        except Exception as e:
            print(f"Error extracting description from {file_path}: {e}")
            return "Interactive one-page website"
    
    def scan_onesites(self) -> List[Dict]:
        """Scan the one_page_websites directory for numbered HTML files."""
        if not self.onesite_dir.exists():
            print(f"One-page websites directory not found: {self.onesite_dir}")
            return []
        
        sites = []
        
        # Look for numbered HTML files (1.html, 2.html, etc.)
        for file_path in self.onesite_dir.glob("*.html"):
            # Check if filename is a number
            if re.match(r'^\d+\.html$', file_path.name):
                site_data = self.get_site_data(file_path)
                if site_data:
                    sites.append(site_data)
        
        # Sort by number
        sites.sort(key=lambda x: x['number'])
        return sites
    
    def get_site_data(self, file_path: Path, force_update: bool = False) -> Optional[Dict]:
        """Get site data from cache or extract fresh data."""
        file_key = str(file_path)
        
        # Check cache first
        if not force_update and file_key in self.cache:
            # Verify file hasn't been modified
            cached_data = self.cache[file_key]
            if cached_data.get('file_mtime') == file_path.stat().st_mtime:
                print(f"Using cached data for {file_path.name}")
                return cached_data
        
        # Extract fresh data
        try:
            file_stat = file_path.stat()
            number = int(file_path.stem)
            
            print(f"Extracting data for {file_path.name}...")
            
            site_data = {
                'number': number,
                'filename': file_path.name,
                'title': self.extract_title_from_html(file_path),
                'description': self.extract_description_from_html(file_path),
                'file_path': str(file_path),
                'relative_path': f"{self.onesite_dir.name}/{file_path.name}",
                'file_size': file_stat.st_size,
                'file_mtime': file_stat.st_mtime,
                'created_at': datetime.fromtimestamp(file_stat.st_ctime).isoformat(),
                'modified_at': datetime.fromtimestamp(file_stat.st_mtime).isoformat(),
                'cached_at': time.time()
            }
            
            # Cache the data
            self.cache[file_key] = site_data
            self.save_cache()
            
            return site_data
            
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return None
    
    def list_sites(self):
        """List all detected one-page websites."""
        sites = self.scan_onesites()
        
        if not sites:
            print("No one-page websites found.")
            return
        
        print("\n" + "="*80)
        print("ONE-PAGE WEBSITES PORTFOLIO")
        print("="*80)
        print(f"{'#':<3} {'Title':<40} {'Size':<8} {'Modified':<20}")
        print("="*80)
        
        for site in sites:
            size_kb = site['file_size'] / 1024
            modified = datetime.fromisoformat(site['modified_at']).strftime('%Y-%m-%d %H:%M')
            title = site['title'][:38] + "..." if len(site['title']) > 38 else site['title']
            
            print(f"{site['number']:<3} {title:<40} {size_kb:>6.1f}K {modified:<20}")
        
        print("="*80)
        print(f"Total sites: {len(sites)}")
        print(f"Last updated: {self.config['metadata'].get('last_updated', 'Never')}")
    
    def update_sites(self, force: bool = False):
        """Update metadata for all one-page websites."""
        sites = self.scan_onesites()
        
        if not sites:
            print("No one-page websites to update.")
            return
        
        print(f"\nUpdating {len(sites)} one-page websites...")
        updated_count = 0
        
        for site in sites:
            file_path = Path(site['file_path'])
            print(f"[{site['number']}] Updating {file_path.name}")
            
            updated_data = self.get_site_data(file_path, force_update=force)
            if updated_data:
                updated_count += 1
            else:
                print(f"  ❌ Failed to update")
        
        # Update metadata
        self.config['metadata']['total_sites'] = len(sites)
        self.config['metadata']['last_updated'] = datetime.now().isoformat()
        self.save_config()
        
        print(f"\n✅ Updated {updated_count}/{len(sites)} sites successfully!")
    
    def generate_html_section(self) -> str:
        """Generate HTML section for the main website."""
        sites = self.scan_onesites()
        
        if not sites:
            return ""
        
        section_title = self.config['settings']['section_title']
        section_description = self.config['settings']['section_description']
        
        html_lines = [
            '        <!-- One Page Websites Section -->',
            '        <section class="onesite-section">',
            '            <div class="onesite-container">',
            f'                <h2 class="onesite-title">{section_title}</h2>',
            f'                <p class="onesite-description">{section_description}</p>',
            '                <div class="onesite-grid">'
        ]
        
        for site in sites:
            html_lines.append(self.generate_site_card(site))
        
        html_lines.extend([
            '                </div>',
            '            </div>',
            '        </section>'
        ])
        
        return '\n'.join(html_lines)
    
    def generate_site_card(self, site: Dict) -> str:
        """Generate HTML card for a single one-page website."""
        return f"""                    <div class="onesite-card">
                        <div class="onesite-header">
                            <h3 class="onesite-name">{site['title']}</h3>
                            <span class="onesite-number">#{site['number']}</span>
                        </div>
                        <p class="onesite-card-description">{site['description']}</p>
                        <div class="onesite-links">
                            <a href="{site['relative_path']}" target="_blank" class="onesite-link">Launch →</a>
                        </div>
                    </div>"""
    
    def generate_index_page(self):
        """Update index.html with the one-page websites section."""
        if not self.index_file.exists():
            print(f"Index file not found: {self.index_file}")
            return False
        
        # Create backup
        backup_path = self.backup_dir / f"index_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        shutil.copy2(self.index_file, backup_path)
        print(f"Backup created: {backup_path}")
        
        # Read current index.html
        with open(self.index_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Generate onesite section
        onesite_html = self.generate_html_section()
        
        if not onesite_html:
            print("No one-page websites found. Nothing to generate.")
            return False
        
        # Remove existing onesite section if present
        onesite_pattern = r'\s*<!-- One Page Websites Section -->.*?</section>\s*'
        html_content = re.sub(onesite_pattern, '\n', html_content, flags=re.DOTALL)
        
        # Find insertion point (before closing </body>)
        insertion_pattern = r'(\s*</body>)'
        
        # Insert onesite section before closing body tag
        new_content = re.sub(
            insertion_pattern,
            f'\n{onesite_html}\n\\1',
            html_content
        )
        
        # Write updated content
        with open(self.index_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ Index page updated with {len(self.scan_onesites())} one-page websites!")
        return True
    
    def validate_sites(self):
        """Validate all one-page websites and configuration."""
        print("\n" + "="*60)
        print("ONE-PAGE WEBSITES VALIDATION")
        print("="*60)
        
        issues = []
        
        # Check directory exists
        if not self.onesite_dir.exists():
            issues.append(f"One-page websites directory missing: {self.onesite_dir}")
        
        # Check for sites
        sites = self.scan_onesites()
        if not sites:
            issues.append("No numbered HTML files found (1.html, 2.html, etc.)")
        
        # Validate each site
        for site in sites:
            file_path = Path(site['file_path'])
            if not file_path.exists():
                issues.append(f"Site file missing: {file_path}")
            
            if not site['title'] or site['title'] == f"Website {file_path.stem}":
                issues.append(f"No proper title found for {file_path.name}")
        
        # Report results
        if issues:
            print("⚠️  Issues found:")
            for issue in issues:
                print(f"   - {issue}")
        else:
            print("✅ All validations passed!")
        
        print(f"\nSummary:")
        print(f"  Sites found: {len(sites)}")
        print(f"  Issues: {len(issues)}")
        print(f"  Directory: {self.onesite_dir}")

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    
    manager = OnesiteManager()
    command = sys.argv[1].lower()
    
    if command == 'scan':
        sites = manager.scan_onesites()
        print(f"Found {len(sites)} one-page websites")
        
    elif command == 'list':
        manager.list_sites()
        
    elif command == 'update':
        force = '--force' in sys.argv
        manager.update_sites(force=force)
        
    elif command == 'generate':
        manager.generate_index_page()
        
    elif command == 'validate':
        manager.validate_sites()
        
    else:
        print(f"Unknown command: {command}")
        print(__doc__)

if __name__ == "__main__":
    main()