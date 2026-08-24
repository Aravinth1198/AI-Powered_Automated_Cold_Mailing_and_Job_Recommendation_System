

import re
import sys
from datetime import datetime
from typing import Dict, List, Tuple, Any, Optional

class ApplicantValidator:
    """
    Comprehensive validation class for applicant data
    Each validation method returns (is_valid, error_message, cleaned_value)
    """
    
    # Predefined valid options
    VALID_EDUCATION_LEVELS = [
        "High School",
        "Bachelor's Degree",
        "Master's Degree",
        "PhD",
        "Other"
    ]
    
    VALID_JOB_ROLES = [
        "Software Engineer",
        "Data Scientist",
        "Product Manager",
        "DevOps Engineer",
        "Frontend Developer",
        "Backend Developer",
        "Full Stack Developer",
        "Machine Learning Engineer",
        "Data Analyst",
        "Business Analyst",
        "Project Manager",
        "UX Designer",
        "QA Engineer",
        "System Administrator",
        "Cloud Architect"
    ]
    
    @staticmethod
    def validate_name(name: str) -> Tuple[bool, str, str]:
        """
        Validate applicant name
        Rules:
        - Required field
        - Minimum 2 characters
        - Maximum 100 characters
        - Only letters, spaces, hyphens, and apostrophes
        - Must have at least one letter
        """
        if not name or not name.strip():
            return False, "Name is required", ""
        
        name = name.strip()
        
        if len(name) < 2:
            return False, "Name must be at least 2 characters long", name
        
        if len(name) > 100:
            return False, "Name must not exceed 100 characters", name
        
        # Allow letters, spaces, hyphens, apostrophes
        if not re.match(r"^[A-Za-z\s\-']+$", name):
            return False, "Name can only contain letters, spaces, hyphens, and apostrophes", name
        
        # Must contain at least one letter
        if not any(c.isalpha() for c in name):
            return False, "Name must contain at least one letter", name
        
        return True, "Valid name", name
    
    @staticmethod
    def validate_email(email: str) -> Tuple[bool, str, str]:
        """
        Validate email address
        Rules:
        - Required field
        - Must be in valid email format
        - Must contain @ and domain
        - Maximum 255 characters
        """
        if not email or not email.strip():
            return False, "Email is required", ""
        
        email = email.strip().lower()
        
        if len(email) > 255:
            return False, "Email must not exceed 255 characters", email
        
        # Comprehensive email validation
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            return False, "Invalid email format. Example: user@domain.com", email
        
        # Additional checks
        local_part, domain = email.split('@')
        
        if len(local_part) < 1:
            return False, "Email local part cannot be empty", email
        
        if len(domain.split('.')) < 2:
            return False, "Email domain must have a valid TLD", email
        
        return True, "Valid email", email
    
    @staticmethod
    def validate_password(password: str) -> Tuple[bool, str, str]:
        """
        Validate password
        Rules:
        - Required field
        - Minimum 8 characters
        - Maximum 50 characters
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one number
        - At least one special character
        """
        if not password or not password.strip():
            return False, "Password is required", ""
        
        password = password.strip()
        
        if len(password) < 8:
            return False, "Password must be at least 8 characters long", password
        
        if len(password) > 50:
            return False, "Password must not exceed 50 characters", password
        
        # Check for uppercase
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter", password
        
        # Check for lowercase
        if not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter", password
        
        # Check for number
        if not re.search(r'\d', password):
            return False, "Password must contain at least one number", password
        
        # Check for special character
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False, "Password must contain at least one special character", password
        
        return True, "Strong password", password
    
    @staticmethod
    def validate_phone(phone: str) -> Tuple[bool, str, str]:
        """
        Validate phone number
        Rules:
        - Required field
        - Must be 10-15 digits (including country code)
        - Can include +, -, spaces, parentheses, dots
        """
        if not phone or not phone.strip():
            return False, "Phone number is required", ""
        
        phone = phone.strip()
        
        # Remove common formatting characters for length check
        phone_clean = re.sub(r'[\s\-\(\)\.]', '', phone)
        
        # Remove leading + if present
        if phone_clean.startswith('+'):
            phone_clean = phone_clean[1:]
        
        # Check if it contains only digits after cleaning
        if not phone_clean.isdigit():
            return False, "Phone number can only contain digits and formatting characters", phone
        
        # Check length
        if len(phone_clean) < 10:
            return False, "Phone number must have at least 10 digits", phone
        
        if len(phone_clean) > 15:
            return False, "Phone number must not exceed 15 digits", phone
        
        return True, "Valid phone number", phone
    
    @staticmethod
    def validate_skills(skills_str: str) -> Tuple[bool, str, List[str]]:
        """
        Validate skills
        Rules:
        - Required field
        - At least one skill
        - Maximum 20 skills
        - Each skill must be 2-50 characters
        - Skills separated by commas
        """
        if not skills_str or not skills_str.strip():
            return False, "At least one skill is required", []
        
        # Split by comma and clean
        skills = [s.strip() for s in skills_str.split(',') if s.strip()]
        
        if len(skills) == 0:
            return False, "At least one skill is required", []
        
        if len(skills) > 20:
            return False, f"Maximum 20 skills allowed (you have {len(skills)})", skills
        
        # Validate each skill
        for skill in skills:
            if len(skill) < 2:
                return False, f"Skill '{skill}' must be at least 2 characters long", skills
            if len(skill) > 50:
                return False, f"Skill '{skill}' must not exceed 50 characters", skills
            # Check for invalid characters
            if not re.match(r'^[A-Za-z0-9\s#\+\.\-]+$', skill):
                return False, f"Skill '{skill}' contains invalid characters", skills
        
        return True, f"Valid skills ({len(skills)} skills)", skills
    
    @staticmethod
    def validate_education(education_input: Dict[str, Any]) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Validate education data
        Rules:
        - Required fields: level, institution, field_of_study, graduation_year
        - level must be from predefined list
        - institution: 2-100 characters
        - field_of_study: 2-100 characters
        - graduation_year: 1950-current year
        """
        if not education_input:
            return False, "Education data is required", {}
        
        # Create a default structure if fields are missing
        education = {
            'level': education_input.get('level', ''),
            'institution': education_input.get('institution', ''),
            'field_of_study': education_input.get('field_of_study', ''),
            'graduation_year': education_input.get('graduation_year', '')
        }
        
        # Validate level
        if not education['level']:
            return False, "Education level is required", education
        if education['level'] not in ApplicantValidator.VALID_EDUCATION_LEVELS:
            return False, f"Invalid education level. Must be one of: {', '.join(ApplicantValidator.VALID_EDUCATION_LEVELS)}", education
        
        # Validate institution
        if not education['institution'] or not education['institution'].strip():
            return False, "Institution name is required", education
        education['institution'] = education['institution'].strip()
        if len(education['institution']) < 2:
            return False, "Institution name must be at least 2 characters", education
        if len(education['institution']) > 100:
            return False, "Institution name must not exceed 100 characters", education
        
        # Validate field of study
        if not education['field_of_study'] or not education['field_of_study'].strip():
            return False, "Field of study is required", education
        education['field_of_study'] = education['field_of_study'].strip()
        if len(education['field_of_study']) < 2:
            return False, "Field of study must be at least 2 characters", education
        if len(education['field_of_study']) > 100:
            return False, "Field of study must not exceed 100 characters", education
        
        # Validate graduation year
        if not education['graduation_year']:
            return False, "Graduation year is required", education
        try:
            year = int(education['graduation_year'])
            current_year = datetime.now().year
            if year < 1950:
                return False, f"Graduation year must be at least 1950 (got {year})", education
            if year > current_year:
                return False, f"Graduation year cannot be in the future (got {year})", education
            education['graduation_year'] = str(year)  # Convert back to string
        except ValueError:
            return False, "Graduation year must be a valid number", education
        
        return True, "Valid education data", education
    
    @staticmethod
    def validate_experience(exp_input: List[Dict[str, Any]]) -> Tuple[bool, str, List[Dict[str, Any]]]:
        """
        Validate experience data
        Rules:
        - Required field (at least one experience)
        - Each experience: company, title, start_date required
        - end_date required unless current position
        - Date format: YYYY-MM-DD
        - end_date must be after start_date
        """
        if not exp_input:
            return False, "At least one work experience is required", []
        
        validated_experience = []
        
        for idx, exp in enumerate(exp_input):
            # Create default structure
            experience = {
                'company': exp.get('company', ''),
                'title': exp.get('title', ''),
                'start_date': exp.get('start_date', ''),
                'end_date': exp.get('end_date', ''),
                'current': exp.get('current', False)
            }
            
            # Validate company
            if not experience['company'] or not experience['company'].strip():
                return False, f"Experience #{idx+1}: Company name is required", []
            experience['company'] = experience['company'].strip()
            if len(experience['company']) < 2:
                return False, f"Experience #{idx+1}: Company name must be at least 2 characters", []
            
            # Validate title
            if not experience['title'] or not experience['title'].strip():
                return False, f"Experience #{idx+1}: Job title is required", []
            experience['title'] = experience['title'].strip()
            if len(experience['title']) < 2:
                return False, f"Experience #{idx+1}: Job title must be at least 2 characters", []
            
            # Validate start_date
            if not experience['start_date']:
                return False, f"Experience #{idx+1}: Start date is required", []
            try:
                start_date = datetime.strptime(experience['start_date'], '%Y-%m-%d')
            except ValueError:
                return False, f"Experience #{idx+1}: Invalid start date format. Use YYYY-MM-DD", []
            
            # Validate end_date
            if not experience['current']:
                if not experience['end_date']:
                    return False, f"Experience #{idx+1}: End date is required for completed positions", []
                try:
                    end_date = datetime.strptime(experience['end_date'], '%Y-%m-%d')
                    if end_date < start_date:
                        return False, f"Experience #{idx+1}: End date must be after start date", []
                except ValueError:
                    return False, f"Experience #{idx+1}: Invalid end date format. Use YYYY-MM-DD", []
            else:
                # If current position, set end_date to None or current date
                experience['end_date'] = None
            
            validated_experience.append(experience)
        
        return True, f"Valid experience data ({len(validated_experience)} entries)", validated_experience
    
    @staticmethod
    def validate_job_role(job_role: str) -> Tuple[bool, str, str]:
        """
        Validate job role
        Rules:
        - Required field
        - 2-100 characters
        - Should be from predefined list or custom
        """
        if not job_role or not job_role.strip():
            return False, "Job role is required", ""
        
        job_role = job_role.strip()
        
        if len(job_role) < 2:
            return False, "Job role must be at least 2 characters", job_role
        
        if len(job_role) > 100:
            return False, "Job role must not exceed 100 characters", job_role
        
        # Check if it's in predefined list (case-insensitive)
        if job_role.lower() in [role.lower() for role in ApplicantValidator.VALID_JOB_ROLES]:
            return True, f"Valid job role (from standard list)", job_role
        
        # Allow custom job roles but warn
        return True, f"Valid job role (custom role)", job_role
    
    @staticmethod
    def validate_location(location: str) -> Tuple[bool, str, str]:
        """
        Validate location
        Rules:
        - Required field
        - 2-100 characters
        - Can include letters, numbers, spaces, commas, hyphens, periods
        """
        if not location or not location.strip():
            return False, "Location is required", ""
        
        location = location.strip()
        
        if len(location) < 2:
            return False, "Location must be at least 2 characters", location
        
        if len(location) > 100:
            return False, "Location must not exceed 100 characters", location
        
        # Allow letters, numbers, spaces, commas, hyphens, periods, apostrophes
        if not re.match(r"^[A-Za-z0-9\s,\.\-']+$", location):
            return False, "Location contains invalid characters", location
        
        return True, "Valid location", location
    
    @staticmethod
    def validate_projects(projects_input: List[Dict[str, Any]]) -> Tuple[bool, str, List[Dict[str, Any]]]:
        """
        Validate projects data
        Rules:
        - Optional field (can be empty)
        - Each project: name, description, technologies, year
        - name: 3-100 characters
        - description: 10-500 characters
        - technologies: list of 1-20 technologies
        - year: 2000-current year
        """
        if not projects_input:
            return True, "No projects provided (optional)", []
        
        validated_projects = []
        
        for idx, project in enumerate(projects_input):
            # Create default structure
            proj = {
                'name': project.get('name', ''),
                'description': project.get('description', ''),
                'technologies': project.get('technologies', []),
                'year': project.get('year', '')
            }
            
            # Validate name
            if not proj['name'] or not proj['name'].strip():
                return False, f"Project #{idx+1}: Project name is required", []
            proj['name'] = proj['name'].strip()
            if len(proj['name']) < 3:
                return False, f"Project #{idx+1}: Project name must be at least 3 characters", []
            if len(proj['name']) > 100:
                return False, f"Project #{idx+1}: Project name must not exceed 100 characters", []
            
            # Validate description
            if not proj['description'] or not proj['description'].strip():
                return False, f"Project #{idx+1}: Description is required", []
            proj['description'] = proj['description'].strip()
            if len(proj['description']) < 10:
                return False, f"Project #{idx+1}: Description must be at least 10 characters", []
            if len(proj['description']) > 500:
                return False, f"Project #{idx+1}: Description must not exceed 500 characters", []
            
            # Validate technologies
            if not proj['technologies']:
                return False, f"Project #{idx+1}: At least one technology is required", []
            if isinstance(proj['technologies'], str):
                # Convert comma-separated string to list
                proj['technologies'] = [t.strip() for t in proj['technologies'].split(',') if t.strip()]
            if not isinstance(proj['technologies'], list):
                return False, f"Project #{idx+1}: Technologies must be a list", []
            if len(proj['technologies']) < 1:
                return False, f"Project #{idx+1}: At least one technology is required", []
            if len(proj['technologies']) > 20:
                return False, f"Project #{idx+1}: Maximum 20 technologies allowed", []
            for tech in proj['technologies']:
                if len(tech.strip()) < 2:
                    return False, f"Project #{idx+1}: Technology '{tech}' must be at least 2 characters", []
            
            # Validate year
            if not proj['year']:
                return False, f"Project #{idx+1}: Year is required", []
            try:
                year = int(proj['year'])
                current_year = datetime.now().year
                if year < 2000:
                    return False, f"Project #{idx+1}: Year must be at least 2000 (got {year})", []
                if year > current_year:
                    return False, f"Project #{idx+1}: Year cannot be in the future (got {year})", []
                proj['year'] = str(year)
            except ValueError:
                return False, f"Project #{idx+1}: Year must be a valid number", []
            
            validated_projects.append(proj)
        
        return True, f"Valid projects data ({len(validated_projects)} projects)", validated_projects


def get_user_input():
    """
    Collect all user input from terminal with validation
    """
    print("\n" + "="*60)
    print("APPLICANT DATA VALIDATION SYSTEM")
    print("="*60)
    print("\nPlease enter the applicant details:")
    print("-"*60)
    
    # Store all input data
    data = {}
    validation_results = {}
    all_valid = True
    
    # 1. Name
    print("\n1. NAME")
    print("   Rules: Required, 2-100 chars, letters/spaces/hyphens/apostrophes only")
    name = input("   Enter full name: ").strip()
    valid, msg, cleaned = ApplicantValidator.validate_name(name)
    validation_results['name'] = {'valid': valid, 'message': msg, 'value': cleaned}
    data['name'] = cleaned
    if not valid:
        all_valid = False
        print(f"   ❌ {msg}")
    else:
        print(f"   ✅ {msg}")
    
    # 2. Email
    print("\n2. EMAIL")
    print("   Rules: Required, valid email format (user@domain.com)")
    email = input("   Enter email address: ").strip()
    valid, msg, cleaned = ApplicantValidator.validate_email(email)
    validation_results['email'] = {'valid': valid, 'message': msg, 'value': cleaned}
    data['email'] = cleaned
    if not valid:
        all_valid = False
        print(f"   ❌ {msg}")
    else:
        print(f"   ✅ {msg}")
    
    # 3. Password
    print("\n3. PASSWORD")
    print("   Rules: Required, 8-50 chars, uppercase, lowercase, number, special char")
    password = input("   Enter password: ").strip()
    valid, msg, cleaned = ApplicantValidator.validate_password(password)
    validation_results['password'] = {'valid': valid, 'message': msg, 'value': '***HIDDEN***'}
    data['password'] = cleaned
    if not valid:
        all_valid = False
        print(f"   ❌ {msg}")
    else:
        print(f"   ✅ {msg}")
    
    # 4. Phone
    print("\n4. PHONE NUMBER")
    print("   Rules: Required, 10-15 digits (can include +, -, spaces, parentheses, dots)")
    phone = input("   Enter phone number: ").strip()
    valid, msg, cleaned = ApplicantValidator.validate_phone(phone)
    validation_results['phone'] = {'valid': valid, 'message': msg, 'value': cleaned}
    data['phone'] = cleaned
    if not valid:
        all_valid = False
        print(f"   ❌ {msg}")
    else:
        print(f"   ✅ {msg}")
    
    # 5. Skills
    print("\n5. SKILLS")
    print("   Rules: Required, 1-20 skills, 2-50 chars each (comma-separated)")
    print("   Example: Python, Java, SQL, JavaScript")
    skills_input = input("   Enter skills (comma-separated): ").strip()
    valid, msg, cleaned = ApplicantValidator.validate_skills(skills_input)
    validation_results['skills'] = {'valid': valid, 'message': msg, 'value': cleaned}
    data['skills'] = cleaned
    if not valid:
        all_valid = False
        print(f"   ❌ {msg}")
    else:
        print(f"   ✅ {msg}")
    
    # 6. Education
    print("\n6. EDUCATION")
    print("   Rules: Required fields - level, institution, field_of_study, graduation_year")
    print(f"   Valid levels: {', '.join(ApplicantValidator.VALID_EDUCATION_LEVELS)}")
    
    education = {}
    level = input("   Education level: ").strip()
    institution = input("   Institution name: ").strip()
    field_of_study = input("   Field of study: ").strip()
    grad_year = input("   Graduation year (YYYY): ").strip()
    
    education_input = {
        'level': level,
        'institution': institution,
        'field_of_study': field_of_study,
        'graduation_year': grad_year
    }
    
    valid, msg, cleaned = ApplicantValidator.validate_education(education_input)
    validation_results['education'] = {'valid': valid, 'message': msg, 'value': cleaned}
    data['education'] = cleaned
    if not valid:
        all_valid = False
        print(f"   ❌ {msg}")
    else:
        print(f"   ✅ {msg}")
    
    # 7. Experience
    print("\n7. EXPERIENCE")
    print("   Rules: Required, at least 1 experience")
    print("   Each experience: company, title, start_date, end_date (or current)")
    
    experiences = []
    more_experience = True
    exp_count = 0
    
    while more_experience:
        exp_count += 1
        print(f"\n   --- Experience #{exp_count} ---")
        company = input("   Company name: ").strip()
        title = input("   Job title: ").strip()
        start_date = input("   Start date (YYYY-MM-DD): ").strip()
        current = input("   Current position? (yes/no): ").strip().lower() == 'yes'
        end_date = None
        if not current:
            end_date = input("   End date (YYYY-MM-DD): ").strip()
        
        experiences.append({
            'company': company,
            'title': title,
            'start_date': start_date,
            'end_date': end_date,
            'current': current
        })
        
        more = input("   Add another experience? (yes/no): ").strip().lower() == 'yes'
        more_experience = more
    
    valid, msg, cleaned = ApplicantValidator.validate_experience(experiences)
    validation_results['experience'] = {'valid': valid, 'message': msg, 'value': cleaned}
    data['experience'] = cleaned
    if not valid:
        all_valid = False
        print(f"   ❌ {msg}")
    else:
        print(f"   ✅ {msg}")
    
    # 8. Job Role
    print("\n8. JOB ROLE")
    print("   Rules: Required, 2-100 characters")
    job_role = input("   Enter job role: ").strip()
    valid, msg, cleaned = ApplicantValidator.validate_job_role(job_role)
    validation_results['job_role'] = {'valid': valid, 'message': msg, 'value': cleaned}
    data['job_role'] = cleaned
    if not valid:
        all_valid = False
        print(f"   ❌ {msg}")
    else:
        print(f"   ✅ {msg}")
    
    # 9. Location
    print("\n9. LOCATION")
    print("   Rules: Required, 2-100 characters, letters/numbers/spaces/commas/hyphens/periods")
    location = input("   Enter location: ").strip()
    valid, msg, cleaned = ApplicantValidator.validate_location(location)
    validation_results['location'] = {'valid': valid, 'message': msg, 'value': cleaned}
    data['location'] = cleaned
    if not valid:
        all_valid = False
        print(f"   ❌ {msg}")
    else:
        print(f"   ✅ {msg}")
    
    # 10. Projects (Optional)
    print("\n10. PROJECTS (Optional)")
    print("    Rules: Optional, each project: name, description, technologies, year")
    print("    Technologies: comma-separated list")
    
    projects = []
    add_projects = input("    Add projects? (yes/no): ").strip().lower() == 'yes'
    
    if add_projects:
        more_projects = True
        proj_count = 0
        
        while more_projects:
            proj_count += 1
            print(f"\n    --- Project #{proj_count} ---")
            proj_name = input("    Project name: ").strip()
            proj_desc = input("    Description: ").strip()
            proj_tech = input("    Technologies (comma-separated): ").strip()
            proj_year = input("    Year (YYYY): ").strip()
            
            projects.append({
                'name': proj_name,
                'description': proj_desc,
                'technologies': proj_tech,
                'year': proj_year
            })
            
            more = input("    Add another project? (yes/no): ").strip().lower() == 'yes'
            more_projects = more
    
    valid, msg, cleaned = ApplicantValidator.validate_projects(projects)
    validation_results['projects'] = {'valid': valid, 'message': msg, 'value': cleaned}
    data['projects'] = cleaned
    if not valid:
        all_valid = False
        print(f"   ❌ {msg}")
    else:
        print(f"   ✅ {msg}")
    
    return data, validation_results, all_valid


def display_validation_summary(data: Dict, validation_results: Dict, all_valid: bool):
    """
    Display comprehensive validation summary
    """
    print("\n" + "="*60)
    print("VALIDATION SUMMARY")
    print("="*60)
    
    # Display validation results for each field
    print("\n📋 FIELD VALIDATION RESULTS:")
    print("-"*60)
    
    for field, result in validation_results.items():
        status = "✅" if result['valid'] else "❌"
        print(f"{status} {field.upper()}: {result['message']}")
        if not result['valid']:
            print(f"   Value received: '{result['value'] if result['value'] else 'EMPTY'}'")
    
    # Display all valid data
    if all_valid:
        print("\n" + "="*60)
        print("✅ ALL DATA VALIDATED SUCCESSFULLY!")
        print("="*60)
        
        print("\n📊 COLLECTED DATA:")
        print("-"*60)
        
        # Display each field with its value
        for field, value in data.items():
            if field == 'password':
                print(f"   {field}: ********")
            elif field == 'education':
                print(f"\n   {field.upper()}:")
                if value:
                    for key, val in value.items():
                        print(f"      {key}: {val}")
            elif field == 'experience':
                print(f"\n   {field.upper()}:")
                if value:
                    for idx, exp in enumerate(value, 1):
                        print(f"      Experience #{idx}:")
                        for key, val in exp.items():
                            if key == 'current' and val:
                                print(f"         {key}: Yes (Current Position)")
                            elif key == 'end_date' and not val:
                                print(f"         {key}: N/A (Current position)")
                            else:
                                print(f"         {key}: {val}")
            elif field == 'projects':
                print(f"\n   {field.upper()}:")
                if value:
                    for idx, proj in enumerate(value, 1):
                        print(f"      Project #{idx}:")
                        for key, val in proj.items():
                            print(f"         {key}: {val}")
                else:
                    print("      No projects provided")
            elif field == 'skills':
                print(f"\n   {field.upper()}:")
                if value:
                    for skill in value:
                        print(f"      • {skill}")
                else:
                    print("      No skills provided")
            else:
                print(f"   {field}: {value}")
        
        print("\n" + "="*60)
        print("✨ DATA IS READY FOR SUBMISSION!")
        print("="*60)
        
        return True
    else:
        print("\n" + "="*60)
        print("❌ VALIDATION FAILED!")
        print("="*60)
        print("\nPlease correct the following issues:")
        for field, result in validation_results.items():
            if not result['valid']:
                print(f"   • {field.upper()}: {result['message']}")
        
        print("\n🔄 Please run the program again with correct data.")
        return False


def main():
    """
    Main function to run the validation system
    """
    try:
        # Display welcome banner
        print("\n" + "█"*60)
        print("█" + " " * 58 + "█")
        print("█     APPLICANT DATA VALIDATION SYSTEM v1.0     █")
        print("█" + " " * 58 + "█")
        print("█"*60)
        
        # Get and validate user input
        data, validation_results, all_valid = get_user_input()
        
        # Display summary
        display_validation_summary(data, validation_results, all_valid)
        
        # Return the data for further use if needed
        return data, validation_results, all_valid
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Process interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ An error occurred: {str(e)}")
        sys.exit(1)


# Sample test data for testing the validation functions
def run_test_cases():
    """
    Run sample test cases to demonstrate validation
    """
    print("\n" + "="*60)
    print("RUNNING SAMPLE TEST CASES")
    print("="*60)
    
    validator = ApplicantValidator()
    
    test_cases = [
        # (function, input_value, expected_valid)
        (validator.validate_name, "John Doe", True),
        (validator.validate_name, "J", False),
        (validator.validate_name, "John123", False),
        
        (validator.validate_email, "test@example.com", True),
        (validator.validate_email, "invalid-email", False),
        (validator.validate_email, "test@.com", False),
        
        (validator.validate_password, "Strong@123", True),
        (validator.validate_password, "weak", False),
        (validator.validate_password, "NoSpecial1", False),
        
        (validator.validate_phone, "+1234567890", True),
        (validator.validate_phone, "123", False),
        (validator.validate_phone, "123-456-7890", True),
        
        (validator.validate_skills, "Python, Java, SQL", True),
        (validator.validate_skills, "", False),
        
        (validator.validate_job_role, "Software Engineer", True),
        (validator.validate_job_role, "", False),
        
        (validator.validate_location, "San Francisco, CA", True),
        (validator.validate_location, "NY", True),
        (validator.validate_location, "", False),
    ]
    
    passed = 0
    failed = 0
    
    for func, input_val, expected in test_cases:
        valid, msg, _ = func(input_val)
        if valid == expected:
            print(f"✅ PASS: {func.__name__}({input_val}) -> {msg}")
            passed += 1
        else:
            print(f"❌ FAIL: {func.__name__}({input_val}) -> Expected {expected}, Got {valid}")
            failed += 1
    
    print(f"\nTest Results: {passed} passed, {failed} failed")
    return passed, failed


if __name__ == "__main__":
    # Run the main validation system
    main()
    
    # Uncomment the line below to run test cases instead
    # run_test_cases()