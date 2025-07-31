#!/usr/bin/env python3
"""
Jekyll Blog Post Manager
A comprehensive tool for managing Jekyll blog posts locally.

Usage:
    python blog_manager.py add          # Create new post
    python blog_manager.py list         # Show all posts
    python blog_manager.py edit         # Edit existing post
    python blog_manager.py remove       # Remove post
    python blog_manager.py preview      # Preview post
    python blog_manager.py validate     # Validate all posts for consistency
"""

import os
import sys
import re
import yaml
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple

try:
    from PIL import Image, ImageFilter, ImageEnhance
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("Warning: PIL/Pillow not available. Image processing features disabled.")

class BlogManager:
    def __init__(self):
        self.posts_dir = Path("_posts")
        self.backup_dir = Path(".backups")
        self.images_dir = Path("blog/images")
        self.posts_images_dir = self.images_dir / "posts"
        
        # Create necessary directories
        self.backup_dir.mkdir(exist_ok=True)
        self.posts_dir.mkdir(exist_ok=True)
        self.images_dir.mkdir(exist_ok=True)
        self.posts_images_dir.mkdir(exist_ok=True)
        
        # Common categories for suggestions
        self.common_categories = ["ai", "philosophy", "personal", "literature", "research", "technical", 
                                "music", "physics", "creativity", "murakami", "poetry", "mathematics", "programming"]
    
    def create_frontmatter(self, data):
        """Create properly formatted frontmatter matching existing posts."""
        lines = ['---']
        lines.append(f'layout: {data["layout"]}')
        lines.append(f'title: "{data["title"]}"')
        lines.append(f'date: {data["date"]}')
        
        # Format categories as inline array
        if data["categories"]:
            categories_str = "[" + ", ".join(data["categories"]) + "]"
            lines.append(f'categories: {categories_str}')
        
        
        lines.append(f'excerpt: "{data["excerpt"]}"')
        lines.append(f'reading_time: {data["reading_time"]}')
        
        # Add image fields if present
        if data.get("hero_image"):
            lines.append(f'hero_image: "{data["hero_image"]}"')
        if data.get("hero_alt"):
            lines.append(f'hero_alt: "{data["hero_alt"]}"')
        
        lines.append('---')
        return '\n'.join(lines)
    
    def validate_post_data(self, title, categories, excerpt, date_input):
        """Validate post data for common issues."""
        issues = []
        
        # Check for common typos in categories
        typo_fixes = {
            "philosphy": "philosophy",
            "tecnical": "technical",
            "reseach": "research"
        }
        
        fixed_categories = []
        for cat in categories:
            if cat in typo_fixes:
                print(f"Warning: '{cat}' corrected to '{typo_fixes[cat]}'")
                fixed_categories.append(typo_fixes[cat])
            else:
                fixed_categories.append(cat)
        
        # Check date is not in future (more than 1 day)
        try:
            post_date = datetime.strptime(date_input.split()[0], "%Y-%m-%d")
            if post_date.date() > datetime.now().date():
                print(f"Warning: Post date {post_date.date()} is in the future. Consider using current date.")
        except:
            pass
        
        # Check title length
        if len(title) > 80:
            issues.append("Title is quite long (>80 chars). Consider shortening for better display.")
        
        # Check excerpt length
        if len(excerpt) > 200:
            issues.append("Excerpt is quite long (>200 chars). Consider shortening for better display.")
        
        return fixed_categories, issues
    
    def slugify(self, title: str) -> str:
        """Convert title to URL-friendly slug."""
        slug = re.sub(r'[^\w\s-]', '', title.lower())
        slug = re.sub(r'[-\s]+', '-', slug)
        return slug.strip('-')
    
    def calculate_reading_time(self, content: str) -> int:
        """Calculate reading time based on word count."""
        words = len(content.split())
        # Average reading speed: 200 words per minute
        return max(1, round(words / 200))
    
    def get_existing_categories(self) -> List[str]:
        """Extract all existing categories from posts."""
        categories = set()
        for post_file in self.posts_dir.glob("*.md"):
            try:
                with open(post_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if content.startswith('---'):
                        yaml_end = content.find('---', 3)
                        if yaml_end != -1:
                            frontmatter = yaml.safe_load(content[3:yaml_end])
                            if 'categories' in frontmatter:
                                categories.update(frontmatter['categories'])
            except Exception:
                continue
        return sorted(list(categories))
    
    def parse_post(self, post_file: Path) -> Optional[Dict]:
        """Parse a Jekyll post file and extract frontmatter and content."""
        try:
            with open(post_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if not content.startswith('---'):
                return None
            
            yaml_end = content.find('---', 3)
            if yaml_end == -1:
                return None
            
            frontmatter = yaml.safe_load(content[3:yaml_end])
            post_content = content[yaml_end + 3:].strip()
            
            return {
                'filename': post_file.name,
                'path': post_file,
                'frontmatter': frontmatter,
                'content': post_content
            }
        except Exception as e:
            print(f"Error parsing {post_file}: {e}")
            return None
    
    def create_backup(self, post_file: Path) -> Path:
        """Create a backup of a post file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{post_file.stem}_{timestamp}.md"
        backup_path = self.backup_dir / backup_name
        shutil.copy2(post_file, backup_path)
        return backup_path
    
    def ensure_year_directories(self, year: str):
        """Ensure year-based image directories exist."""
        posts_year_dir = self.posts_images_dir / year
        posts_year_dir.mkdir(exist_ok=True)
        return posts_year_dir
    
    
    def detect_hero_image_in_content(self, content: str) -> Optional[str]:
        """Detect the first image in post content that could be a hero image."""
        # Look for markdown image syntax at the start of content
        import re
        
        # Remove frontmatter first
        if content.startswith('---'):
            yaml_end = content.find('---', 3)
            if yaml_end != -1:
                content = content[yaml_end + 3:].strip()
        
        # Look for first image in first few lines
        lines = content.split('\n')[:10]  # Check first 10 lines
        for line in lines:
            line = line.strip()
            if line.startswith('!['):
                # Extract image path from markdown syntax
                match = re.search(r'!\[.*?\]\((.*?)\)', line)
                if match:
                    image_path = match.group(1)
                    # Handle Jekyll liquid tags
                    if '{{' in image_path and '}}' in image_path:
                        # Extract the actual path from liquid syntax
                        path_match = re.search(r'"([^"]*)"', image_path)
                        if path_match:
                            return path_match.group(1)
                    return image_path
        return None
    
    def process_post_images(self, post_slug: str, year: str, hero_image_path: str = None) -> Dict[str, str]:
        """Process images for a blog post - simple path handling without blur."""
        if not PIL_AVAILABLE:
            return {}
        
        # Ensure year directories exist
        posts_year_dir = self.ensure_year_directories(year)
        
        result = {}
        
        if hero_image_path:
            # Check if it's a relative path that needs to be converted to absolute
            if hero_image_path.startswith('/'):
                hero_image_path = hero_image_path[1:]  # Remove leading slash
            
            original_path = Path(hero_image_path)
            
            # If the path doesn't exist, try to find it in posts directory
            if not original_path.exists():
                # Try in posts directory
                potential_path = self.posts_images_dir / year / original_path.name
                if potential_path.exists():
                    original_path = potential_path
                else:
                    print(f"Warning: Hero image not found: {hero_image_path}")
                    return {}
            
            # Store the hero image path for frontmatter (no blur processing)
            if original_path.exists():
                result['hero_image'] = f"/blog/images/posts/{year}/{original_path.name}"
                print(f"✓ Hero image ready: {original_path}")
        
        return result
    
    def list_posts(self):
        """List all blog posts with details."""
        posts = []
        for post_file in sorted(self.posts_dir.glob("*.md"), reverse=True):
            post_data = self.parse_post(post_file)
            if post_data:
                posts.append(post_data)
        
        if not posts:
            print("No blog posts found.")
            return
        
        print("\n" + "="*80)
        print(f"{'#':<3} {'Title':<40} {'Date':<12} {'Tags':<20}")
        print("="*80)
        
        for i, post in enumerate(posts, 1):
            title = post['frontmatter'].get('title', 'No Title')[:38]
            date = str(post['frontmatter'].get('date', 'No Date'))[:10]
            tags = ', '.join(post['frontmatter'].get('tags', []))[:18]
            print(f"{i:<3} {title:<40} {date:<12} {tags:<20}")
        
        print("="*80 + "\n")
        return posts
    
    def select_post(self, posts: List[Dict]) -> Optional[Dict]:
        """Interactive post selection."""
        while True:
            try:
                choice = input(f"Select post (1-{len(posts)}) or 'q' to quit: ").strip()
                if choice.lower() == 'q':
                    return None
                
                index = int(choice) - 1
                if 0 <= index < len(posts):
                    return posts[index]
                else:
                    print(f"Please enter a number between 1 and {len(posts)}")
            except ValueError:
                print("Please enter a valid number or 'q' to quit")
    
    def input_multiselect(self, prompt: str, options: List[str], selected: List[str] = None) -> List[str]:
        """Multi-select input for tags/categories."""
        if selected is None:
            selected = []
        
        print(f"\n{prompt}")
        print("Available options:")
        for i, option in enumerate(options, 1):
            marker = "✓" if option in selected else " "
            print(f"  {i:2}. [{marker}] {option}")
        
        print(f"\nCurrently selected: {', '.join(selected) if selected else 'None'}")
        print("Commands: number to toggle, 'a' to add custom, 'd' to done, 'c' to clear all")
        
        while True:
            choice = input("Choice: ").strip().lower()
            
            if choice == 'd':
                return selected
            elif choice == 'c':
                selected = []
                print("Cleared all selections")
            elif choice == 'a':
                custom = input("Enter custom option: ").strip()
                if custom and custom not in selected:
                    selected.append(custom)
                    print(f"Added: {custom}")
            else:
                try:
                    index = int(choice) - 1
                    if 0 <= index < len(options):
                        option = options[index]
                        if option in selected:
                            selected.remove(option)
                            print(f"Removed: {option}")
                        else:
                            selected.append(option)
                            print(f"Added: {option}")
                    else:
                        print(f"Please enter a number between 1 and {len(options)}")
                except ValueError:
                    print("Invalid input. Use number, 'a', 'd', or 'c'")
    
    def add_post(self):
        """Create a new blog post."""
        print("\n" + "="*50)
        print("CREATE NEW BLOG POST")
        print("="*50)
        
        # Get title
        title = input("Post title: ").strip()
        if not title:
            print("Title is required!")
            return
        
        # Generate slug and filename
        slug = self.slugify(title)
        date_str = datetime.now().strftime("%Y-%m-%d")
        filename = f"{date_str}-{slug}.md"
        
        # Check if file exists
        post_path = self.posts_dir / filename
        if post_path.exists():
            overwrite = input(f"File {filename} exists. Overwrite? (y/n): ").strip().lower()
            if overwrite != 'y':
                return
        
        # Get date/time
        date_input = input(f"Date/time (press enter for now: {datetime.now().strftime('%Y-%m-%d %H:%M:%S +0530')}): ").strip()
        if date_input:
            try:
                # Try to parse the input date
                date_obj = datetime.strptime(date_input, "%Y-%m-%d %H:%M:%S")
                date_str = date_obj.strftime("%Y-%m-%d")
                # Update filename with new date
                filename = f"{date_str}-{slug}.md"
                post_path = self.posts_dir / filename
            except ValueError:
                print("Invalid date format. Using current time.")
                date_input = datetime.now().strftime("%Y-%m-%d %H:%M:%S +0530")
        else:
            date_input = datetime.now().strftime("%Y-%m-%d %H:%M:%S +0530")
        
        # Get categories
        existing_categories = self.get_existing_categories()
        all_categories = sorted(list(set(self.common_categories + existing_categories)))
        categories = self.input_multiselect("Select categories:", all_categories)
        
        # Get excerpt
        excerpt = input("\nPost excerpt/description: ").strip()
        
        # Get content
        print("\nContent options:")
        print("1. Write inline")
        print("2. Open in editor")
        content_choice = input("Choice (1 or 2): ").strip()
        
        if content_choice == "2":
            # Create temporary file and open in editor
            temp_file = Path("temp_post_content.md")
            temp_file.write_text("Write your blog post content here...\n\n")
            
            # Try to open in default editor
            try:
                if sys.platform == "win32":
                    os.startfile(temp_file)
                elif sys.platform == "darwin":
                    subprocess.run(["open", temp_file])
                else:
                    subprocess.run(["xdg-open", temp_file])
                
                input("Press Enter when you're done editing...")
                content = temp_file.read_text(encoding='utf-8')
                temp_file.unlink()
            except Exception:
                print("Could not open editor. Using inline input.")
                content_choice = "1"
        
        if content_choice == "1":
            print("\nEnter content (press Ctrl+D or Ctrl+Z to finish):")
            content_lines = []
            try:
                while True:
                    line = input()
                    content_lines.append(line)
            except EOFError:
                content = '\n'.join(content_lines)
        
        # Calculate reading time
        auto_reading_time = self.calculate_reading_time(content)
        reading_time_input = input(f"\nReading time (press enter for auto-calculated {auto_reading_time} min): ").strip()
        reading_time = int(reading_time_input) if reading_time_input.isdigit() else auto_reading_time
        
        # Hero image handling
        hero_image_data = {}
        if PIL_AVAILABLE:
            print("\n" + "="*50)
            print("HERO IMAGE (Optional)")
            print("="*50)
            print("You can add a hero image that will:")
            print("- Display as a hero banner at the top of your post")
            print("- Show as a thumbnail in the blog index")
            print("- Be optimized for both mobile and desktop viewing")
            
            add_hero = input("\nAdd hero image? (y/n): ").strip().lower()
            if add_hero == 'y':
                print("\nHero image options:")
                print("1. File path (existing image)")
                print("2. URL (will be downloaded)")
                print("3. Skip for now")
                
                hero_choice = input("Choice (1, 2, or 3): ").strip()
                year = date_str[:4]  # Extract year from date
                
                if hero_choice == "1":
                    hero_path = input("Enter image file path: ").strip()
                    if hero_path and Path(hero_path).exists():
                        # Copy to posts directory
                        year_dir = self.posts_images_dir / year
                        year_dir.mkdir(exist_ok=True)
                        
                        image_name = f"{slug}-hero{Path(hero_path).suffix}"
                        dest_path = year_dir / image_name
                        shutil.copy2(hero_path, dest_path)
                        
                        # Process hero image
                        image_data = self.process_post_images(slug, year, str(dest_path))
                        if image_data:
                            hero_image_data.update(image_data)
                            
                            # Add alt text
                            alt_text = input("Alt text for accessibility: ").strip()
                            if alt_text:
                                hero_image_data['hero_alt'] = alt_text
                
                elif hero_choice == "2":
                    print("URL download not implemented yet. You can add the image manually later.")
        else:
            print("\nNote: Install Pillow for hero image processing: pip install Pillow")
        
        # Validate post data and fix common issues
        categories, validation_issues = self.validate_post_data(title, categories, excerpt, date_input)
        
        # Show validation issues if any
        if validation_issues:
            print("\nValidation warnings:")
            for issue in validation_issues:
                print(f"  - {issue}")
            
            proceed = input("\nProceed anyway? (y/n): ").strip().lower()
            if proceed != 'y':
                print("Post creation cancelled.")
                return
        
        # Create frontmatter data
        frontmatter_data = {
            'layout': 'post',
            'title': title,
            'date': date_input,
            'categories': categories,
            'excerpt': excerpt,
            'reading_time': reading_time
        }
        
        # Add hero image data if present
        frontmatter_data.update(hero_image_data)
        
        # Write post file with proper formatting
        with open(post_path, 'w', encoding='utf-8') as f:
            f.write(self.create_frontmatter(frontmatter_data))
            f.write('\n\n')
            f.write(content)
        
        # Create category pages for any new categories
        self.ensure_category_pages(categories)
        
        print(f"\n✓ Post created: {filename}")
        print(f"✓ Format: Matches existing Jekyll post structure")
        print(f"✓ Categories: {', '.join(categories)}")
        print(f"✓ Category pages: Ensured to exist")
    
    def ensure_category_pages(self, categories):
        """Ensure category pages exist for all specified categories."""
        blog_categories_dir = Path("blog/categories")
        blog_categories_dir.mkdir(parents=True, exist_ok=True)
        
        category_descriptions = {
            "ai": "Exploring artificial intelligence, machine learning, and the intersection of technology and humanity.",
            "philosophy": "Thoughts on existence, meaning, creativity, and the human condition.",
            "personal": "Personal reflections, experiences, and thoughts on life and learning.",
            "literature": "Book reviews, literary analysis, and reflections on great works of literature.",
            "murakami": "Explorations of Haruki Murakami's works, characters, and themes.",
            "research": "Academic research, scientific discoveries, and scholarly pursuits.",
            "technical": "Programming, software development, and technical projects.",
            "music": "Musical compositions, analysis, and the intersection of sound and emotion.",
            "physics": "Quantum mechanics, physics research, and the fundamental nature of reality.",
            "creativity": "Artistic expression, creative processes, and the nature of inspiration.",
            "poetry": "Poetic works, literary analysis, and the craft of verse.",
            "mathematics": "Mathematical concepts, proofs, and the beauty of abstract reasoning.",
            "programming": "Code, algorithms, and software engineering insights."
        }
        
        for category in categories:
            category_file = blog_categories_dir / f"{category.lower()}.html"
            
            if not category_file.exists():
                # Create the category page
                category_content = f"""---
layout: category
title: {category.capitalize()}
category: {category.lower()}
description: "{category_descriptions.get(category.lower(), f'Posts about {category.lower()}.')}"
---"""
                
                with open(category_file, 'w', encoding='utf-8') as f:
                    f.write(category_content)
                print(f"✓ Created category page: {category_file}")
    
    def edit_post(self):
        """Edit an existing blog post."""
        posts = self.list_posts()
        if not posts:
            return
        
        selected_post = self.select_post(posts)
        if not selected_post:
            return
        
        # Create backup
        backup_path = self.create_backup(selected_post['path'])
        print(f"Backup created: {backup_path}")
        
        while True:
            print(f"\n" + "="*50)
            print(f"EDITING: {selected_post['frontmatter'].get('title', 'No Title')}")
            print("="*50)
            print("1. Edit title")
            print("2. Edit date")
            print("3. Edit categories")
            print("4. Edit excerpt")
            print("5. Edit reading time")
            print("6. Edit content")
            print("7. Edit hero image")
            print("8. Preview post")
            print("9. Save and exit")
            print("0. Exit without saving")
            
            choice = input("\nSelect option: ").strip()
            
            if choice == "1":
                current_title = selected_post['frontmatter'].get('title', '')
                new_title = input(f"Current title: {current_title}\nNew title: ").strip()
                if new_title:
                    selected_post['frontmatter']['title'] = new_title
                    # Update filename if title changed
                    old_path = selected_post['path']
                    new_slug = self.slugify(new_title)
                    date_part = old_path.name[:10]  # Keep the date part
                    new_filename = f"{date_part}-{new_slug}.md"
                    new_path = self.posts_dir / new_filename
                    selected_post['path'] = new_path
                    print(f"Title updated. File will be renamed to: {new_filename}")
            
            elif choice == "2":
                current_date = selected_post['frontmatter'].get('date', '')
                new_date = input(f"Current date: {current_date}\nNew date: ").strip()
                if new_date:
                    selected_post['frontmatter']['date'] = new_date
                    print("Date updated")
            
            elif choice == "3":
                existing_categories = self.get_existing_categories()
                all_categories = sorted(list(set(self.common_categories + existing_categories)))
                current = selected_post['frontmatter'].get('categories', [])
                new_categories = self.input_multiselect("Edit categories:", all_categories, current)
                selected_post['frontmatter']['categories'] = new_categories
                print("Categories updated")
            
            elif choice == "4":
                current_excerpt = selected_post['frontmatter'].get('excerpt', '')
                new_excerpt = input(f"Current excerpt: {current_excerpt}\nNew excerpt: ").strip()
                if new_excerpt:
                    selected_post['frontmatter']['excerpt'] = new_excerpt
                    print("Excerpt updated")
            
            elif choice == "5":
                current_time = selected_post['frontmatter'].get('reading_time', '')
                auto_time = self.calculate_reading_time(selected_post['content'])
                new_time = input(f"Current: {current_time} min, Auto-calculated: {auto_time} min\nNew reading time: ").strip()
                if new_time.isdigit():
                    selected_post['frontmatter']['reading_time'] = int(new_time)
                    print("Reading time updated")
            
            elif choice == "6":
                print("Content editing options:")
                print("1. Edit inline")
                print("2. Open in editor")
                edit_choice = input("Choice: ").strip()
                
                if edit_choice == "2":
                    temp_file = Path("temp_edit_content.md")
                    temp_file.write_text(selected_post['content'], encoding='utf-8')
                    
                    try:
                        if sys.platform == "win32":
                            os.startfile(temp_file)
                        elif sys.platform == "darwin":
                            subprocess.run(["open", temp_file])
                        else:
                            subprocess.run(["xdg-open", temp_file])
                        
                        input("Press Enter when done editing...")
                        selected_post['content'] = temp_file.read_text(encoding='utf-8')
                        temp_file.unlink()
                        print("Content updated")
                    except Exception:
                        print("Could not open editor")
                
                else:
                    print("Current content:")
                    print("-" * 50)
                    print(selected_post['content'][:500] + "..." if len(selected_post['content']) > 500 else selected_post['content'])
                    print("-" * 50)
                    print("Enter new content (Ctrl+D/Ctrl+Z to finish):")
                    content_lines = []
                    try:
                        while True:
                            line = input()
                            content_lines.append(line)
                    except EOFError:
                        selected_post['content'] = '\n'.join(content_lines)
                        print("Content updated")
            
            elif choice == "7":
                # Edit hero image
                if PIL_AVAILABLE:
                    print("\n" + "="*50)
                    print("HERO IMAGE MANAGEMENT")
                    print("="*50)
                    current_hero = selected_post['frontmatter'].get('hero_image', 'None')
                    current_alt = selected_post['frontmatter'].get('hero_alt', 'None')
                    print(f"Current hero image: {current_hero}")
                    print(f"Current alt text: {current_alt}")
                    
                    print("\nOptions:")
                    print("1. Add/Replace hero image")
                    print("2. Edit alt text only")
                    print("3. Remove hero image")
                    print("4. Back to main menu")
                    
                    hero_choice = input("Choice: ").strip()
                    
                    if hero_choice == "1":
                        hero_path = input("Enter image file path: ").strip()
                        if hero_path and Path(hero_path).exists():
                            # Extract post slug and year
                            title = selected_post['frontmatter'].get('title', '')
                            slug = self.slugify(title)
                            date_str = str(selected_post['frontmatter'].get('date', ''))[:10]
                            year = date_str[:4]
                            
                            # Copy to posts directory
                            year_dir = self.posts_images_dir / year
                            year_dir.mkdir(exist_ok=True)
                            
                            image_name = f"{slug}-hero{Path(hero_path).suffix}"
                            dest_path = year_dir / image_name
                            shutil.copy2(hero_path, dest_path)
                            
                            # Process hero image
                            image_data = self.process_post_images(slug, year, str(dest_path))
                            if image_data:
                                selected_post['frontmatter'].update(image_data)
                                
                                # Add alt text
                                alt_text = input("Alt text for accessibility: ").strip()
                                if alt_text:
                                    selected_post['frontmatter']['hero_alt'] = alt_text
                                
                                print("✓ Hero image added and processed")
                        else:
                            print("File not found or invalid path")
                    
                    elif hero_choice == "2":
                        new_alt = input("New alt text: ").strip()
                        if new_alt:
                            selected_post['frontmatter']['hero_alt'] = new_alt
                            print("Alt text updated")
                    
                    elif hero_choice == "3":
                        # Remove hero image fields
                        for key in ['hero_image', 'hero_alt']:
                            selected_post['frontmatter'].pop(key, None)
                        print("Hero image removed")
                else:
                    print("PIL/Pillow not available. Install with: pip install Pillow")
            
            elif choice == "8":
                print("\n" + "="*50)
                print("POST PREVIEW")
                print("="*50)
                print(f"Title: {selected_post['frontmatter'].get('title')}")
                print(f"Date: {selected_post['frontmatter'].get('date')}")
                print(f"Categories: {', '.join(selected_post['frontmatter'].get('categories', []))}")
                print(f"Excerpt: {selected_post['frontmatter'].get('excerpt')}")
                print(f"Reading time: {selected_post['frontmatter'].get('reading_time')} min")
                print(f"Hero image: {selected_post['frontmatter'].get('hero_image', 'None')}")
                print("\nContent:")
                print("-" * 50)
                preview = selected_post['content'][:1000]
                print(preview + "..." if len(selected_post['content']) > 1000 else preview)
                print("-" * 50)
            
            elif choice == "9":
                # Save the post
                old_path = Path(selected_post['filename']).parent / selected_post['filename']
                if old_path.exists() and old_path != selected_post['path']:
                    old_path.unlink()  # Remove old file if renamed
                
                # Use proper frontmatter formatting
                with open(selected_post['path'], 'w', encoding='utf-8') as f:
                    f.write(self.create_frontmatter(selected_post['frontmatter']))
                    f.write('\n\n')
                    f.write(selected_post['content'])
                
                print(f"✓ Post saved: {selected_post['path'].name}")
                print(f"✓ Format: Updated to match Jekyll standards")
                break
            
            elif choice == "0":
                print("Exiting without saving")
                break
            
            else:
                print("Invalid choice")
    
    def remove_post(self):
        """Remove a blog post."""
        posts = self.list_posts()
        if not posts:
            return
        
        selected_post = self.select_post(posts)
        if not selected_post:
            return
        
        print(f"\nYou are about to delete:")
        print(f"Title: {selected_post['frontmatter'].get('title')}")
        print(f"File: {selected_post['filename']}")
        
        confirm = input("\nAre you sure? Type 'DELETE' to confirm: ").strip()
        if confirm == "DELETE":
            # Create backup before deletion
            backup_path = self.create_backup(selected_post['path'])
            print(f"Backup created: {backup_path}")
            
            # Remove the file
            selected_post['path'].unlink()
            print(f"✓ Post deleted: {selected_post['filename']}")
        else:
            print("Deletion cancelled")
    
    def validate_all_posts(self):
        """Validate all blog posts for formatting and consistency."""
        print("\n" + "="*60)
        print("BLOG VALIDATION REPORT")
        print("="*60)
        
        posts = []
        for post_file in self.posts_dir.glob("*.md"):
            post_data = self.parse_post(post_file)
            if post_data:
                posts.append(post_data)
        
        if not posts:
            print("No blog posts found.")
            return
        
        issues_found = 0
        
        for post in posts:
            post_issues = []
            frontmatter = post['frontmatter']
            
            # Check required fields
            required_fields = ['layout', 'title', 'date', 'categories', 'excerpt']
            for field in required_fields:
                if field not in frontmatter:
                    post_issues.append(f"Missing required field: {field}")
            
            # Check field types
            if 'categories' in frontmatter and not isinstance(frontmatter['categories'], list):
                post_issues.append("Categories should be a list")
            
            # Check for common typos
            if 'categories' in frontmatter:
                for cat in frontmatter['categories']:
                    if cat == "philosphy":
                        post_issues.append("Typo in category: 'philosphy' should be 'philosophy'")
            
            # Check date format
            try:
                if 'date' in frontmatter:
                    date_str = str(frontmatter['date'])
                    post_date = datetime.strptime(date_str.split()[0], "%Y-%m-%d")
                    if post_date.date() > datetime.now().date():
                        post_issues.append(f"Future date: {post_date.date()}")
            except:
                post_issues.append("Invalid date format")
            
            # Report issues for this post
            if post_issues:
                issues_found += len(post_issues)
                print(f"\n📄 {post['filename']}")
                for issue in post_issues:
                    print(f"  ❌ {issue}")
            else:
                print(f"✅ {post['filename']}")
        
        print(f"\n" + "="*60)
        if issues_found == 0:
            print("🎉 All posts are properly formatted!")
        else:
            print(f"⚠️  Found {issues_found} issues across {len([p for p in posts if any([True for issue in []])])} posts")
            print("Use 'python blog_manager.py edit' to fix issues")
        print("="*60)

    def preview_post(self):
        """Preview a blog post."""
        posts = self.list_posts()
        if not posts:
            return
        
        selected_post = self.select_post(posts)
        if not selected_post:
            return
        
        print("\n" + "="*80)
        print("POST PREVIEW")
        print("="*80)
        print(f"File: {selected_post['filename']}")
        print(f"Title: {selected_post['frontmatter'].get('title')}")
        print(f"Date: {selected_post['frontmatter'].get('date')}")
        print(f"Categories: {', '.join(selected_post['frontmatter'].get('categories', []))}")
        print(f"Tags: {', '.join(selected_post['frontmatter'].get('tags', []))}")
        print(f"Excerpt: {selected_post['frontmatter'].get('excerpt')}")
        print(f"Reading time: {selected_post['frontmatter'].get('reading_time')} min")
        print("\nContent:")
        print("-" * 80)
        print(selected_post['content'])
        print("-" * 80)

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    command = sys.argv[1].lower()
    blog_manager = BlogManager()
    
    if command == "add":
        blog_manager.add_post()
    elif command == "list":
        blog_manager.list_posts()
    elif command == "edit":
        blog_manager.edit_post()
    elif command == "remove":
        blog_manager.remove_post()
    elif command == "preview":
        blog_manager.preview_post()
    elif command == "validate":
        blog_manager.validate_all_posts()
    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)

if __name__ == "__main__":
    main()