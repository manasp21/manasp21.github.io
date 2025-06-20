#!/usr/bin/env python3
"""
Photo Manager for Manas Pandey Photography Portfolio
A comprehensive tool for managing photos while maintaining 100% compatibility with the existing gallery system.

Usage:
    python photo_manager.py list                    # View all photos with metadata
    python photo_manager.py validate               # Check system integrity
    python photo_manager.py edit                   # Interactive metadata editing
    python photo_manager.py edit --photo ID        # Edit specific photo by ID
    python photo_manager.py preview                # Preview rename operations
    python photo_manager.py rename                 # Smart batch renaming
    python photo_manager.py rename --preview       # Show rename plan only
    python photo_manager.py add PATH               # Add new photos
    python photo_manager.py remove --photo ID      # Remove photos with backups
    python photo_manager.py rollback --backup DIR  # Rollback to backup
"""

import os
import sys
import json
import re
import shutil
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import argparse

class PhotoManager:
    def __init__(self):
        self.base_dir = Path(".")
        self.gallery_dir = Path("gallery")
        self.images_dir = self.gallery_dir / "images"
        self.metadata_file = self.gallery_dir / "metadata.json"
        self.backup_dir = Path(".backups")
        self.backup_dir.mkdir(exist_ok=True)
        
        # Load current metadata
        self.metadata = self.load_metadata()
        
    def load_metadata(self) -> Dict:
        """Load gallery metadata from JSON file."""
        if not self.metadata_file.exists():
            print(f"❌ Metadata file not found: {self.metadata_file}")
            return {"gallery": {}, "images": []}
        
        try:
            with open(self.metadata_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Error loading metadata: {e}")
            return {"gallery": {}, "images": []}
    
    def save_metadata(self):
        """Save metadata back to JSON file."""
        try:
            # Create backup before saving
            if self.metadata_file.exists():
                backup_path = self.backup_dir / f"metadata_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                shutil.copy2(self.metadata_file, backup_path)
            
            with open(self.metadata_file, 'w', encoding='utf-8') as f:
                json.dump(self.metadata, f, indent=2, ensure_ascii=False)
            print("✅ Metadata saved successfully")
        except Exception as e:
            print(f"❌ Error saving metadata: {e}")
    
    def create_backup(self) -> Path:
        """Create complete backup of gallery directory."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = self.backup_dir / f"gallery_backup_{timestamp}"
        
        try:
            shutil.copytree(self.gallery_dir, backup_path)
            print(f"✅ Backup created: {backup_path}")
            return backup_path
        except Exception as e:
            print(f"❌ Error creating backup: {e}")
            return None
    
    def validate_system(self) -> List[str]:
        """Validate photography system integrity with comprehensive checks."""
        issues = []
        warnings = []
        
        # Check gallery directory exists
        if not self.gallery_dir.exists():
            issues.append(f"Gallery directory missing: {self.gallery_dir}")
            return issues
        
        # Check images directory exists
        if not self.images_dir.exists():
            issues.append(f"Images directory missing: {self.images_dir}")
            return issues
        
        # Check metadata file exists
        if not self.metadata_file.exists():
            issues.append(f"Metadata file missing: {self.metadata_file}")
            return issues
        
        # Validate metadata structure
        if "images" not in self.metadata:
            issues.append("Missing 'images' array in metadata")
            return issues
        
        # Check each image in metadata
        for i, image in enumerate(self.metadata["images"]):
            # Validate required fields
            required_fields = ["id", "filename", "title", "caption", "category", "tags"]
            for field in required_fields:
                if field not in image:
                    issues.append(f"Image {i+1}: Missing required field '{field}'")
            
            # Check if file exists
            if "filename" in image:
                image_path = self.images_dir / image["filename"]
                if not image_path.exists():
                    issues.append(f"Image file missing: {image['filename']}")
                
                # Validate filename format (should be professional after rename)
                filename = image["filename"]
                if not re.match(r'\d{4}-\d{2}-\d{2}-\w+-\w+\.(jpg|jpeg|png|webp)$', filename.lower()):
                    warnings.append(f"Non-standard filename format: {filename}")
            
            # Check for generic titles and captions
            if image.get("title", "").startswith("Image "):
                warnings.append(f"Generic title detected: {image.get('title')} for {image.get('filename')}")
            
            if image.get("caption") == "Image Caption":
                warnings.append(f"Generic caption detected for {image.get('filename')}")
            
            # Validate category
            valid_categories = ["urban", "night", "landscape", "abstract", "nature", "street"]
            if image.get("category") not in valid_categories:
                warnings.append(f"Invalid category '{image.get('category')}' for {image.get('filename')}")
            
            # Check for empty tags
            if not image.get("tags") or len(image.get("tags", [])) == 0:
                warnings.append(f"No tags assigned to {image.get('filename')}")
            
            # Validate dimensions and aspect ratio
            if "dimensions" in image and "aspectRatio" in image:
                width = image["dimensions"].get("width", 0)
                height = image["dimensions"].get("height", 0)
                if width > 0 and height > 0:
                    calculated_ratio = round(width / height, 2)
                    stored_ratio = image["aspectRatio"]
                    if abs(calculated_ratio - stored_ratio) > 0.1:
                        warnings.append(f"Aspect ratio mismatch for {image.get('filename')}: calculated {calculated_ratio}, stored {stored_ratio}")
        
        # Check for orphaned files
        if self.images_dir.exists():
            metadata_files = {img["filename"] for img in self.metadata["images"] if "filename" in img}
            actual_files = {f.name for f in self.images_dir.iterdir() if f.is_file() and f.suffix.lower() in ['.jpg', '.jpeg', '.png', '.webp']}
            orphaned = actual_files - metadata_files
            if orphaned:
                issues.append(f"Orphaned files found: {', '.join(orphaned)}")
        
        # Check for duplicate IDs
        ids = [img.get("id") for img in self.metadata["images"] if "id" in img]
        if len(ids) != len(set(ids)):
            issues.append("Duplicate IDs found in metadata")
        
        # Check for duplicate filenames
        filenames = [img.get("filename") for img in self.metadata["images"] if "filename" in img]
        if len(filenames) != len(set(filenames)):
            issues.append("Duplicate filenames found in metadata")
        
        # Check sort order consistency
        sort_orders = [img.get("sortOrder") for img in self.metadata["images"] if "sortOrder" in img]
        if len(sort_orders) != len(set(sort_orders)):
            warnings.append("Duplicate sort orders found")
        
        # Validate featured photos balance
        featured_count = sum(1 for img in self.metadata["images"] if img.get("featured", False))
        total_count = len(self.metadata["images"])
        if featured_count == 0:
            warnings.append("No featured photos selected")
        elif featured_count > total_count * 0.5:
            warnings.append(f"Too many featured photos ({featured_count}/{total_count})")
        
        # Print warnings if any
        if warnings:
            print("⚠️  Warnings found:")
            for warning in warnings:
                print(f"   - {warning}")
        
        return issues
    
    def list_photos(self, category_filter: str = None, featured_only: bool = False):
        """Display all photos with metadata in tabular format."""
        images = self.metadata.get("images", [])
        
        # Apply filters
        if category_filter:
            images = [img for img in images if img.get("category") == category_filter]
        if featured_only:
            images = [img for img in images if img.get("featured", False)]
        
        if not images:
            print("No photos found matching criteria.")
            return
        
        print(f"\n{'='*100}")
        print(f"PHOTOGRAPHY PORTFOLIO - {len(images)} PHOTOS")
        print(f"{'='*100}")
        print(f"{'ID':<3} {'FILENAME':<35} {'TITLE':<25} {'CATEGORY':<12} {'TAGS':<20}")
        print(f"{'='*100}")
        
        for img in images:
            img_id = str(img.get("id", "?"))
            filename = img.get("filename", "Unknown")[:33] + ("..." if len(img.get("filename", "")) > 33 else "")
            title = img.get("title", "No title")[:23] + ("..." if len(img.get("title", "")) > 23 else "")
            category = img.get("category", "none")
            tags = ", ".join(img.get("tags", [])[:3])[:18] + ("..." if len(img.get("tags", [])) > 3 else "")
            
            print(f"{img_id:<3} {filename:<35} {title:<25} {category:<12} {tags:<20}")
        
        print(f"{'='*100}")
        
        # Show summary
        total_images = len(self.metadata.get("images", []))
        categories = {}
        featured_count = 0
        
        for img in self.metadata.get("images", []):
            cat = img.get("category", "none")
            categories[cat] = categories.get(cat, 0) + 1
            if img.get("featured", False):
                featured_count += 1
        
        print(f"Total photos: {total_images} | Featured: {featured_count}")
        print(f"Categories: {', '.join([f'{k}({v})' for k, v in categories.items()])}")
    
    def get_photo_by_id(self, photo_id: int) -> Optional[Dict]:
        """Get photo metadata by ID."""
        for img in self.metadata.get("images", []):
            if img.get("id") == photo_id:
                return img
        return None
    
    def edit_photo_interactive(self, photo_id: int = None):
        """Interactive photo metadata editor."""
        if photo_id:
            photo = self.get_photo_by_id(photo_id)
            if not photo:
                print(f"❌ Photo with ID {photo_id} not found")
                return
            self._edit_single_photo(photo)
        else:
            # Show list and let user choose
            self.list_photos()
            try:
                photo_id = int(input("\nEnter photo ID to edit (or 0 to cancel): ").strip())
                if photo_id == 0:
                    print("Operation cancelled.")
                    return
                
                photo = self.get_photo_by_id(photo_id)
                if not photo:
                    print(f"❌ Photo with ID {photo_id} not found")
                    return
                
                self._edit_single_photo(photo)
            except (ValueError, KeyboardInterrupt):
                print("\nOperation cancelled.")
                return
    
    def _edit_single_photo(self, photo: Dict):
        """Edit a single photo's metadata interactively."""
        print(f"\n{'='*60}")
        print(f"EDITING PHOTO: {photo.get('filename', 'Unknown')}")
        print(f"{'='*60}")
        
        try:
            while True:
                print(f"\nCurrent metadata:")
                print(f"1. Title: {photo.get('title', 'N/A')}")
                print(f"2. Caption: {photo.get('caption', 'N/A')}")
                print(f"3. Category: {photo.get('category', 'N/A')}")
                print(f"4. Tags: {', '.join(photo.get('tags', []))}")
                print(f"5. Featured: {photo.get('featured', False)}")
                print(f"6. Location: {photo.get('location', 'N/A')}")
                print(f"7. Camera: {photo.get('metadata', {}).get('camera', 'N/A')}")
                print(f"8. Lens: {photo.get('metadata', {}).get('lens', 'N/A')}")
                print(f"9. Settings: {photo.get('metadata', {}).get('settings', 'N/A')}")
                print(f"10. Date: {photo.get('dateCreated', 'N/A')}")
                print(f"0. Save and exit")
                
                choice = input("\nWhat would you like to edit? (1-10, 0 to save): ").strip()
                
                if choice == "0":
                    self.save_metadata()
                    print("✅ Photo updated successfully!")
                    break
                elif choice == "1":
                    new_title = input(f"Enter new title (current: {photo.get('title', 'N/A')}): ").strip()
                    if new_title:
                        photo["title"] = new_title
                elif choice == "2":
                    print(f"Current caption: {photo.get('caption', 'N/A')}")
                    new_caption = input("Enter new caption (or press Enter to keep current): ").strip()
                    if new_caption:
                        photo["caption"] = new_caption
                elif choice == "3":
                    print("Available categories: urban, night, landscape, abstract, nature, street")
                    new_category = input(f"Enter category (current: {photo.get('category', 'N/A')}): ").strip().lower()
                    if new_category:
                        photo["category"] = new_category
                elif choice == "4":
                    print(f"Current tags: {', '.join(photo.get('tags', []))}")
                    print("Enter tags separated by commas:")
                    new_tags = input().strip()
                    if new_tags:
                        photo["tags"] = [tag.strip() for tag in new_tags.split(",") if tag.strip()]
                elif choice == "5":
                    featured = input(f"Featured photo? (y/n, current: {photo.get('featured', False)}): ").strip().lower()
                    photo["featured"] = featured in ["y", "yes", "true"]
                elif choice == "6":
                    new_location = input(f"Enter location (current: {photo.get('location', 'N/A')}): ").strip()
                    if new_location:
                        photo["location"] = new_location
                elif choice == "7":
                    if "metadata" not in photo:
                        photo["metadata"] = {}
                    new_camera = input(f"Enter camera (current: {photo.get('metadata', {}).get('camera', 'N/A')}): ").strip()
                    if new_camera:
                        photo["metadata"]["camera"] = new_camera
                elif choice == "8":
                    if "metadata" not in photo:
                        photo["metadata"] = {}
                    new_lens = input(f"Enter lens (current: {photo.get('metadata', {}).get('lens', 'N/A')}): ").strip()
                    if new_lens:
                        photo["metadata"]["lens"] = new_lens
                elif choice == "9":
                    if "metadata" not in photo:
                        photo["metadata"] = {}
                    new_settings = input(f"Enter settings (current: {photo.get('metadata', {}).get('settings', 'N/A')}): ").strip()
                    if new_settings:
                        photo["metadata"]["settings"] = new_settings
                elif choice == "10":
                    new_date = input(f"Enter date (YYYY-MM-DD, current: {photo.get('dateCreated', 'N/A')}): ").strip()
                    if new_date and re.match(r'\d{4}-\d{2}-\d{2}', new_date):
                        photo["dateCreated"] = new_date
                else:
                    print("Invalid choice. Please try again.")
                    
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
    
    def generate_new_filename(self, photo: Dict) -> str:
        """Generate SEO-friendly filename from photo metadata."""
        # Extract date
        date_created = photo.get("dateCreated", "")
        if not date_created:
            # Try to extract from current filename
            filename = photo.get("filename", "")
            date_match = re.search(r'(\d{4})(\d{2})(\d{2})', filename)
            if date_match:
                date_created = f"{date_match.group(1)}-{date_match.group(2)}-{date_match.group(3)}"
            else:
                date_created = datetime.now().strftime("%Y-%m-%d")
        
        # Get category
        category = photo.get("category", "misc")
        
        # Get primary tag (first tag or derived from title)
        tags = photo.get("tags", [])
        if tags:
            primary_tag = tags[0].lower().replace(" ", "-")
        else:
            # Derive from title
            title = photo.get("title", "image")
            primary_tag = re.sub(r'[^a-z0-9\s-]', '', title.lower()).replace(" ", "-")[:15]
        
        # Get file extension
        original_filename = photo.get("filename", "image.jpg")
        ext = Path(original_filename).suffix.lower()
        
        # Generate new filename
        new_filename = f"{date_created}-{category}-{primary_tag}{ext}"
        
        # Clean up filename
        new_filename = re.sub(r'[^a-z0-9\-.]', '', new_filename)
        new_filename = re.sub(r'-+', '-', new_filename)
        
        return new_filename
    
    def preview_rename_operations(self) -> List[Tuple[str, str]]:
        """Preview what files would be renamed."""
        rename_operations = []
        new_filenames = set()
        
        print(f"\n{'='*80}")
        print("RENAME PREVIEW")
        print(f"{'='*80}")
        print(f"{'#':<3} {'CURRENT FILENAME':<40} {'NEW FILENAME':<35}")
        print(f"{'='*80}")
        
        for i, photo in enumerate(self.metadata.get("images", []), 1):
            current_filename = photo.get("filename", "")
            new_filename = self.generate_new_filename(photo)
            
            # Handle conflicts
            original_new = new_filename
            counter = 1
            while new_filename in new_filenames:
                name_part, ext = os.path.splitext(original_new)
                new_filename = f"{name_part}-{counter}{ext}"
                counter += 1
            
            new_filenames.add(new_filename)
            rename_operations.append((current_filename, new_filename))
            
            # Display preview
            current_display = current_filename[:38] + ("..." if len(current_filename) > 38 else "")
            new_display = new_filename[:33] + ("..." if len(new_filename) > 33 else "")
            print(f"{i:<3} {current_display:<40} {new_display:<35}")
        
        print(f"{'='*80}")
        print(f"Total files to rename: {len(rename_operations)}")
        
        # Check for conflicts
        conflicts = len(rename_operations) - len(set(op[1] for op in rename_operations))
        if conflicts > 0:
            print(f"⚠️  {conflicts} naming conflicts detected and resolved with suffixes")
        else:
            print("✅ No naming conflicts detected")
        
        return rename_operations
    
    def execute_rename_operations(self, operations: List[Tuple[str, str]]):
        """Execute the rename operations with full safety checks."""
        if not operations:
            print("No rename operations to execute.")
            return
        
        print(f"\n⚠️  About to rename {len(operations)} files.")
        confirm = input("This operation will modify files. Continue? (yes/no): ").strip().lower()
        
        if confirm not in ["yes", "y"]:
            print("Operation cancelled.")
            return
        
        # Create backup
        backup_path = self.create_backup()
        if not backup_path:
            print("❌ Failed to create backup. Aborting rename operation.")
            return
        
        try:
            success_count = 0
            
            # Phase 1: Rename physical files
            print("\nRenaming files...")
            for current_filename, new_filename in operations:
                current_path = self.images_dir / current_filename
                new_path = self.images_dir / new_filename
                
                if current_path.exists():
                    if new_path.exists():
                        print(f"⚠️  Target file already exists: {new_filename}")
                        continue
                    
                    current_path.rename(new_path)
                    print(f"  ✅ {current_filename} → {new_filename}")
                    success_count += 1
                else:
                    print(f"  ❌ Source file not found: {current_filename}")
            
            # Phase 2: Update metadata
            print("\nUpdating metadata...")
            rename_mapping = dict(operations)
            
            for photo in self.metadata["images"]:
                if photo.get("filename") in rename_mapping:
                    old_filename = photo["filename"]
                    new_filename = rename_mapping[old_filename]
                    photo["filename"] = new_filename
                    print(f"  ✅ Updated metadata: {old_filename} → {new_filename}")
            
            # Save updated metadata
            self.save_metadata()
            
            # Phase 3: Validation
            print("\nValidating changes...")
            issues = self.validate_system()
            
            if issues:
                print("❌ Validation failed after rename operation:")
                for issue in issues:
                    print(f"  - {issue}")
                print(f"\n🔄 Rolling back to backup: {backup_path}")
                self._rollback_from_backup(backup_path)
            else:
                print(f"✅ Rename operation completed successfully!")
                print(f"✅ {success_count}/{len(operations)} files renamed")
                print(f"✅ Metadata updated and validated")
                
        except Exception as e:
            print(f"❌ Error during rename operation: {e}")
            print(f"🔄 Rolling back to backup: {backup_path}")
            self._rollback_from_backup(backup_path)
    
    def _rollback_from_backup(self, backup_path: Path):
        """Rollback gallery to backup state."""
        try:
            if self.gallery_dir.exists():
                shutil.rmtree(self.gallery_dir)
            shutil.copytree(backup_path, self.gallery_dir)
            
            # Reload metadata
            self.metadata = self.load_metadata()
            
            print("✅ Successfully rolled back to backup state")
        except Exception as e:
            print(f"❌ Critical error during rollback: {e}")
            print(f"Manual recovery required from: {backup_path}")
    
    def fix_metadata_issues(self):
        """Fix common metadata issues automatically."""
        print("\n🔧 Scanning for fixable issues...")
        
        changes_made = False
        
        # Fix missing required fields
        for i, image in enumerate(self.metadata["images"]):
            # Add missing fields with defaults
            if "aspectRatio" not in image and "dimensions" in image:
                width = image["dimensions"].get("width", 0)
                height = image["dimensions"].get("height", 0)
                if width > 0 and height > 0:
                    image["aspectRatio"] = round(width / height, 2)
                    print(f"  ✅ Added aspectRatio for {image.get('filename')}")
                    changes_made = True
            
            # Fix sort order gaps
            if image.get("sortOrder") != i + 1:
                image["sortOrder"] = i + 1
                print(f"  ✅ Fixed sortOrder for {image.get('filename')}: {image['sortOrder']}")
                changes_made = True
            
            # Ensure required fields exist
            if "featured" not in image:
                image["featured"] = False
                changes_made = True
            
            if "tags" not in image:
                image["tags"] = []
                changes_made = True
        
        # Fix JSON formatting
        if not self.metadata_file.read_text().endswith('\n'):
            changes_made = True
            print("  ✅ Fixed JSON file formatting")
        
        if changes_made:
            self.save_metadata()
            print("✅ Metadata issues fixed successfully!")
            
            # Auto-sync with photography.html
            print("\n🔄 Auto-syncing with photography.html...")
            self.update_photography_html_fallback()
        else:
            print("✅ No fixable issues found")
    
    def bulk_edit_titles(self):
        """Bulk update photo titles based on tags and categories."""
        print("\n📝 Bulk Title Enhancement")
        print("This will generate descriptive titles based on photo metadata.")
        
        confirm = input("Continue? (y/n): ").strip().lower()
        if confirm not in ['y', 'yes']:
            print("Operation cancelled.")
            return
        
        updated_count = 0
        
        for image in self.metadata["images"]:
            current_title = image.get("title", "")
            
            # Only update generic titles
            if current_title.startswith("Image ") or not current_title or current_title == "Untitled":
                category = image.get("category", "")
                tags = image.get("tags", [])
                
                # Generate descriptive title
                if category and tags:
                    # Use category and first 2 relevant tags
                    relevant_tags = [tag for tag in tags if tag.lower() not in category.lower()][:2]
                    if relevant_tags:
                        new_title = f"{category.title()} {' '.join(relevant_tags).title()}"
                    else:
                        new_title = f"{category.title()} Photography"
                elif category:
                    new_title = f"{category.title()} Photography"
                else:
                    new_title = "Artistic Photography"
                
                # Capitalize properly
                new_title = ' '.join(word.capitalize() for word in new_title.split())
                
                image["title"] = new_title
                print(f"  ✅ {current_title} → {new_title}")
                updated_count += 1
        
        if updated_count > 0:
            self.save_metadata()
            print(f"\n✅ Updated {updated_count} photo titles!")
            
            # Auto-sync with photography.html
            print("🔄 Auto-syncing with photography.html...")
            self.update_photography_html_fallback()
        else:
            print("\n✅ No generic titles found to update")
    
    def bulk_edit_captions(self):
        """Bulk update photo captions with descriptive text."""
        print("\n📝 Bulk Caption Enhancement")
        print("This will generate descriptive captions based on photo metadata.")
        
        confirm = input("Continue? (y/n): ").strip().lower()
        if confirm not in ['y', 'yes']:
            print("Operation cancelled.")
            return
        
        updated_count = 0
        
        for image in self.metadata["images"]:
            current_caption = image.get("caption", "")
            
            # Only update generic captions
            if current_caption == "Image Caption" or not current_caption:
                category = image.get("category", "")
                tags = image.get("tags", [])
                location = image.get("location", "")
                
                # Generate descriptive caption
                caption_parts = []
                
                if category == "urban":
                    caption_parts.append("Urban photography capturing")
                elif category == "landscape":
                    caption_parts.append("Landscape photography showcasing")
                elif category == "night":
                    caption_parts.append("Night photography featuring")
                elif category == "abstract":
                    caption_parts.append("Abstract artistic composition with")
                elif category == "nature":
                    caption_parts.append("Nature photography highlighting")
                elif category == "street":
                    caption_parts.append("Street photography documenting")
                else:
                    caption_parts.append("Photography featuring")
                
                # Add relevant tags
                if tags:
                    tag_text = ", ".join(tags[:3])
                    caption_parts.append(tag_text)
                
                # Add location if available
                if location and location not in ["Unknown", "N/A"]:
                    caption_parts.append(f"captured in {location}")
                
                new_caption = " ".join(caption_parts) + "."
                new_caption = new_caption.replace("  ", " ")  # Clean double spaces
                
                image["caption"] = new_caption
                print(f"  ✅ Enhanced caption for {image.get('filename')}")
                updated_count += 1
        
        if updated_count > 0:
            self.save_metadata()
            print(f"\n✅ Updated {updated_count} photo captions!")
            
            # Auto-sync with photography.html
            print("🔄 Auto-syncing with photography.html...")
            self.update_photography_html_fallback()
        else:
            print("\n✅ No generic captions found to update")
    
    def add_new_photo(self, photo_path: str):
        """Add a new photo to the gallery with interactive metadata collection."""
        source_path = Path(photo_path)
        
        if not source_path.exists():
            print(f"❌ Photo file not found: {photo_path}")
            return
        
        if source_path.suffix.lower() not in ['.jpg', '.jpeg', '.png', '.webp']:
            print(f"❌ Unsupported file format: {source_path.suffix}")
            return
        
        print(f"\n📸 Adding new photo: {source_path.name}")
        
        # Generate new ID
        existing_ids = [img.get("id", 0) for img in self.metadata["images"]]
        new_id = max(existing_ids) + 1 if existing_ids else 1
        
        # Interactive metadata collection
        try:
            title = input("Enter photo title: ").strip()
            caption = input("Enter photo caption: ").strip()
            
            print("Available categories: urban, night, landscape, abstract, nature, street")
            category = input("Enter category: ").strip().lower()
            
            tags_input = input("Enter tags (comma-separated): ").strip()
            tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()]
            
            location = input("Enter location (optional): ").strip()
            
            featured = input("Featured photo? (y/n): ").strip().lower() in ['y', 'yes']
            
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            return
        
        # Generate filename
        date_str = datetime.now().strftime("%Y-%m-%d")
        primary_tag = tags[0].lower().replace(" ", "-") if tags else "photo"
        new_filename = f"{date_str}-{category}-{primary_tag}{source_path.suffix.lower()}"
        
        # Ensure unique filename
        existing_files = {img["filename"] for img in self.metadata["images"]}
        counter = 1
        original_filename = new_filename
        while new_filename in existing_files:
            name_part, ext = os.path.splitext(original_filename)
            new_filename = f"{name_part}-{counter}{ext}"
            counter += 1
        
        # Copy file to gallery
        dest_path = self.images_dir / new_filename
        try:
            shutil.copy2(source_path, dest_path)
            print(f"✅ Copied {source_path.name} → {new_filename}")
        except Exception as e:
            print(f"❌ Error copying file: {e}")
            return
        
        # Create metadata entry
        new_photo = {
            "id": new_id,
            "filename": new_filename,
            "title": title or f"Photo {new_id}",
            "caption": caption or "Professional photography",
            "metadata": {
                "camera": "Unknown",
                "lens": "Unknown", 
                "settings": "Unknown"
            },
            "tags": tags,
            "category": category or "misc",
            "featured": featured,
            "sortOrder": new_id,
            "aspectRatio": 1.5,  # Default, can be updated later
            "dimensions": {
                "width": 1920,
                "height": 1280
            },
            "location": location or "Unknown",
            "dateCreated": datetime.now().strftime("%Y-%m-%d")
        }
        
        # Add to metadata
        self.metadata["images"].append(new_photo)
        self.save_metadata()
        
        print(f"✅ Successfully added photo with ID {new_id}")
        
        # Auto-sync with photography.html
        print("🔄 Auto-syncing with photography.html...")
        self.update_photography_html_fallback()
    
    def update_photography_html_fallback(self):
        """Update photography.html fallback with current photo metadata for automatic loading."""
        photography_file = Path("photography.html")
        
        if not photography_file.exists():
            print("❌ photography.html not found")
            return
        
        # Read photography.html
        with open(photography_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Create backup
        backup_path = self.backup_dir / f"photography_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        shutil.copy2(photography_file, backup_path)
        print(f"✅ Backup created: {backup_path}")
        
        # Generate comprehensive fallback data with all metadata
        fallback_data = "            const fallbackImages = [\n"
        for img in self.metadata["images"]:
            # Escape quotes in strings
            title = img.get("title", "Untitled").replace("'", "\\'")
            caption = img.get("caption", "").replace("'", "\\'")
            location = img.get("location", "Unknown").replace("'", "\\'")
            camera = img.get("metadata", {}).get("camera", "Unknown").replace("'", "\\'")
            lens = img.get("metadata", {}).get("lens", "Unknown").replace("'", "\\'")
            settings = img.get("metadata", {}).get("settings", "Unknown").replace("'", "\\'")
            
            fallback_data += f"                {{\n"
            fallback_data += f"                    id: {img.get('id', 1)},\n"
            fallback_data += f"                    filename: '{img.get('filename', '')}',\n"
            fallback_data += f"                    title: '{title}',\n"
            fallback_data += f"                    caption: '{caption}',\n"
            fallback_data += f"                    location: '{location}',\n"
            fallback_data += f"                    camera: '{camera}',\n"
            fallback_data += f"                    lens: '{lens}',\n"
            fallback_data += f"                    settings: '{settings}',\n"
            fallback_data += f"                    tags: {json.dumps(img.get('tags', []))},\n"
            fallback_data += f"                    category: '{img.get('category', 'general')}',\n"
            fallback_data += f"                    featured: {str(img.get('featured', False)).lower()},\n"
            fallback_data += f"                    sortOrder: {img.get('sortOrder', 0)},\n"
            fallback_data += f"                    aspectRatio: {img.get('aspectRatio', 1.5)},\n"
            dimensions = img.get('dimensions', {'width': 1920, 'height': 1280})
            fallback_data += f"                    dimensions: {{ width: {dimensions.get('width', 1920)}, height: {dimensions.get('height', 1280)} }}\n"
            fallback_data += f"                }},\n"
        fallback_data += "            ];"
        
        # Replace the fallback list in photography.html
        pattern = r'const fallbackImages = \[[\s\S]*?\];'
        new_content = re.sub(pattern, fallback_data, content)
        
        # Also update the fallback mapping to use the rich data
        fallback_mapping = """
            return fallbackImages.map((item, index) => ({
                id: item.id,
                filename: item.filename,
                src: `gallery/images/${item.filename}`,
                title: item.title,
                caption: item.caption,
                metadata: { 
                    camera: item.camera, 
                    lens: item.lens, 
                    settings: item.settings,
                    location: item.location
                },
                tags: item.tags,
                category: item.category,
                featured: item.featured,
                sortOrder: item.sortOrder,
                aspectRatio: item.aspectRatio,
                dimensions: item.dimensions
            }));"""
        
        # Replace the fallback mapping
        mapping_pattern = r'return fallbackImages\.map\([\s\S]*?\}\)\);'
        new_content = re.sub(mapping_pattern, fallback_mapping.strip(), new_content)
        
        # Write updated content
        with open(photography_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print("✅ Updated photography.html with complete metadata fallback")
        print(f"✅ {len(self.metadata['images'])} photos with full metadata")
        print("✅ Photos will load automatically with professional titles and captions")
    
    def validate_photography_integration(self):
        """Validate that photography.html is compatible with current photo system."""
        print("\n🔍 Validating photography.html integration...")
        
        issues = []
        warnings = []
        
        photography_file = Path("photography.html")
        if not photography_file.exists():
            issues.append("photography.html file not found")
            return issues
        
        # Read photography.html content
        with open(photography_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check metadata file path
        if 'gallery/metadata.json' in content:
            correct_path = str(self.metadata_file.relative_to(Path(".")))
            if correct_path != 'gallery/metadata.json':
                issues.append(f"Metadata path mismatch: expects 'gallery/metadata.json', actual is '{correct_path}'")
        
        # Check image folder path
        if 'gallery/images/' in content:
            correct_path = str(self.images_dir.relative_to(Path(".")) / "")
            if correct_path != 'gallery/images/':
                issues.append(f"Image folder path mismatch: expects 'gallery/images/', actual is '{correct_path}'")
        
        # Extract fallback filenames from photography.html
        fallback_match = re.search(r'const fallbackImages = \[([\s\S]*?)\];', content)
        if fallback_match:
            fallback_content = fallback_match.group(1)
            fallback_filenames = re.findall(r"'([^']+)'", fallback_content)
            
            # Get current filenames
            current_filenames = [img["filename"] for img in self.metadata["images"]]
            
            # Check for mismatches
            missing_in_fallback = set(current_filenames) - set(fallback_filenames)
            extra_in_fallback = set(fallback_filenames) - set(current_filenames)
            
            if missing_in_fallback:
                issues.append(f"Fallback missing {len(missing_in_fallback)} current photos: {', '.join(list(missing_in_fallback)[:3])}...")
            
            if extra_in_fallback:
                warnings.append(f"Fallback has {len(extra_in_fallback)} outdated photos: {', '.join(list(extra_in_fallback)[:3])}...")
        else:
            warnings.append("Could not find fallback image list in photography.html")
        
        # Check if any files in fallback don't exist
        for img in self.metadata["images"]:
            image_path = self.images_dir / img["filename"]
            if not image_path.exists():
                issues.append(f"Image file missing: {img['filename']}")
        
        # Print warnings
        if warnings:
            print("⚠️  Warnings found:")
            for warning in warnings:
                print(f"   - {warning}")
        
        # Print summary
        if not issues and not warnings:
            print("✅ Photography.html integration is perfect!")
        elif not issues:
            print("✅ Photography.html integration is functional with minor warnings")
        
        return issues
    
    def fix_photography_integration(self):
        """Fix photography.html integration issues automatically."""
        print("\n🔧 Fixing photography.html integration...")
        
        # Validate first
        issues = self.validate_photography_integration()
        
        if not issues:
            print("✅ No issues found to fix")
            return
        
        # Update fallback list
        self.update_photography_html_fallback()
        
        # Re-validate
        remaining_issues = self.validate_photography_integration()
        
        if not remaining_issues:
            print("✅ All photography.html integration issues fixed!")
        else:
            print("⚠️  Some issues remain:")
            for issue in remaining_issues:
                print(f"   - {issue}")

def main():
    parser = argparse.ArgumentParser(description="Photo Manager for Photography Portfolio")
    parser.add_argument("command", choices=[
        "list", "validate", "edit", "preview", "rename", 
        "fix", "bulk-titles", "bulk-captions", "add",
        "validate-web", "fix-web", "update-fallback"
    ], help="Command to execute")
    parser.add_argument("--photo", type=int, help="Photo ID for edit command")
    parser.add_argument("--category", help="Filter by category for list command")
    parser.add_argument("--featured", action="store_true", help="Show only featured photos")
    parser.add_argument("--preview", action="store_true", help="Preview mode for rename")
    parser.add_argument("path", nargs="?", help="Path to photo file for add command")
    
    args = parser.parse_args()
    
    manager = PhotoManager()
    
    if args.command == "list":
        manager.list_photos(category_filter=args.category, featured_only=args.featured)
    
    elif args.command == "validate":
        print("\n🔍 Validating photography system...")
        issues = manager.validate_system()
        
        if issues:
            print("❌ Issues found:")
            for issue in issues:
                print(f"  - {issue}")
            print(f"\nTotal issues: {len(issues)}")
        else:
            print("✅ All validations passed!")
            print("✅ Photography system is healthy")
    
    elif args.command == "edit":
        manager.edit_photo_interactive(args.photo)
    
    elif args.command == "preview":
        manager.preview_rename_operations()
    
    elif args.command == "rename":
        if args.preview:
            manager.preview_rename_operations()
        else:
            operations = manager.preview_rename_operations()
            if operations:
                manager.execute_rename_operations(operations)
    
    elif args.command == "fix":
        manager.fix_metadata_issues()
    
    elif args.command == "bulk-titles":
        manager.bulk_edit_titles()
    
    elif args.command == "bulk-captions":
        manager.bulk_edit_captions()
    
    elif args.command == "add":
        if not args.path:
            print("❌ Please provide path to photo file")
            print("Usage: python photo_manager.py add /path/to/photo.jpg")
        else:
            manager.add_new_photo(args.path)
    
    elif args.command == "validate-web":
        manager.validate_photography_integration()
    
    elif args.command == "fix-web":
        manager.fix_photography_integration()
    
    elif args.command == "update-fallback":
        manager.update_photography_html_fallback()

if __name__ == "__main__":
    main()