#!/usr/bin/env python3
"""
Google Scholar Research Manager
A comprehensive tool for automatically fetching and displaying research publications from Google Scholar.

Usage:
    python scholar_manager.py update                # Fetch latest publications from Google Scholar
    python scholar_manager.py generate             # Update research.html with publication cards
    python scholar_manager.py list                 # Show all cached publications
    python scholar_manager.py validate             # Check system integrity
    python scholar_manager.py add                  # Manually add a publication
    python scholar_manager.py remove --id ID       # Remove a publication
"""

import os
import sys
import json
import time
import re
import requests
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
import argparse
import urllib.parse
import html

class ScholarManager:
    def __init__(self):
        self.config_file = Path("scholar_config.json")
        self.cache_file = Path(".scholar_cache.json")
        self.research_html = Path("research.html")
        self.backup_dir = Path(".backups")
        self.backup_dir.mkdir(exist_ok=True)
        
        # Default Google Scholar settings
        self.user_id = "3cqkF08AAAAJ"  # From provided URL
        self.scholar_base_url = "https://scholar.google.com/citations"
        self.rate_limit_delay = 2.0  # Seconds between requests
        
        # Load configuration
        self.config = self.load_config()
        self.cache = self.load_cache()
    
    def load_config(self) -> Dict:
        """Load scholar configuration."""
        if not self.config_file.exists():
            return self.create_default_config()
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
            return self.create_default_config()
    
    def create_default_config(self) -> Dict:
        """Create default configuration."""
        default_config = {
            "profile": {
                "user_id": self.user_id,
                "name": "Manas Pandey",
                "affiliation": "IIT Kanpur",
                "profile_url": f"{self.scholar_base_url}?user={self.user_id}&hl=en"
            },
            "settings": {
                "auto_update": True,
                "cache_duration": 86400,  # 24 hours
                "max_publications": 50,
                "sort_by": "year",  # year, citations, title
                "include_citations": True,
                "include_pdf_links": True
            },
            "display": {
                "cards_per_row": 2,
                "show_abstract": False,
                "highlight_recent": True,
                "recent_months": 12
            },
            "metadata": {
                "last_updated": None,
                "total_publications": 0,
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
            print(f"Error saving configuration: {e}")
    
    def load_cache(self) -> Dict:
        """Load cached publication data."""
        if not self.cache_file.exists():
            return {"publications": [], "last_updated": None, "profile_data": {}}
        
        try:
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                cache = json.load(f)
                
            # Check cache expiration
            cache_duration = self.config.get('settings', {}).get('cache_duration', 86400)
            if cache.get('last_updated'):
                last_updated = datetime.fromisoformat(cache['last_updated'])
                if (datetime.now() - last_updated).total_seconds() > cache_duration:
                    print("📅 Cache expired, will fetch fresh data")
                    return {"publications": [], "last_updated": None, "profile_data": {}}
            
            return cache
        except Exception as e:
            print(f"Error loading cache: {e}")
            return {"publications": [], "last_updated": None, "profile_data": {}}
    
    def save_cache(self):
        """Save cache to file."""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving cache: {e}")
    
    def create_backup(self) -> Optional[Path]:
        """Create backup of current research.html."""
        if not self.research_html.exists():
            return None
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.backup_dir / f"research_backup_{timestamp}.html"
        
        try:
            import shutil
            shutil.copy2(self.research_html, backup_path)
            print(f"✅ Backup created: {backup_path}")
            return backup_path
        except Exception as e:
            print(f"❌ Failed to create backup: {e}")
            return None
    
    def fetch_scholar_data(self) -> bool:
        """Fetch publications from Google Scholar profile."""
        print("🔍 Fetching publications from Google Scholar...")
        
        profile_url = self.config['profile']['profile_url']
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        try:
            response = requests.get(profile_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            html_content = response.text
            
            # Extract profile information
            profile_data = self.extract_profile_data(html_content)
            
            # Extract publications
            publications = self.extract_publications(html_content)
            
            # Update cache
            self.cache = {
                "publications": publications,
                "profile_data": profile_data,
                "last_updated": datetime.now().isoformat(),
                "fetch_url": profile_url
            }
            
            self.save_cache()
            
            # Update config metadata
            self.config['metadata']['total_publications'] = len(publications)
            self.config['metadata']['last_updated'] = datetime.now().isoformat()
            self.save_config()
            
            print(f"✅ Successfully fetched {len(publications)} publications")
            return True
            
        except requests.RequestException as e:
            print(f"❌ Network error fetching Scholar data: {e}")
            return False
        except Exception as e:
            print(f"❌ Error parsing Scholar data: {e}")
            return False
    
    def extract_profile_data(self, html_content: str) -> Dict:
        """Extract profile information from Scholar page HTML."""
        profile_data = {}
        
        try:
            # Name
            name_match = re.search(r'<div[^>]*id=["\']gsc_prf_in["\'][^>]*>([^<]+)', html_content)
            if name_match:
                profile_data['name'] = html.unescape(name_match.group(1).strip())
            
            # Affiliation
            affiliation_match = re.search(r'<div[^>]*class=["\'][^"\']*gsc_prf_il[^"\']*["\'][^>]*>([^<]+)', html_content)
            if affiliation_match:
                profile_data['affiliation'] = html.unescape(affiliation_match.group(1).strip())
            
            # Research interests - extract text from links within gsc_prf_int div
            interests_section = re.search(r'<div[^>]*id=["\']gsc_prf_int["\'][^>]*>(.*?)</div>', html_content, re.DOTALL)
            if interests_section:
                interests = re.findall(r'<a[^>]*>([^<]+)</a>', interests_section.group(1))
                profile_data['interests'] = [html.unescape(interest.strip()) for interest in interests]
            
            # Citation metrics - basic extraction
            metrics = {}
            citations_match = re.search(r'Citations</td><td[^>]*>(\d+)</td><td[^>]*>(\d+)</td>', html_content)
            if citations_match:
                metrics['Citations'] = {
                    'all_time': citations_match.group(1),
                    'since_2019': citations_match.group(2)
                }
            
            h_index_match = re.search(r'h-index</td><td[^>]*>(\d+)</td><td[^>]*>(\d+)</td>', html_content)
            if h_index_match:
                metrics['h-index'] = {
                    'all_time': h_index_match.group(1),
                    'since_2019': h_index_match.group(2)
                }
                
            if metrics:
                profile_data['metrics'] = metrics
                
        except Exception as e:
            print(f"⚠️  Error extracting profile data: {e}")
        
        return profile_data
    
    def extract_publications(self, html_content: str) -> List[Dict]:
        """Extract publication list from Scholar page HTML."""
        publications = []
        
        try:
            # Find publications table section
            table_match = re.search(r'<table[^>]*id=["\']gsc_a_t["\'][^>]*>(.*?)</table>', html_content, re.DOTALL)
            if not table_match:
                print("❌ Could not find publications table")
                return publications
            
            table_content = table_match.group(1)
            
            # Find all publication rows
            rows = re.findall(r'<tr[^>]*class=["\'][^"\']*gsc_a_tr[^"\']*["\'][^>]*>(.*?)</tr>', table_content, re.DOTALL)
            
            for i, row_html in enumerate(rows, 1):
                try:
                    pub_data = self.extract_publication_data(row_html, i)
                    if pub_data:
                        publications.append(pub_data)
                        print(f"  📄 {i}. {pub_data['title'][:50]}...")
                        
                        # Rate limiting
                        time.sleep(self.rate_limit_delay)
                        
                except Exception as e:
                    print(f"⚠️  Error extracting publication {i}: {e}")
                    continue
                    
        except Exception as e:
            print(f"❌ Error extracting publications: {e}")
        
        return publications
    
    def extract_publication_data(self, row_html: str, index: int) -> Optional[Dict]:
        """Extract data for a single publication from HTML row."""
        try:
            pub_data = {"id": index}
            
            # Title and link
            title_match = re.search(r'<a[^>]*class=["\'][^"\']*gsc_a_at[^"\']*["\'][^>]*href=["\']([^"\']+)["\'][^>]*>([^<]+)</a>', row_html)
            if title_match:
                pub_data['scholar_url'] = 'https://scholar.google.com' + title_match.group(1)
                pub_data['title'] = html.unescape(title_match.group(2).strip())
            else:
                # Try simpler pattern if the first doesn't work
                title_simple = re.search(r'<a[^>]*class=["\'][^"\']*gsc_a_at[^"\']*["\'][^>]*>([^<]+)</a>', row_html)
                if title_simple:
                    pub_data['title'] = html.unescape(title_simple.group(1).strip())
                else:
                    pub_data['title'] = f"Publication {index}"
            
            # Authors and venue from gs_gray div
            gray_match = re.search(r'<div[^>]*class=["\'][^"\']*gs_gray[^"\']*["\'][^>]*>([^<]+)</div>', row_html)
            if gray_match:
                details_text = html.unescape(gray_match.group(1).strip())
                pub_data['authors_venue'] = details_text
                
                # Try to separate authors and venue
                if ' - ' in details_text:
                    parts = details_text.split(' - ', 1)
                    pub_data['authors'] = parts[0].strip()
                    pub_data['venue'] = parts[1].strip()
                else:
                    pub_data['authors'] = details_text
                    pub_data['venue'] = ''
            else:
                pub_data['authors'] = 'Unknown Authors'
                pub_data['venue'] = ''
            
            # Citation count
            cite_match = re.search(r'<a[^>]*class=["\'][^"\']*gsc_a_ac[^"\']*["\'][^>]*>(\d+)</a>', row_html)
            if cite_match:
                try:
                    pub_data['citations'] = int(cite_match.group(1))
                except ValueError:
                    pub_data['citations'] = 0
            else:
                pub_data['citations'] = 0
            
            # Year
            year_match = re.search(r'<span[^>]*class=["\'][^"\']*gsc_a_h[^"\']*["\'][^>]*>(\d{4})</span>', row_html)
            if year_match:
                try:
                    pub_data['year'] = int(year_match.group(1))
                except ValueError:
                    pub_data['year'] = None
            else:
                pub_data['year'] = None
            
            # Try to extract DOI or external links
            pub_data['doi'] = None
            pub_data['external_url'] = None
            
            # If we have scholar_url, try to fetch DOI from the publication page
            if 'scholar_url' in pub_data:
                try:
                    doi_info = self.extract_doi_from_scholar(pub_data['scholar_url'])
                    if doi_info:
                        pub_data.update(doi_info)
                except Exception as e:
                    print(f"  ⚠️  Could not fetch DOI for publication {index}: {e}")
            
            # Additional metadata
            pub_data['added_date'] = datetime.now().isoformat()
            pub_data['featured'] = index <= 3  # Feature top 3 publications
            
            return pub_data
            
        except Exception as e:
            print(f"Error processing publication row: {e}")
            return None
    
    def extract_doi_from_scholar(self, scholar_url: str) -> Optional[Dict]:
        """Extract DOI and external links from a Scholar publication page."""
        try:
            print(f"    🔗 Fetching DOI from Scholar page...")
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(scholar_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            html_content = response.text
            link_info = {}
            
            # Try to find DOI links in various formats
            doi_patterns = [
                r'https?://(?:dx\.)?doi\.org/(10\.\S+)',
                r'doi:?\s*(10\.\S+)',
                r'DOI:?\s*(10\.\S+)'
            ]
            
            for pattern in doi_patterns:
                doi_match = re.search(pattern, html_content, re.IGNORECASE)
                if doi_match:
                    doi = doi_match.group(1)
                    link_info['doi'] = doi
                    link_info['doi_url'] = f'https://doi.org/{doi}'
                    print(f"    ✅ Found DOI: {doi}")
                    break
            
            # Try to find external publication links
            external_patterns = [
                r'<a[^>]*href=["\']([^"\']*(?:arxiv\.org|pubmed|nature\.com|science\.org|aps\.org|iop\.org|springer\.com|wiley\.com|elsevier\.com)[^"\']*)["\'][^>]*>',
                r'<a[^>]*href=["\']([^"\']*\.pdf)["\'][^>]*>'
            ]
            
            for pattern in external_patterns:
                external_match = re.search(pattern, html_content, re.IGNORECASE)
                if external_match and not link_info.get('external_url'):
                    url = external_match.group(1)
                    if url.startswith('http'):
                        link_info['external_url'] = url
                        print(f"    🔗 Found external link: {url[:50]}...")
                        break
            
            # Rate limiting
            time.sleep(self.rate_limit_delay * 2)  # Longer delay for detailed pages
            
            return link_info if link_info else None
            
        except Exception as e:
            print(f"    ❌ Error fetching DOI: {e}")
            return None
    
    def list_publications(self):
        """Display all cached publications."""
        publications = self.cache.get('publications', [])
        
        if not publications:
            print("📚 No publications found in cache")
            print("Run 'python scholar_manager.py update' to fetch publications")
            return
        
        print("=" * 100)
        print("RESEARCH PUBLICATIONS")
        print("=" * 100)
        print(f"{'ID':<3} {'Title':<50} {'Year':<6} {'Citations':<10} {'Venue':<25}")
        print("=" * 100)
        
        for pub in publications:
            title = pub.get('title', 'Unknown')[:47] + ("..." if len(pub.get('title', '')) > 47 else "")
            year = str(pub.get('year', 'N/A'))
            citations = str(pub.get('citations', 0))
            venue = pub.get('venue', 'Unknown')[:22] + ("..." if len(pub.get('venue', '')) > 22 else "")
            
            print(f"{pub.get('id', 0):<3} {title:<50} {year:<6} {citations:<10} {venue:<25}")
        
        print("=" * 100)
        print(f"Total publications: {len(publications)}")
        
        # Show profile data if available
        profile_data = self.cache.get('profile_data', {})
        if profile_data.get('metrics'):
            print(f"\n📊 Citation Metrics:")
            for metric, values in profile_data['metrics'].items():
                print(f"   {metric}: {values.get('all_time', 'N/A')} (all time)")
    
    def update_research_html(self):
        """Update research.html with publication cards."""
        print("🔄 Updating research.html with publication cards...")
        
        # Create backup
        backup_path = self.create_backup()
        
        try:
            # Read current research.html
            if self.research_html.exists():
                with open(self.research_html, 'r', encoding='utf-8') as f:
                    content = f.read()
            else:
                print("❌ research.html not found")
                return False
            
            # Generate publications section HTML
            publications_html = self.generate_publications_html()
            
            # Insert publications section into research.html
            # Look for the main container and insert content
            main_pattern = r'(<main class="page-container">\s*)(.*?)(\s*</main>)'
            
            new_main_content = f'''
        <h1 class="page-title">Research</h1>
        
        <!-- Publications Section -->
        <section class="content-section">
            <h2 class="section-title">Publications</h2>
            <p class="section-description">Exploring the intersection of quantum mechanics and artificial intelligence</p>
            <div class="content-grid publications-grid">
{publications_html}
            </div>
        </section>
        
        <!-- Research Interests Section -->
        <section class="content-section">
            <h2 class="section-title">Research Interests</h2>
            <p class="section-description">Current areas of investigation and academic curiosity</p>
            <div class="content-grid interests-grid">
                <div class="interest-card">
                    <h3>Quantum Machine Learning</h3>
                    <p>Investigating the potential of quantum computing to enhance machine learning algorithms and exploring quantum-classical hybrid approaches.</p>
                </div>
                <div class="interest-card">
                    <h3>Experimental Physics</h3>
                    <p>Hands-on research in quantum optics and magnetometry, bridging theoretical concepts with practical implementations.</p>
                </div>
                <div class="interest-card">
                    <h3>AI in Scientific Discovery</h3>
                    <p>Applying artificial intelligence techniques to accelerate scientific research and uncover new patterns in complex physical systems.</p>
                </div>
            </div>
        </section>
'''
            
            updated_content = re.sub(main_pattern, f'\\1{new_main_content}\\3', content, flags=re.DOTALL)
            
            # Write updated content
            with open(self.research_html, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            print("✅ research.html updated successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error updating research.html: {e}")
            if backup_path and backup_path.exists():
                print(f"🔄 Restoring from backup: {backup_path}")
                import shutil
                shutil.copy2(backup_path, self.research_html)
            return False
    
    def generate_publications_html(self) -> str:
        """Generate HTML for publication cards."""
        publications = self.cache.get('publications', [])
        
        if not publications:
            return '''
                <div class="no-publications">
                    <p>Publications will appear here automatically when they are found on Google Scholar.</p>
                    <p>Run <code>python scholar_manager.py update</code> to fetch the latest publications.</p>
                </div>'''
        
        # Sort publications
        sort_by = self.config.get('settings', {}).get('sort_by', 'year')
        if sort_by == 'year':
            publications = sorted(publications, key=lambda x: x.get('year', 0), reverse=True)
        elif sort_by == 'citations':
            publications = sorted(publications, key=lambda x: x.get('citations', 0), reverse=True)
        
        html_parts = []
        
        for pub in publications:
            title = pub.get('title', 'Unknown Title')
            authors = pub.get('authors', 'Unknown Authors')
            venue = pub.get('venue', '')
            year = pub.get('year', 'N/A')
            citations = pub.get('citations', 0)
            scholar_url = pub.get('scholar_url', '')
            doi_url = pub.get('doi_url', '')
            external_url = pub.get('external_url', '')
            featured = pub.get('featured', False)
            
            # Determine best link for title - prefer DOI, then external, then Scholar
            title_link = doi_url or external_url or scholar_url
            link_icon = "📄" if doi_url else "🔗" if external_url else "📚"
            
            # Create publication card
            card_class = "publication-card featured" if featured else "publication-card"
            
            card_html = f'''
                <div class="{card_class}">
                    <div class="pub-header">
                        <h3 class="pub-title">
                            {title if not title_link else f'<a href="{title_link}" target="_blank" title="Click to open publication">{title}</a>'}
                        </h3>
                        <div class="pub-year">{year}</div>
                    </div>
                    <div class="pub-authors">{authors}</div>
                    {f'<div class="pub-venue">{venue}</div>' if venue else ''}
                    <div class="pub-metrics">
                        <span class="citations">📚 {citations} citation{'s' if citations != 1 else ''}</span>
                        <div class="pub-links">
                            {f'<a href="{doi_url}" target="_blank" class="doi-link" title="View DOI">📄 DOI</a>' if doi_url else ''}
                            {f'<a href="{external_url}" target="_blank" class="external-link" title="View Publication">🔗 Full Text</a>' if external_url and not doi_url else ''}
                            {f'<a href="{scholar_url}" target="_blank" class="scholar-link" title="View on Google Scholar">📚 Scholar</a>' if scholar_url and not doi_url and not external_url else ''}
                        </div>
                    </div>
                </div>'''
            
            html_parts.append(card_html)
        
        return '\n'.join(html_parts)
    
    def validate_system(self) -> List[str]:
        """Validate the scholar system integrity."""
        issues = []
        
        # Check config file
        if not self.config_file.exists():
            issues.append("Configuration file missing")
        
        # Check cache
        if not self.cache_file.exists():
            issues.append("Cache file missing - run update command")
        
        # Check research.html
        if not self.research_html.exists():
            issues.append("research.html file missing")
        
        # Validate cached data
        publications = self.cache.get('publications', [])
        if not publications:
            issues.append("No publications in cache - run update command")
        
        # Check for required fields in publications
        for i, pub in enumerate(publications):
            if not pub.get('title'):
                issues.append(f"Publication {i+1} missing title")
            if not pub.get('authors'):
                issues.append(f"Publication {i+1} missing authors")
        
        return issues
    
    def add_manual_publication(self):
        """Manually add a publication."""
        print("📝 Adding publication manually...")
        
        title = input("Title: ").strip()
        if not title:
            print("❌ Title is required")
            return
        
        authors = input("Authors: ").strip()
        venue = input("Venue/Journal: ").strip()
        year_str = input("Year: ").strip()
        
        try:
            year = int(year_str) if year_str else None
        except ValueError:
            year = None
        
        citations_str = input("Citation count (0): ").strip()
        try:
            citations = int(citations_str) if citations_str else 0
        except ValueError:
            citations = 0
        
        # Create publication entry
        pub_data = {
            "id": len(self.cache.get('publications', [])) + 1,
            "title": title,
            "authors": authors,
            "venue": venue,
            "year": year,
            "citations": citations,
            "added_date": datetime.now().isoformat(),
            "manual_entry": True,
            "featured": False
        }
        
        # Add to cache
        if 'publications' not in self.cache:
            self.cache['publications'] = []
        
        self.cache['publications'].append(pub_data)
        self.save_cache()
        
        print(f"✅ Added publication: {title}")
    
    def update_publication_links(self):
        """Update DOI and external links for existing publications."""
        publications = self.cache.get('publications', [])
        
        if not publications:
            print("📚 No publications found to update")
            return False
        
        print("🔗 Update Publication Links")
        print("=" * 50)
        
        for i, pub in enumerate(publications, 1):
            print(f"\n{i}. {pub.get('title', 'Unknown Title')}")
            print(f"   Current DOI: {pub.get('doi_url', 'None')}")
            print(f"   Current External URL: {pub.get('external_url', 'None')}")
            print(f"   Current Scholar URL: {pub.get('scholar_url', 'None')}")
            
            update = input(f"Update links for publication {i}? (y/n): ").strip().lower()
            if update == 'y':
                # Update DOI
                current_doi = pub.get('doi', '')
                new_doi = input(f"Enter DOI (current: {current_doi or 'None'}): ").strip()
                if new_doi:
                    pub['doi'] = new_doi
                    pub['doi_url'] = f"https://doi.org/{new_doi}"
                elif new_doi == '' and current_doi:
                    # Clear DOI if empty string entered
                    pub['doi'] = None
                    pub['doi_url'] = None
                
                # Update external URL
                current_external = pub.get('external_url', '')
                new_external = input(f"Enter external URL (current: {current_external or 'None'}): ").strip()
                if new_external:
                    if not new_external.startswith('http'):
                        new_external = f"https://{new_external}"
                    pub['external_url'] = new_external
                elif new_external == '' and current_external:
                    pub['external_url'] = None
                
                # Update Scholar URL
                current_scholar = pub.get('scholar_url', '')
                new_scholar = input(f"Enter Scholar URL (current: {current_scholar or 'None'}): ").strip()
                if new_scholar:
                    pub['scholar_url'] = new_scholar
                elif new_scholar == '' and current_scholar:
                    pub['scholar_url'] = None
                
                print(f"✅ Updated links for publication {i}")
        
        # Save cache
        self.cache['last_updated'] = datetime.now().isoformat()
        self.save_cache()
        
        print("✅ Publication links updated successfully")
        return True

def main():
    parser = argparse.ArgumentParser(description="Google Scholar Research Manager")
    parser.add_argument("command", choices=[
        "update", "generate", "list", "validate", "add", "links"
    ], help="Command to execute")
    parser.add_argument("--id", type=int, help="Publication ID for remove command")
    
    args = parser.parse_args()
    manager = ScholarManager()
    
    if args.command == "update":
        success = manager.fetch_scholar_data()
        if success:
            print("🔄 Automatically updating research.html...")
            manager.update_research_html()
    
    elif args.command == "generate":
        manager.update_research_html()
    
    elif args.command == "list":
        manager.list_publications()
    
    elif args.command == "validate":
        issues = manager.validate_system()
        if not issues:
            print("✅ Scholar system validation passed")
        else:
            print("⚠️  Validation issues found:")
            for issue in issues:
                print(f"   - {issue}")
    
    elif args.command == "add":
        manager.add_manual_publication()
    
    elif args.command == "links":
        manager.update_publication_links()
        print("🔄 Regenerating research.html...")
        manager.update_research_html()

if __name__ == "__main__":
    main()