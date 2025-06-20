#!/usr/bin/env python3
"""
LinkedIn Profile Manager
A tool for managing LinkedIn profile data and updating the about page.

Usage:
    python linkedin_manager.py parse       # Parse LinkedIn data and create profile
    python linkedin_manager.py interactive # Interactive mode to edit/add experiences
    python linkedin_manager.py update      # Update about.html with latest profile data
    python linkedin_manager.py validate    # Validate profile data structure
    python linkedin_manager.py preview     # Preview generated HTML sections
    python linkedin_manager.py skills      # Show extracted skills summary
    python linkedin_manager.py list        # List all current profile data
"""

import os
import sys
import json
import re
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import shutil

class LinkedInManager:
    def __init__(self):
        self.base_dir = Path(".")
        self.config_file = Path("linkedin_profile.json")
        self.about_file = Path("about.html")
        self.backup_dir = Path(".backups")
        self.backup_dir.mkdir(exist_ok=True)
        
        # Load existing profile data
        self.profile_data = self.load_profile_data()
        
    def load_profile_data(self) -> Dict:
        """Load existing LinkedIn profile data."""
        if not self.config_file.exists():
            return self.create_default_profile()
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading profile data: {e}")
            return self.create_default_profile()
    
    def create_default_profile(self) -> Dict:
        """Create default profile structure."""
        return {
            "profile": {
                "name": "Manas Pandey",
                "title": "Undergraduate & Researcher",
                "summary": "Undergraduate Undergraduate at IIT Kanpur exploring the intersection of Physics and Artificial Intelligence.",
                "last_updated": None,
                "version": "1.0.0"
            },
            "experience": [],
            "education": [],
            "skills": {},
            "metadata": {
                "total_experiences": 0,
                "total_education": 0,
                "last_parsed": None
            }
        }
    
    def save_profile_data(self):
        """Save profile data to file."""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.profile_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving profile data: {e}")
    
    def parse_linkedin_experience(self, linkedin_text: str) -> List[Dict]:
        """Parse LinkedIn experience text into structured data."""
        experiences = []
        
        # Split by experience entries (looking for company logos or clear separators)
        experience_blocks = self.split_experience_blocks(linkedin_text)
        
        for block in experience_blocks:
            experience = self.parse_single_experience(block)
            if experience:
                experiences.append(experience)
        
        return experiences
    
    def split_experience_blocks(self, text: str) -> List[str]:
        """Split LinkedIn text into individual experience blocks."""
        # Remove common LinkedIn formatting artifacts
        clean_text = re.sub(r'\s+logo\s*', ' ', text)
        clean_text = re.sub(r'·\s*', '· ', clean_text)
        
        # Split by patterns that indicate new experiences
        # Look for patterns like "Title\nTitle\nCompany Name · Type"
        blocks = []
        lines = clean_text.split('\n')
        current_block = []
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
                
            # Check if this line starts a new experience block
            if self.is_new_experience_start(line, lines[i:i+5] if i+5 < len(lines) else lines[i:]):
                if current_block:
                    blocks.append('\n'.join(current_block))
                    current_block = []
            
            current_block.append(line)
        
        # Add the last block
        if current_block:
            blocks.append('\n'.join(current_block))
        
        return blocks
    
    def is_new_experience_start(self, line: str, next_lines: List[str]) -> bool:
        """Determine if a line starts a new experience entry."""
        # Skip common headers
        if line.lower() in ['experience', 'education']:
            return False
            
        # Look for patterns indicating a job title followed by company
        next_few = next_lines[:3] if len(next_lines) >= 3 else next_lines
        next_text = ' '.join(next_few)
        
        # Check for company indicators
        company_indicators = ['·', 'Full-time', 'Part-time', 'Internship', 'Institute', 'University', 'IIT', 'Club']
        has_company_indicator = any(indicator in next_text for indicator in company_indicators)
        
        # Check for date patterns in next lines
        has_date_pattern = bool(re.search(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{4}', next_text))
        
        return has_company_indicator or has_date_pattern
    
    def parse_single_experience(self, block: str) -> Optional[Dict]:
        """Parse a single experience block into structured data."""
        lines = [line.strip() for line in block.split('\n') if line.strip()]
        
        if len(lines) < 2:
            return None
        
        experience = {
            "title": "",
            "company": "",
            "type": "",
            "duration": "",
            "location": "",
            "skills": [],
            "website": "",
            "description": ""
        }
        
        # Parse title (usually first non-duplicate line)
        title_candidates = []
        for line in lines[:3]:
            if line not in title_candidates:
                title_candidates.append(line)
        
        if title_candidates:
            experience["title"] = title_candidates[0]
        
        # Parse company and type (look for · separator)
        for line in lines:
            if '·' in line:
                parts = line.split('·')
                if len(parts) >= 2:
                    experience["company"] = parts[0].strip()
                    experience["type"] = parts[1].strip()
                break
        
        # Parse duration (look for date patterns)
        duration_pattern = r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{4}\s*[-–]\s*(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{4}|Present|\d+\s*(yr|mo)'
        for line in lines:
            if re.search(duration_pattern, line):
                experience["duration"] = line.strip()
                break
        
        # Parse location (look for geographic indicators)
        location_indicators = ['Germany', 'India', 'Kanpur', 'Mainz', 'On-site', 'Remote']
        for line in lines:
            if any(indicator in line for indicator in location_indicators):
                experience["location"] = line.strip()
                break
        
        # Parse skills (look for "Skills:" prefix)
        for line in lines:
            if line.startswith('Skills:'):
                skills_text = line.replace('Skills:', '').strip()
                experience["skills"] = [skill.strip() for skill in skills_text.split('·') if skill.strip()]
                break
        
        # Parse website (look for "website" keyword)
        for line in lines:
            if 'website' in line.lower() or 'Website' in line:
                experience["website"] = line.strip()
                break
        
        return experience if experience["title"] and experience["company"] else None
    
    def parse_linkedin_education(self, linkedin_text: str) -> List[Dict]:
        """Parse LinkedIn education text into structured data."""
        education_entries = []
        
        # Look for education section
        education_section = self.extract_education_section(linkedin_text)
        if not education_section:
            return education_entries
        
        # Parse individual education entries
        education_blocks = self.split_education_blocks(education_section)
        
        for block in education_blocks:
            education = self.parse_single_education(block)
            if education:
                education_entries.append(education)
        
        return education_entries
    
    def extract_education_section(self, text: str) -> str:
        """Extract the education section from LinkedIn text."""
        lines = text.split('\n')
        education_start = -1
        
        for i, line in enumerate(lines):
            if line.strip().lower() == 'education':
                education_start = i
                break
        
        if education_start == -1:
            return ""
        
        # Extract from education start to end of text
        education_lines = lines[education_start+1:]
        return '\n'.join(education_lines)
    
    def split_education_blocks(self, text: str) -> List[str]:
        """Split education text into individual institution blocks."""
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        blocks = []
        current_block = []
        
        for line in lines:
            # Check if this line starts a new education entry (institution name pattern)
            if self.is_new_education_start(line):
                if current_block:
                    blocks.append('\n'.join(current_block))
                    current_block = []
            
            current_block.append(line)
        
        if current_block:
            blocks.append('\n'.join(current_block))
        
        return blocks
    
    def is_new_education_start(self, line: str) -> bool:
        """Determine if a line starts a new education entry."""
        education_indicators = [
            'Institute', 'University', 'College', 'School', 'IIT', 'Delhi Public'
        ]
        return any(indicator in line for indicator in education_indicators)
    
    def parse_single_education(self, block: str) -> Optional[Dict]:
        """Parse a single education block into structured data."""
        lines = [line.strip() for line in block.split('\n') if line.strip()]
        
        if len(lines) < 2:
            return None
        
        education = {
            "institution": "",
            "degree": "",
            "field": "",
            "duration": "",
            "location": ""
        }
        
        # First line is usually institution name
        if lines:
            education["institution"] = lines[0]
        
        # Look for degree information
        for line in lines:
            if any(degree_type in line for degree_type in ['Bachelor', 'Master', 'PhD', 'Diploma', 'BS', 'MS']):
                # Parse degree and field
                if ',' in line:
                    parts = line.split(',')
                    education["degree"] = parts[0].strip()
                    if len(parts) > 1:
                        education["field"] = parts[1].strip()
                else:
                    education["degree"] = line.strip()
                break
        
        return education if education["institution"] else None
    
    def extract_all_skills(self) -> Dict[str, List[str]]:
        """Extract and categorize all skills from experiences."""
        all_skills = []
        
        for experience in self.profile_data.get("experience", []):
            all_skills.extend(experience.get("skills", []))
        
        # Categorize skills
        skill_categories = {
            "Technical": [],
            "Management": [],
            "Creative": [],
            "Communication": [],
            "Research": []
        }
        
        # Categorization logic
        technical_keywords = ['Python', 'MATLAB', 'Programming', 'Data', 'Analysis', 'Computing']
        management_keywords = ['Management', 'Leadership', 'Planning', 'Organization']
        creative_keywords = ['Design', 'Editing', 'Adobe', 'Photoshop', 'Canva', 'Creative']
        communication_keywords = ['Communication', 'Writing', 'Public Relations', 'Marketing', 'Narrator']
        research_keywords = ['Research', 'Astrophysics', 'Astronomy', 'Physics', 'Science']
        
        for skill in set(all_skills):  # Remove duplicates
            skill_lower = skill.lower()
            categorized = False
            
            if any(keyword.lower() in skill_lower for keyword in technical_keywords):
                skill_categories["Technical"].append(skill)
                categorized = True
            if any(keyword.lower() in skill_lower for keyword in management_keywords):
                skill_categories["Management"].append(skill)
                categorized = True
            if any(keyword.lower() in skill_lower for keyword in creative_keywords):
                skill_categories["Creative"].append(skill)
                categorized = True
            if any(keyword.lower() in skill_lower for keyword in communication_keywords):
                skill_categories["Communication"].append(skill)
                categorized = True
            if any(keyword.lower() in skill_lower for keyword in research_keywords):
                skill_categories["Research"].append(skill)
                categorized = True
            
            # If not categorized, add to technical as default
            if not categorized:
                skill_categories["Technical"].append(skill)
        
        return skill_categories
    
    def generate_experience_html(self) -> str:
        """Generate HTML for experience section."""
        if not self.profile_data.get("experience"):
            return ""
        
        html_lines = [
            '    <section class="experience-section">',
            '        <h2>Experience</h2>',
            '        <div class="experience-timeline">'
        ]
        
        for i, exp in enumerate(self.profile_data["experience"]):
            html_lines.append(self.generate_experience_card(exp, i))
        
        html_lines.extend([
            '        </div>',
            '    </section>'
        ])
        
        return '\n'.join(html_lines)
    
    def generate_experience_card(self, experience: Dict, index: int) -> str:
        """Generate HTML card for a single experience."""
        skills_html = ""
        if experience.get("skills"):
            skills_tags = [f'<span class="skill-tag">{skill}</span>' for skill in experience["skills"]]
            skills_html = f'                <div class="experience-skills">{" ".join(skills_tags)}</div>'
        
        location_html = ""
        if experience.get("location"):
            location_html = f'                <div class="experience-location">{experience["location"]}</div>'
        
        website_html = ""
        if experience.get("website"):
            website_html = f'                <div class="experience-website"><a href="#" class="experience-link">{experience["website"]}</a></div>'
        
        return f"""            <div class="experience-card" data-index="{index}">
                <div class="experience-header">
                    <h3 class="experience-title">{experience["title"]}</h3>
                    <div class="experience-company">{experience["company"]}</div>
                    <div class="experience-meta">
                        <span class="experience-type">{experience.get("type", "")}</span>
                        <span class="experience-duration">{experience.get("duration", "")}</span>
                    </div>
                </div>
{location_html}
{skills_html}
{website_html}
            </div>"""
    
    def generate_education_html(self) -> str:
        """Generate HTML for education section."""
        if not self.profile_data.get("education"):
            return ""
        
        html_lines = [
            '    <section class="education-section">',
            '        <h2>Education</h2>',
            '        <div class="education-list">'
        ]
        
        for i, edu in enumerate(self.profile_data["education"]):
            html_lines.append(self.generate_education_card(edu, i))
        
        html_lines.extend([
            '        </div>',
            '    </section>'
        ])
        
        return '\n'.join(html_lines)
    
    def generate_education_card(self, education: Dict, index: int) -> str:
        """Generate HTML card for a single education entry."""
        field_html = ""
        if education.get("field"):
            field_html = f'                <div class="education-field">{education["field"]}</div>'
        
        return f"""            <div class="education-card" data-index="{index}">
                <div class="education-header">
                    <h3 class="education-institution">{education["institution"]}</h3>
                    <div class="education-degree">{education.get("degree", "")}</div>
                </div>
{field_html}
            </div>"""
    
    def generate_skills_html(self) -> str:
        """Generate HTML for skills section."""
        skills_by_category = self.extract_all_skills()
        
        if not any(skills_by_category.values()):
            return ""
        
        html_lines = [
            '    <section class="skills-section">',
            '        <h2>Skills & Expertise</h2>',
            '        <div class="skills-grid">'
        ]
        
        for category, skills in skills_by_category.items():
            if skills:
                skills_tags = [f'<span class="skill-tag">{skill}</span>' for skill in skills]
                html_lines.append(f"""            <div class="skills-category">
                <h4 class="skills-category-title">{category}</h4>
                <div class="skills-tags">{" ".join(skills_tags)}</div>
            </div>""")
        
        html_lines.extend([
            '        </div>',
            '    </section>'
        ])
        
        return '\n'.join(html_lines)
    
    def generate_professional_summary_html(self) -> str:
        """Generate HTML for professional summary section."""
        summary = self.profile_data["profile"].get("summary", "")
        
        return f"""    <section class="professional-summary">
        <h2>Professional Journey</h2>
        <p class="summary-text">{summary}</p>
    </section>"""
    
    def parse_provided_linkedin_data(self):
        """Parse the LinkedIn data provided by the user with manual entry."""
        # Manually create the structured data based on provided LinkedIn information
        experiences = [
            {
                "title": "Associate Member",
                "company": "Institute of Physics",
                "type": "Full-time",
                "duration": "Oct 2023 - Dec 2024 · 1 yr 3 mos",
                "location": "",
                "skills": [],
                "website": "",
                "description": ""
            },
            {
                "title": "Research Intern",
                "company": "Helmholtz-Institut Mainz",
                "type": "Full-time",
                "duration": "May 2024 - Jul 2024 · 3 mos",
                "location": "Mainz, Rhineland-Palatinate, Germany · On-site",
                "skills": [],
                "website": "",
                "description": ""
            },
            {
                "title": "Research Intern",
                "company": "Indian Institute of Science (IISc)",
                "type": "Internship",
                "duration": "May 2023 - Jul 2023 · 3 mos",
                "location": "",
                "skills": [],
                "website": "",
                "description": ""
            },
            {
                "title": "Secretary",
                "company": "Astronomy Club, IIT Kanpur",
                "type": "Part-time",
                "duration": "Sep 2022 - Apr 2023 · 8 mos",
                "location": "",
                "skills": ["Management", "Editing", "Astrophysics", "Astronomy"],
                "website": "Astronomy Club Website",
                "description": ""
            },
            {
                "title": "Secretary, Research Wing",
                "company": "Academics and Career Council, IIT Kanpur",
                "type": "Part-time",
                "duration": "Jun 2022 - Apr 2023 · 11 mos",
                "location": "Kanpur, Uttar Pradesh, India",
                "skills": ["Public Relations", "Narrator", "Marketing", "Writing", "Communication", "Design", "Editing"],
                "website": "AnC Council IITK website",
                "description": ""
            },
            {
                "title": "Secretary, Book Club",
                "company": "Media and Cultural Council, IIT Kanpur",
                "type": "Part-time",
                "duration": "Jun 2022 - Apr 2023 · 11 mos",
                "location": "",
                "skills": ["Cataloging", "Writing", "Adobe Photoshop", "Editing", "Canva"],
                "website": "Book Club at MnC Council IITK website",
                "description": ""
            }
        ]
        
        education = [
            {
                "institution": "Indian Institute of Technology, Kanpur",
                "degree": "Bachelor of Science - BS",
                "field": "Physics",
                "duration": "2021 - 2025 (Expected)",
                "location": "Kanpur, Uttar Pradesh, India"
            },
            {
                "institution": "Delhi Public School Patna",
                "degree": "High School Diploma",
                "field": "High School/Secondary Diplomas and Certificates",
                "duration": "2019 - 2021",
                "location": "Patna, Bihar, India"
            }
        ]
        
        # Update profile data
        self.profile_data["experience"] = experiences
        self.profile_data["education"] = education
        self.profile_data["metadata"]["total_experiences"] = len(experiences)
        self.profile_data["metadata"]["total_education"] = len(education)
        self.profile_data["metadata"]["last_parsed"] = datetime.now().isoformat()
        self.profile_data["profile"]["last_updated"] = datetime.now().isoformat()
        
        # Extract and store skills
        self.profile_data["skills"] = self.extract_all_skills()
        
        print(f"✅ Parsed {len(experiences)} experience entries")
        print(f"✅ Parsed {len(education)} education entries")
        print(f"✅ Extracted skills in {len(self.profile_data['skills'])} categories")
        
        # Save the parsed data
        self.save_profile_data()
    
    def update_about_page(self):
        """Update about.html with LinkedIn profile data."""
        if not self.about_file.exists():
            print(f"About file not found: {self.about_file}")
            return False
        
        # Create backup
        backup_path = self.backup_dir / f"about_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        shutil.copy2(self.about_file, backup_path)
        print(f"Backup created: {backup_path}")
        
        # Read current about.html
        with open(self.about_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Generate LinkedIn content sections
        summary_html = self.generate_professional_summary_html()
        experience_html = self.generate_experience_html()
        education_html = self.generate_education_html()
        skills_html = self.generate_skills_html()
        
        # Combine all sections
        linkedin_content = f"""        <h1 class="page-title">About</h1>
        
{summary_html}
        
{experience_html}
        
{education_html}
        
{skills_html}"""
        
        # Replace the main content (between <main class="page-container"> and </main>)
        main_pattern = r'(<main class="page-container">)(.*?)(</main>)'
        new_content = re.sub(
            main_pattern,
            f'\\1\n{linkedin_content}\n    \\3',
            html_content,
            flags=re.DOTALL
        )
        
        # Write updated content
        with open(self.about_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ About page updated with LinkedIn profile data!")
        print(f"   - {len(self.profile_data['experience'])} experience entries")
        print(f"   - {len(self.profile_data['education'])} education entries")
        print(f"   - {sum(len(skills) for skills in self.profile_data['skills'].values())} skills")
        
        return True
    
    def validate_profile_data(self):
        """Validate the profile data structure."""
        issues = []
        
        # Check required fields
        if not self.profile_data.get("profile", {}).get("name"):
            issues.append("Missing profile name")
        
        # Validate experiences
        for i, exp in enumerate(self.profile_data.get("experience", [])):
            if not exp.get("title"):
                issues.append(f"Experience {i+1}: Missing title")
            if not exp.get("company"):
                issues.append(f"Experience {i+1}: Missing company")
        
        # Validate education
        for i, edu in enumerate(self.profile_data.get("education", [])):
            if not edu.get("institution"):
                issues.append(f"Education {i+1}: Missing institution")
        
        return issues
    
    def preview_generated_html(self):
        """Preview the generated HTML sections."""
        print("\n" + "="*80)
        print("LINKEDIN PROFILE HTML PREVIEW")
        print("="*80)
        
        print("\n📋 PROFESSIONAL SUMMARY:")
        print(self.generate_professional_summary_html())
        
        print("\n💼 EXPERIENCE SECTION:")
        print(self.generate_experience_html())
        
        print("\n🎓 EDUCATION SECTION:")
        print(self.generate_education_html())
        
        print("\n🛠️ SKILLS SECTION:")
        print(self.generate_skills_html())
    
    def show_skills_summary(self):
        """Show extracted skills summary."""
        skills_by_category = self.extract_all_skills()
        
        print("\n" + "="*60)
        print("EXTRACTED SKILLS SUMMARY")
        print("="*60)
        
        total_skills = sum(len(skills) for skills in skills_by_category.values())
        print(f"Total Skills: {total_skills}")
        
        for category, skills in skills_by_category.items():
            if skills:
                print(f"\n{category} ({len(skills)} skills):")
                print("  " + " · ".join(skills))
    
    def interactive_mode(self):
        """Interactive mode for managing profile data."""
        while True:
            print("\n" + "="*80)
            print("LINKEDIN PROFILE INTERACTIVE MANAGER")
            print("="*80)
            print("1. View current profile data")
            print("2. Add new experience")
            print("3. Edit existing experience")
            print("4. Add new education")
            print("5. Edit existing education")
            print("6. Update professional summary")
            print("7. Generate and preview HTML")
            print("8. Update about page")
            print("9. Exit")
            
            try:
                choice = input("\nSelect option (1-9): ").strip()
                
                if choice == '1':
                    self.show_current_profile()
                elif choice == '2':
                    self.add_experience_interactive()
                elif choice == '3':
                    self.edit_experience_interactive()
                elif choice == '4':
                    self.add_education_interactive()
                elif choice == '5':
                    self.edit_education_interactive()
                elif choice == '6':
                    self.update_summary_interactive()
                elif choice == '7':
                    self.preview_generated_html()
                elif choice == '8':
                    self.update_about_page()
                elif choice == '9':
                    print("Goodbye!")
                    break
                else:
                    print("Invalid option. Please try again.")
                    
            except KeyboardInterrupt:
                print("\nExiting...")
                break
    
    def show_current_profile(self):
        """Show current profile data in a readable format."""
        print("\n" + "="*60)
        print("CURRENT PROFILE DATA")
        print("="*60)
        
        # Profile info
        profile = self.profile_data["profile"]
        print(f"Name: {profile['name']}")
        print(f"Title: {profile['title']}")
        print(f"Summary: {profile['summary']}")
        print(f"Last Updated: {profile.get('last_updated', 'Never')}")
        
        # Experience
        print(f"\n📼 EXPERIENCE ({len(self.profile_data['experience'])} entries):")
        for i, exp in enumerate(self.profile_data["experience"], 1):
            print(f"  {i}. {exp['title']} at {exp['company']} ({exp.get('duration', 'No duration')})")
        
        # Education
        print(f"\n🎓 EDUCATION ({len(self.profile_data['education'])} entries):")
        for i, edu in enumerate(self.profile_data["education"], 1):
            print(f"  {i}. {edu.get('degree', 'No degree')} at {edu['institution']}")
        
        # Skills summary
        skills_count = sum(len(skills) for skills in self.profile_data['skills'].values())
        print(f"\n🛠️ SKILLS: {skills_count} total across {len(self.profile_data['skills'])} categories")
    
    def add_experience_interactive(self):
        """Add new experience entry interactively."""
        print("\n" + "="*60)
        print("ADD NEW EXPERIENCE")
        print("="*60)
        
        experience = {}
        
        experience["title"] = input("Job Title: ").strip()
        experience["company"] = input("Company: ").strip()
        experience["type"] = input("Type (Full-time/Part-time/Internship): ").strip()
        experience["duration"] = input("Duration (e.g., Jan 2023 - Dec 2023): ").strip()
        experience["location"] = input("Location (optional): ").strip()
        
        # Skills input
        skills_input = input("Skills (comma-separated, optional): ").strip()
        experience["skills"] = [skill.strip() for skill in skills_input.split(',')] if skills_input else []
        
        experience["website"] = input("Website/Link (optional): ").strip()
        experience["description"] = input("Description (optional): ").strip()
        
        # Add to profile
        self.profile_data["experience"].append(experience)
        self.profile_data["metadata"]["total_experiences"] = len(self.profile_data["experience"])
        self.profile_data["profile"]["last_updated"] = datetime.now().isoformat()
        
        # Update skills
        self.profile_data["skills"] = self.extract_all_skills()
        
        # Save
        self.save_profile_data()
        
        print(f"\n✅ Added experience: {experience['title']} at {experience['company']}")
    
    def edit_experience_interactive(self):
        """Edit existing experience entry interactively."""
        if not self.profile_data["experience"]:
            print("No experience entries to edit.")
            return
        
        print("\n" + "="*60)
        print("EDIT EXPERIENCE")
        print("="*60)
        
        # Show current experiences
        for i, exp in enumerate(self.profile_data["experience"], 1):
            print(f"  {i}. {exp['title']} at {exp['company']}")
        
        try:
            choice = int(input(f"\nSelect experience to edit (1-{len(self.profile_data['experience'])}): "))
            if 1 <= choice <= len(self.profile_data["experience"]):
                exp_index = choice - 1
                exp = self.profile_data["experience"][exp_index]
                
                print(f"\nEditing: {exp['title']} at {exp['company']}")
                print("Press Enter to keep current value, or type new value:")
                
                # Edit each field
                new_title = input(f"Title [{exp['title']}]: ").strip()
                if new_title:
                    exp["title"] = new_title
                
                new_company = input(f"Company [{exp['company']}]: ").strip()
                if new_company:
                    exp["company"] = new_company
                
                new_type = input(f"Type [{exp['type']}]: ").strip()
                if new_type:
                    exp["type"] = new_type
                
                new_duration = input(f"Duration [{exp['duration']}]: ").strip()
                if new_duration:
                    exp["duration"] = new_duration
                
                new_location = input(f"Location [{exp['location']}]: ").strip()
                if new_location or input("Clear location? (y/n): ").lower() == 'y':
                    exp["location"] = new_location
                
                # Skills
                current_skills = ", ".join(exp['skills'])
                new_skills = input(f"Skills [{current_skills}]: ").strip()
                if new_skills:
                    exp["skills"] = [skill.strip() for skill in new_skills.split(',')]
                
                # Save changes
                self.profile_data["skills"] = self.extract_all_skills()
                self.profile_data["profile"]["last_updated"] = datetime.now().isoformat()
                self.save_profile_data()
                
                print(f"\n✅ Updated experience: {exp['title']} at {exp['company']}")
            else:
                print("Invalid selection.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    def add_education_interactive(self):
        """Add new education entry interactively."""
        print("\n" + "="*60)
        print("ADD NEW EDUCATION")
        print("="*60)
        
        education = {}
        
        education["institution"] = input("Institution: ").strip()
        education["degree"] = input("Degree: ").strip()
        education["field"] = input("Field of Study: ").strip()
        education["duration"] = input("Duration (e.g., 2021 - 2025): ").strip()
        education["location"] = input("Location (optional): ").strip()
        
        # Add to profile
        self.profile_data["education"].append(education)
        self.profile_data["metadata"]["total_education"] = len(self.profile_data["education"])
        self.profile_data["profile"]["last_updated"] = datetime.now().isoformat()
        
        # Save
        self.save_profile_data()
        
        print(f"\n✅ Added education: {education['degree']} at {education['institution']}")
    
    def edit_education_interactive(self):
        """Edit existing education entry interactively."""
        if not self.profile_data["education"]:
            print("No education entries to edit.")
            return
        
        print("\n" + "="*60)
        print("EDIT EDUCATION")
        print("="*60)
        
        # Show current education
        for i, edu in enumerate(self.profile_data["education"], 1):
            print(f"  {i}. {edu.get('degree', 'No degree')} at {edu['institution']}")
        
        try:
            choice = int(input(f"\nSelect education to edit (1-{len(self.profile_data['education'])}): "))
            if 1 <= choice <= len(self.profile_data["education"]):
                edu_index = choice - 1
                edu = self.profile_data["education"][edu_index]
                
                print(f"\nEditing: {edu.get('degree', 'No degree')} at {edu['institution']}")
                print("Press Enter to keep current value, or type new value:")
                
                # Edit each field
                new_institution = input(f"Institution [{edu['institution']}]: ").strip()
                if new_institution:
                    edu["institution"] = new_institution
                
                new_degree = input(f"Degree [{edu.get('degree', '')}]: ").strip()
                if new_degree:
                    edu["degree"] = new_degree
                
                new_field = input(f"Field [{edu.get('field', '')}]: ").strip()
                if new_field:
                    edu["field"] = new_field
                
                new_duration = input(f"Duration [{edu.get('duration', '')}]: ").strip()
                if new_duration:
                    edu["duration"] = new_duration
                
                # Save changes
                self.profile_data["profile"]["last_updated"] = datetime.now().isoformat()
                self.save_profile_data()
                
                print(f"\n✅ Updated education: {edu.get('degree', 'Education')} at {edu['institution']}")
            else:
                print("Invalid selection.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    def update_summary_interactive(self):
        """Update professional summary interactively."""
        print("\n" + "="*60)
        print("UPDATE PROFESSIONAL SUMMARY")
        print("="*60)
        
        current_summary = self.profile_data["profile"]["summary"]
        print(f"Current summary: {current_summary}")
        
        new_summary = input("\nEnter new summary (or press Enter to keep current): ").strip()
        if new_summary:
            self.profile_data["profile"]["summary"] = new_summary
            self.profile_data["profile"]["last_updated"] = datetime.now().isoformat()
            self.save_profile_data()
            print("\n✅ Professional summary updated!")
        else:
            print("\nSummary unchanged.")
    
    def list_profile_data(self):
        """List all profile data in detail."""
        print("\n" + "="*80)
        print("DETAILED PROFILE DATA")
        print("="*80)
        
        # Profile
        print("\n👤 PROFILE:")
        for key, value in self.profile_data["profile"].items():
            print(f"  {key}: {value}")
        
        # Experience
        print(f"\n💼 EXPERIENCE ({len(self.profile_data['experience'])} entries):")
        for i, exp in enumerate(self.profile_data["experience"], 1):
            print(f"\n  [{i}] {exp['title']}")
            for key, value in exp.items():
                if key != 'title':
                    print(f"      {key}: {value}")
        
        # Education
        print(f"\n🎓 EDUCATION ({len(self.profile_data['education'])} entries):")
        for i, edu in enumerate(self.profile_data["education"], 1):
            print(f"\n  [{i}] {edu['institution']}")
            for key, value in edu.items():
                if key != 'institution':
                    print(f"      {key}: {value}")
        
        # Skills
        print(f"\n🛠️ SKILLS:")
        for category, skills in self.profile_data["skills"].items():
            if skills:
                print(f"  {category}: {', '.join(skills)}")

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    
    manager = LinkedInManager()
    command = sys.argv[1].lower()
    
    if command == 'parse':
        manager.parse_provided_linkedin_data()
        
    elif command == 'update':
        manager.update_about_page()
        
    elif command == 'validate':
        issues = manager.validate_profile_data()
        if issues:
            print("⚠️ Issues found:")
            for issue in issues:
                print(f"   - {issue}")
        else:
            print("✅ Profile data validation passed!")
            
    elif command == 'preview':
        manager.preview_generated_html()
        
    elif command == 'skills':
        manager.show_skills_summary()
        
    elif command == 'interactive':
        manager.interactive_mode()
        
    elif command == 'list':
        manager.list_profile_data()
        
    else:
        print(f"Unknown command: {command}")
        print(__doc__)

if __name__ == "__main__":
    main()