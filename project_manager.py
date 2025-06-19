#!/usr/bin/env python3
"""
GitHub Projects Manager
A simple tool for managing GitHub project showcases on your portfolio.

Usage:
    python project_manager.py add <github_url>     # Add new project
    python project_manager.py list                 # Show all projects
    python project_manager.py update               # Fetch latest GitHub data
    python project_manager.py generate             # Generate HTML for projects page
    python project_manager.py remove <project>     # Remove project
    python project_manager.py validate             # Validate configuration
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
from urllib.parse import urlparse

class ProjectManager:
    def __init__(self):
        self.config_file = Path("projects.json")
        self.cache_file = Path(".projects_cache.json")
        self.projects_html = Path("projects.html")
        self.backup_dir = Path(".backups")
        self.backup_dir.mkdir(exist_ok=True)
        
        # GitHub API settings
        self.github_api_base = "https://api.github.com/repos"
        self.rate_limit_delay = 1.2  # Seconds between API calls
        
        # Load configuration
        self.config = self.load_config()
        self.cache = self.load_cache()
    
    def load_config(self) -> Dict:
        """Load projects configuration."""
        if not self.config_file.exists():
            print(f"Configuration file {self.config_file} not found!")
            return self.create_default_config()
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading configuration: {e}")
            return self.create_default_config()
    
    def create_default_config(self) -> Dict:
        """Create default configuration."""
        default_config = {
            "projects": [],
            "settings": {
                "auto_update": True,
                "cache_duration": 86400,
                "github_api_url": "https://api.github.com/repos",
                "cache_file": ".projects_cache.json"
            },
            "metadata": {
                "last_updated": None,
                "total_projects": 0,
                "version": "2.0.0"
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
        """Load cached GitHub data."""
        if not self.cache_file.exists():
            return {}
        
        try:
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                cache = json.load(f)
                
            # Check cache expiration
            cache_duration = self.config.get('settings', {}).get('cache_duration', 86400)
            current_time = time.time()
            
            # Remove expired entries
            for repo_url in list(cache.keys()):
                if 'cached_at' in cache[repo_url]:
                    if current_time - cache[repo_url]['cached_at'] > cache_duration:
                        del cache[repo_url]
            
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
    
    def parse_github_url(self, url: str) -> Optional[tuple]:
        """Parse GitHub URL to extract owner and repo name."""
        # Handle various GitHub URL formats
        patterns = [
            r'github\.com/([^/]+)/([^/]+?)(?:\.git)?/?$',
            r'github\.com/([^/]+)/([^/]+)/.*'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                owner, repo = match.groups()
                # Clean repo name (remove .git suffix if present)
                repo = repo.replace('.git', '')
                return owner, repo
        
        return None
    
    def fetch_github_data(self, repo_url: str) -> Optional[Dict]:
        """Fetch repository data from GitHub API."""
        parsed = self.parse_github_url(repo_url)
        if not parsed:
            print(f"Invalid GitHub URL: {repo_url}")
            return None
        
        owner, repo = parsed
        api_url = f"{self.github_api_base}/{owner}/{repo}"
        
        print(f"Fetching data for {owner}/{repo}...")
        
        try:
            # Add delay to respect rate limits
            time.sleep(self.rate_limit_delay)
            
            response = requests.get(api_url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract relevant information
            project_data = {
                'name': data.get('name'),
                'full_name': data.get('full_name'),
                'description': data.get('description') or 'No description available',
                'language': data.get('language'),
                'stars': data.get('stargazers_count', 0),
                'forks': data.get('forks_count', 0),
                'watchers': data.get('watchers_count', 0),
                'open_issues': data.get('open_issues_count', 0),
                'topics': data.get('topics', []),
                'homepage': data.get('homepage'),
                'license': data.get('license', {}).get('name') if data.get('license') else None,
                'created_at': data.get('created_at'),
                'updated_at': data.get('updated_at'),
                'pushed_at': data.get('pushed_at'),
                'size': data.get('size', 0),
                'default_branch': data.get('default_branch', 'main'),
                'html_url': data.get('html_url'),
                'clone_url': data.get('clone_url'),
                'ssh_url': data.get('ssh_url'),
                'cached_at': time.time()
            }
            
            return project_data
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for {repo_url}: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error fetching data for {repo_url}: {e}")
            return None
    
    def get_project_data(self, repo_url: str, force_update: bool = False) -> Optional[Dict]:
        """Get project data from cache or fetch from GitHub."""
        # Check cache first
        if not force_update and repo_url in self.cache:
            print(f"Using cached data for {repo_url}")
            return self.cache[repo_url]
        
        # Fetch fresh data
        data = self.fetch_github_data(repo_url)
        if data:
            self.cache[repo_url] = data
            self.save_cache()
        
        return data
    
    def add_project(self, repo_url: str):
        """Add a new project to the configuration."""
        print(f"\nAdding project: {repo_url}")
        
        # Validate URL
        parsed = self.parse_github_url(repo_url)
        if not parsed:
            print(f"❌ Invalid GitHub URL: {repo_url}")
            return False
        
        # Check if already exists
        if repo_url in self.config.get('projects', []):
            print(f"❌ Project already exists: {repo_url}")
            return False
        
        # Fetch project data
        project_data = self.get_project_data(repo_url)
        if not project_data:
            print(f"❌ Failed to fetch project data")
            return False
        
        # Add to projects list
        if 'projects' not in self.config:
            self.config['projects'] = []
        self.config['projects'].append(repo_url)
        
        # Update metadata
        self.config['metadata']['total_projects'] = len(self.config['projects'])
        self.config['metadata']['last_updated'] = datetime.now().isoformat()
        
        # Save configuration
        self.save_config()
        
        print(f"✅ Project added successfully!")
        print(f"   Name: {project_data['name']}")
        print(f"   Description: {project_data['description']}")
        print(f"   Language: {project_data['language']}")
        print(f"   Stars: {project_data['stars']}")
        
        return True
    
    def get_all_project_urls(self) -> List[str]:
        """Get all project URLs from configuration."""
        return self.config.get('projects', [])
    
    def list_projects(self):
        """List all projects with their information."""
        all_urls = self.get_all_project_urls()
        
        if not all_urls:
            print("No projects found.")
            return
        
        print("\n" + "="*80)
        print("GITHUB PROJECTS PORTFOLIO")
        print("="*80)
        print(f"{'#':<3} {'Name':<25} {'Language':<12} {'⭐':<5} {'🍴':<5} {'Description':<30}")
        print("="*80)
        
        for i, url in enumerate(all_urls, 1):
            project_data = self.get_project_data(url)
            if project_data:
                name = project_data['name'][:23] if project_data['name'] else 'Unknown'
                language = project_data['language'][:10] if project_data['language'] else 'None'
                stars = str(project_data['stars'])
                forks = str(project_data['forks'])
                description = project_data['description'][:28] if project_data['description'] else 'No description'
                
                print(f"{i:<3} {name:<25} {language:<12} {stars:<5} {forks:<5} {description:<30}")
            else:
                print(f"{i:<3} {'ERROR':<25} {'N/A':<12} {'N/A':<5} {'N/A':<5} {'Failed to fetch data':<30}")
        
        print("="*80)
        print(f"Total projects: {len(all_urls)}")
        print(f"Last updated: {self.config['metadata'].get('last_updated', 'Never')}")
    
    def update_projects(self, force: bool = False):
        """Update all project data from GitHub."""
        all_urls = self.get_all_project_urls()
        
        if not all_urls:
            print("No projects to update.")
            return
        
        print(f"\nUpdating {len(all_urls)} projects...")
        updated_count = 0
        
        for i, url in enumerate(all_urls, 1):
            print(f"[{i}/{len(all_urls)}] Updating {url}")
            
            project_data = self.get_project_data(url, force_update=force)
            if project_data:
                updated_count += 1
            else:
                print(f"  ❌ Failed to update")
        
        # Update metadata
        self.config['metadata']['last_updated'] = datetime.now().isoformat()
        self.save_config()
        
        print(f"\n✅ Updated {updated_count}/{len(all_urls)} projects successfully!")
    
    def generate_project_html(self) -> str:
        """Generate HTML for project showcase section."""
        project_urls = self.config.get('projects', [])
        
        if not project_urls:
            return ""
        
        html = ['            <div class="projects-section">',
                '                <h2 class="section-title">Project Portfolio</h2>',
                '                <p class="section-description">Explore my computational physics and AI projects, each solving real-world problems while advancing scientific understanding.</p>',
                '                <div class="projects-grid">']
        
        for url in project_urls:
            project_data = self.get_project_data(url)
            if project_data:
                html.append(self.generate_project_card(project_data))
        
        html.extend(['                </div>',
                     '            </div>'])
        
        return '\n'.join(html)
    
    
    
    def generate_project_card(self, project_data: Dict) -> str:
        """Generate HTML for a single project card."""
        # Format topics
        topics_html = ""
        if project_data.get('topics'):
            topics = project_data['topics'][:3]  # Limit to 3 topics
            topics_html = ''.join([f'<span class="project-topic">{topic}</span>' for topic in topics])
        
        # Format language badge
        language_html = f'<span class="project-language">{project_data["language"]}</span>' if project_data.get('language') else ''
        
        # Format stats
        stats_html = f"""
                            <div class="project-stats">
                                <span class="project-stat">⭐ {project_data['stars']}</span>
                                <span class="project-stat">🍴 {project_data['forks']}</span>
                            </div>"""
        
        return f"""                    <div class="project-card">
                        <div class="project-header">
                            <h3 class="project-name">{project_data['name']}</h3>
                            {language_html}
                        </div>
                        <p class="project-description">{project_data['description']}</p>
                        <div class="project-topics">
                            {topics_html}
                        </div>
                        {stats_html}
                        <div class="project-links">
                            <a href="{project_data['html_url']}" target="_blank" class="project-link">View on GitHub →</a>
                        </div>
                    </div>"""
    
    def generate_projects_page(self):
        """Generate the complete projects.html with dynamic content."""
        if not self.projects_html.exists():
            print(f"Projects HTML file not found: {self.projects_html}")
            return False
        
        # Create backup
        backup_path = self.backup_dir / f"projects_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        import shutil
        shutil.copy2(self.projects_html, backup_path)
        print(f"Backup created: {backup_path}")
        
        # Read current projects.html
        with open(self.projects_html, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Generate project sections
        project_html = self.generate_project_html()
        
        # Find insertion point (before closing </div> and </main>)
        insertion_pattern = r'(</div>\s*</main>)'
        
        if project_html:
            # Insert project sections before the closing tags
            new_content = re.sub(
                insertion_pattern,
                f'\n{project_html}\n\\1',
                html_content
            )
        else:
            new_content = html_content
        
        # Write updated content
        with open(self.projects_html, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ Projects page updated successfully!")
        return True
    
    def remove_project(self, identifier: str):
        """Remove a project by URL or name."""
        projects = self.config.get('projects', [])
        
        # Find project to remove
        url_to_remove = None
        for url in projects:
            parsed = self.parse_github_url(url)
            if identifier in url or (parsed and identifier == parsed[1]):
                url_to_remove = url
                break
        
        if not url_to_remove:
            print(f"❌ Project not found: {identifier}")
            return False
        
        # Remove from projects list
        self.config['projects'].remove(url_to_remove)
        
        # Remove from cache
        if url_to_remove in self.cache:
            del self.cache[url_to_remove]
            self.save_cache()
        
        # Update metadata
        self.config['metadata']['total_projects'] = len(self.config['projects'])
        self.config['metadata']['last_updated'] = datetime.now().isoformat()
        
        # Save configuration
        self.save_config()
        
        print(f"✅ Project removed successfully: {url_to_remove}")
        return True
    
    def validate_config(self):
        """Validate configuration and project data."""
        print("\n" + "="*60)
        print("PROJECT CONFIGURATION VALIDATION")
        print("="*60)
        
        issues = []
        
        # Check configuration structure
        required_keys = ['projects', 'settings', 'metadata']
        for key in required_keys:
            if key not in self.config:
                issues.append(f"Missing required configuration key: {key}")
        
        # Validate project URLs
        project_urls = self.config.get('projects', [])
        print(f"Validating {len(project_urls)} project URLs...")
        
        for url in project_urls:
            parsed = self.parse_github_url(url)
            if not parsed:
                issues.append(f"Invalid GitHub URL: {url}")
                continue
            
            # Check if data can be fetched
            project_data = self.get_project_data(url)
            if not project_data:
                issues.append(f"Cannot fetch data for: {url}")
        
        # Report results
        if issues:
            print(f"\n❌ Found {len(issues)} issues:")
            for issue in issues:
                print(f"  - {issue}")
        else:
            print(f"\n✅ Configuration is valid!")
            print(f"  - {len(project_urls)} projects configured")
            print(f"  - Cache contains {len(self.cache)} entries")
        
        print("="*60)

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    command = sys.argv[1].lower()
    project_manager = ProjectManager()
    
    if command == "add":
        if len(sys.argv) < 3:
            print("Usage: python project_manager.py add <github_url>")
            sys.exit(1)
        
        github_url = sys.argv[2]
        project_manager.add_project(github_url)
        
    elif command == "list":
        project_manager.list_projects()
        
    elif command == "update":
        force = "--force" in sys.argv
        project_manager.update_projects(force)
        
    elif command == "generate":
        project_manager.generate_projects_page()
        
    elif command == "remove":
        if len(sys.argv) < 3:
            print("Usage: python project_manager.py remove <project_identifier>")
            sys.exit(1)
        
        identifier = sys.argv[2]
        project_manager.remove_project(identifier)
        
    elif command == "validate":
        project_manager.validate_config()
        
    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)

if __name__ == "__main__":
    main()