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

class BlogManager:
    def __init__(self):
        self.posts_dir = Path("_posts")
        self.backup_dir = Path(".backups")
        self.backup_dir.mkdir(exist_ok=True)
        
        # Ensure posts directory exists
        self.posts_dir.mkdir(exist_ok=True)
        
        # Common categories and tags for suggestions
        self.common_categories = ["research", "personal", "technical", "music", "physics", "ai"]
        self.common_tags = ["quantum computing", "machine learning", "physics", "ai", "music", 
                           "poetry", "mathematics", "programming", "research", "philosophy"]
    
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
    
    def get_existing_tags(self) -> List[str]:
        """Extract all existing tags from posts."""
        tags = set()
        for post_file in self.posts_dir.glob("*.md"):
            try:
                with open(post_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if content.startswith('---'):
                        yaml_end = content.find('---', 3)
                        if yaml_end != -1:
                            frontmatter = yaml.safe_load(content[3:yaml_end])
                            if 'tags' in frontmatter:
                                tags.update(frontmatter['tags'])
            except Exception:
                continue
        return sorted(list(tags))
    
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
        
        # Get tags
        existing_tags = self.get_existing_tags()
        all_tags = sorted(list(set(self.common_tags + existing_tags)))
        tags = self.input_multiselect("Select tags:", all_tags)
        
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
        
        # Create frontmatter
        frontmatter = {
            'layout': 'post',
            'title': title,
            'date': date_input,
            'categories': categories,
            'tags': tags,
            'excerpt': excerpt,
            'reading_time': reading_time
        }
        
        # Write post file
        with open(post_path, 'w', encoding='utf-8') as f:
            f.write('---\n')
            yaml.dump(frontmatter, f, default_flow_style=False, allow_unicode=True)
            f.write('---\n\n')
            f.write(content)
        
        print(f"\n✓ Post created: {filename}")
    
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
            print("4. Edit tags")
            print("5. Edit excerpt")
            print("6. Edit reading time")
            print("7. Edit content")
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
                existing_tags = self.get_existing_tags()
                all_tags = sorted(list(set(self.common_tags + existing_tags)))
                current = selected_post['frontmatter'].get('tags', [])
                new_tags = self.input_multiselect("Edit tags:", all_tags, current)
                selected_post['frontmatter']['tags'] = new_tags
                print("Tags updated")
            
            elif choice == "5":
                current_excerpt = selected_post['frontmatter'].get('excerpt', '')
                new_excerpt = input(f"Current excerpt: {current_excerpt}\nNew excerpt: ").strip()
                if new_excerpt:
                    selected_post['frontmatter']['excerpt'] = new_excerpt
                    print("Excerpt updated")
            
            elif choice == "6":
                current_time = selected_post['frontmatter'].get('reading_time', '')
                auto_time = self.calculate_reading_time(selected_post['content'])
                new_time = input(f"Current: {current_time} min, Auto-calculated: {auto_time} min\nNew reading time: ").strip()
                if new_time.isdigit():
                    selected_post['frontmatter']['reading_time'] = int(new_time)
                    print("Reading time updated")
            
            elif choice == "7":
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
            
            elif choice == "8":
                print("\n" + "="*50)
                print("POST PREVIEW")
                print("="*50)
                print(f"Title: {selected_post['frontmatter'].get('title')}")
                print(f"Date: {selected_post['frontmatter'].get('date')}")
                print(f"Categories: {', '.join(selected_post['frontmatter'].get('categories', []))}")
                print(f"Tags: {', '.join(selected_post['frontmatter'].get('tags', []))}")
                print(f"Excerpt: {selected_post['frontmatter'].get('excerpt')}")
                print(f"Reading time: {selected_post['frontmatter'].get('reading_time')} min")
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
                
                with open(selected_post['path'], 'w', encoding='utf-8') as f:
                    f.write('---\n')
                    yaml.dump(selected_post['frontmatter'], f, default_flow_style=False, allow_unicode=True)
                    f.write('---\n\n')
                    f.write(selected_post['content'])
                
                print(f"✓ Post saved: {selected_post['path'].name}")
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
    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)

if __name__ == "__main__":
    main()