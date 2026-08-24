import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os

class DashboardPage(tk.Frame):
    def __init__(self, parent, user_data, on_profile_complete, on_logout):
        super().__init__(parent, bg='#f0f0f0')
        self.user_data = user_data
        self.on_profile_complete = on_profile_complete
        self.on_logout = on_logout
        
        # Check if profile is complete
        self.profile_complete = self.check_profile_complete()
        
        self.setup_ui()
    
    def check_profile_complete(self):
        """Check if user profile has all required fields"""
        required_fields = ['first_name', 'last_name', 'profession', 'skills', 'location']
        
        for field in required_fields:
            value = self.user_data.get(field, '')
            if not value or (isinstance(value, float) and pd.isna(value)):
                return False
        
        # Check preferred domains
        for i in range(1, 4):
            field = f'preferred_domain_{i}'
            value = self.user_data.get(field, '')
            if not value or (isinstance(value, float) and pd.isna(value)):
                return False
        
        return True
    
    def setup_ui(self):
        # Header
        header_frame = tk.Frame(self, bg='#2c3e50', height=100)
        header_frame.pack(fill="x")
        
        tk.Label(
            header_frame,
            text="User Dashboard",
            font=("Arial", 24, "bold"),
            bg='#2c3e50',
            fg='white'
        ).pack(side="left", padx=30, pady=25)
        
        # Logout button
        logout_btn = tk.Button(
            header_frame,
            text="Logout",
            font=("Arial", 11),
            bg='#e74c3c',
            fg='white',
            command=self.on_logout,
            cursor="hand2"
        )
        logout_btn.pack(side="right", padx=30)
        
        if not self.profile_complete:
            self.show_profile_form()
        else:
            self.show_user_details()
    
    def show_user_details(self):
        """Display user details"""
        details_frame = tk.Frame(self, bg='#f0f0f0')
        details_frame.pack(pady=30, padx=50, fill="both", expand=True)
        
        tk.Label(
            details_frame,
            text="Your Profile Information",
            font=("Arial", 18, "bold"),
            bg='#f0f0f0'
        ).pack(pady=20)
        
        # User info display
        info_frame = tk.Frame(details_frame, bg='white', relief="solid", borderwidth=1)
        info_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Display user information
        fields = [
            ("Name:", f"{self.user_data.get('first_name', '')} {self.user_data.get('last_name', '')}"),
            ("Email:", self.user_data.get('email', '')),
            ("Profession:", self.user_data.get('profession', '')),
        ]
        
        # Add experience if working professional
        if self.user_data.get('profession') == 'Working Professional':
            fields.append(("Experience:", f"{self.user_data.get('experience', 0)} years"))
        
        # Add preferred domains
        fields.append(("Preferred Domains:", ""))
        
        row = 0
        for label, value in fields:
            if label == "Preferred Domains:":
                tk.Label(
                    info_frame,
                    text=label,
                    font=("Arial", 12, "bold"),
                    bg='white'
                ).grid(row=row, column=0, sticky="w", padx=20, pady=10)
                
                domains = [
                    self.user_data.get('preferred_domain_1', ''),
                    self.user_data.get('preferred_domain_2', ''),
                    self.user_data.get('preferred_domain_3', '')
                ]
                domain_text = ", ".join([d for d in domains if d])
                
                tk.Label(
                    info_frame,
                    text=domain_text,
                    font=("Arial", 12),
                    bg='white'
                ).grid(row=row, column=1, sticky="w", padx=20, pady=10)
            else:
                tk.Label(
                    info_frame,
                    text=label,
                    font=("Arial", 12, "bold"),
                    bg='white'
                ).grid(row=row, column=0, sticky="w", padx=20, pady=10)
                
                tk.Label(
                    info_frame,
                    text=value,
                    font=("Arial", 12),
                    bg='white'
                ).grid(row=row, column=1, sticky="w", padx=20, pady=10)
            
            row += 1
        
        # Skills display
        tk.Label(
            info_frame,
            text="Skills:",
            font=("Arial", 12, "bold"),
            bg='white'
        ).grid(row=row, column=0, sticky="w", padx=20, pady=10)
        
        skills_text = tk.Text(info_frame, height=5, width=50, font=("Arial", 12))
        skills_text.insert("1.0", self.user_data.get('skills', ''))
        skills_text.config(state="disabled")
        skills_text.grid(row=row, column=1, sticky="w", padx=20, pady=10)
        
        row += 1
        
        # Find Jobs button - FIX: Use lambda to pass user_data
        find_jobs_btn = tk.Button(
            details_frame,
            text="Find Matching Jobs",
            font=("Arial", 14, "bold"),
            bg='#27ae60',
            fg='white',
            command=lambda: self.on_profile_complete(self.user_data),  # FIXED
            cursor="hand2",
            padx=30,
            pady=10
        )
        find_jobs_btn.pack(pady=30)
    
    def show_profile_form(self):
        """Show profile completion form"""
        form_frame = tk.Frame(self, bg='#f0f0f0')
        form_frame.pack(pady=20, padx=50, fill="both", expand=True)
        
        tk.Label(
            form_frame,
            text="Complete Your Profile",
            font=("Arial", 18, "bold"),
            bg='#f0f0f0'
        ).pack(pady=10)
        
        tk.Label(
            form_frame,
            text="Please fill in the following information to get job recommendations",
            font=("Arial", 11),
            bg='#f0f0f0',
            fg='#7f8c8d'
        ).pack(pady=5)
        
        # Create scrollable form
        canvas = tk.Canvas(form_frame, bg='#f0f0f0')
        scrollbar = ttk.Scrollbar(form_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f0f0f0')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # First Name
        tk.Label(scrollable_frame, text="First Name:", bg='#f0f0f0', font=("Arial", 11)).pack(anchor="w", pady=5)
        self.first_name_entry = tk.Entry(scrollable_frame, font=("Arial", 11), width=40)
        self.first_name_entry.pack(pady=5)
        
        # Last Name
        tk.Label(scrollable_frame, text="Last Name:", bg='#f0f0f0', font=("Arial", 11)).pack(anchor="w", pady=5)
        self.last_name_entry = tk.Entry(scrollable_frame, font=("Arial", 11), width=40)
        self.last_name_entry.pack(pady=5)
        
        # Profession
        tk.Label(scrollable_frame, text="Profession:", bg='#f0f0f0', font=("Arial", 11)).pack(anchor="w", pady=5)
        self.profession_var = tk.StringVar(value="Student")
        profession_options = ["Working Professional", "Student", "Recent Graduate"]
        self.profession_combo = ttk.Combobox(
            scrollable_frame, 
            textvariable=self.profession_var,
            values=profession_options,
            state="readonly",
            width=37
        )
        self.profession_combo.pack(pady=5)
        self.profession_combo.bind('<<ComboboxSelected>>', self.on_profession_change)
        
        # Experience (only for working professionals)
        self.experience_label = tk.Label(scrollable_frame, text="Experience (years):", bg='#f0f0f0', font=("Arial", 11))
        self.experience_entry = tk.Entry(scrollable_frame, font=("Arial", 11), width=40)
        
        # Preferred Domains
        tk.Label(scrollable_frame, text="Preferred Domain 1:", bg='#f0f0f0', font=("Arial", 11)).pack(anchor="w", pady=5)
        self.domain1_entry = tk.Entry(scrollable_frame, font=("Arial", 11), width=40)
        self.domain1_entry.pack(pady=5)
        
        tk.Label(scrollable_frame, text="Preferred Domain 2:", bg='#f0f0f0', font=("Arial", 11)).pack(anchor="w", pady=5)
        self.domain2_entry = tk.Entry(scrollable_frame, font=("Arial", 11), width=40)
        self.domain2_entry.pack(pady=5)
        
        tk.Label(scrollable_frame, text="Preferred Domain 3:", bg='#f0f0f0', font=("Arial", 11)).pack(anchor="w", pady=5)
        self.domain3_entry = tk.Entry(scrollable_frame, font=("Arial", 11), width=40)
        self.domain3_entry.pack(pady=5)
        
        # Skills
        tk.Label(scrollable_frame, text="Skills (comma-separated):", bg='#f0f0f0', font=("Arial", 11)).pack(anchor="w", pady=5)
        self.skills_text = tk.Text(scrollable_frame, height=5, width=40, font=("Arial", 11))
        self.skills_text.pack(pady=5)
        
        # Location — needed on the resume header
        tk.Label(scrollable_frame, text="Location (City, State):", bg='#f0f0f0', font=("Arial", 11)).pack(anchor="w", pady=5)
        self.location_entry = tk.Entry(scrollable_frame, font=("Arial", 11), width=40)
        self.location_entry.pack(pady=5)
        
        # Education — one line per entry, feeds the resume's Education section
        tk.Label(scrollable_frame, text="Education (one per line):", bg='#f0f0f0', font=("Arial", 11)).pack(anchor="w", pady=5)
        tk.Label(
            scrollable_frame,
            text="Format: Institution ; Location ; Degree ; Start - End",
            bg='#f0f0f0', fg='#7f8c8d', font=("Arial", 9)
        ).pack(anchor="w")
        self.education_text = tk.Text(scrollable_frame, height=3, width=60, font=("Arial", 10))
        self.education_text.pack(pady=5)
        
        # Work experience — one line per entry, feeds the resume's Experience section
        tk.Label(scrollable_frame, text="Work Experience (one per line):", bg='#f0f0f0', font=("Arial", 11)).pack(anchor="w", pady=5)
        tk.Label(
            scrollable_frame,
            text="Format: Company ; Location ; Role ; Start - End ; bullet one | bullet two",
            bg='#f0f0f0', fg='#7f8c8d', font=("Arial", 9)
        ).pack(anchor="w")
        self.work_experience_text = tk.Text(scrollable_frame, height=4, width=60, font=("Arial", 10))
        self.work_experience_text.pack(pady=5)
        
        # Projects — one line per entry, feeds the resume's Projects section
        tk.Label(scrollable_frame, text="Projects (one per line):", bg='#f0f0f0', font=("Arial", 11)).pack(anchor="w", pady=5)
        tk.Label(
            scrollable_frame,
            text="Format: Project Title ; Tech Stack (comma-separated) ; Start - End ; bullet one | bullet two",
            bg='#f0f0f0', fg='#7f8c8d', font=("Arial", 9)
        ).pack(anchor="w")
        self.projects_text = tk.Text(scrollable_frame, height=4, width=60, font=("Arial", 10))
        self.projects_text.pack(pady=5)
        
        # Save button - FIX: Use lambda to pass user_data
        save_btn = tk.Button(
            scrollable_frame,
            text="Save Profile",
            font=("Arial", 12, "bold"),
            bg='#27ae60',
            fg='white',
            command=self.save_profile,
            cursor="hand2",
            padx=20,
            pady=5
        )
        save_btn.pack(pady=20)
    
    def on_profession_change(self, event=None):
        """Show/hide experience field based on profession"""
        if self.profession_var.get() == "Working Professional":
            self.experience_label.pack(anchor="w", pady=5)
            self.experience_entry.pack(pady=5)
        else:
            self.experience_label.pack_forget()
            self.experience_entry.pack_forget()
    
    def save_profile(self):
        """Save user profile to Excel"""
        # Validate inputs
        first_name = self.first_name_entry.get().strip()
        last_name = self.last_name_entry.get().strip()
        profession = self.profession_var.get()
        experience = self.experience_entry.get().strip() if profession == "Working Professional" else "0"
        domain1 = self.domain1_entry.get().strip()
        domain2 = self.domain2_entry.get().strip()
        domain3 = self.domain3_entry.get().strip()
        skills = self.skills_text.get("1.0", tk.END).strip()
        
        # NEW: resume fields — location is required, the multi-line boxes
        # (education/work experience/projects) are optional so a Student
        # profile with no job history yet can still save.
        location = self.location_entry.get().strip()
        education_raw = self.education_text.get("1.0", tk.END).strip()
        work_experience_raw = self.work_experience_text.get("1.0", tk.END).strip()
        projects_raw = self.projects_text.get("1.0", tk.END).strip()
        
        if not all([first_name, last_name, domain1, domain2, domain3, skills, location]):
            messagebox.showerror("Error", "Please fill in all fields, including Location")
            return
        
        # Update user data
        self.user_data['first_name'] = first_name
        self.user_data['last_name'] = last_name
        self.user_data['profession'] = profession
        self.user_data['experience'] = float(experience) if experience else 0
        self.user_data['preferred_domain_1'] = domain1
        self.user_data['preferred_domain_2'] = domain2
        self.user_data['preferred_domain_3'] = domain3
        self.user_data['skills'] = skills
        self.user_data['location'] = location
        self.user_data['education_raw'] = education_raw
        self.user_data['work_experience_raw'] = work_experience_raw
        self.user_data['projects_raw'] = projects_raw
        
        # Save to Excel
        users_file = 'data/users.xlsx'
        df = pd.read_excel(users_file)
        
        # BUG FIX / SCHEMA UPGRADE: older users.xlsx files won't have these
        # columns yet. Add them if missing so .loc[] assignment below doesn't
        # raise a KeyError on a file generated before this change.
        for col in ['location', 'education_raw', 'work_experience_raw', 'projects_raw']:
            if col not in df.columns:
                df[col] = ''
        
        # Update the specific user
        email = self.user_data['email']
        df.loc[df['email'] == email, 'first_name'] = first_name
        df.loc[df['email'] == email, 'last_name'] = last_name
        df.loc[df['email'] == email, 'profession'] = profession
        df.loc[df['email'] == email, 'experience'] = float(experience) if experience else 0
        df.loc[df['email'] == email, 'preferred_domain_1'] = domain1
        df.loc[df['email'] == email, 'preferred_domain_2'] = domain2
        df.loc[df['email'] == email, 'preferred_domain_3'] = domain3
        df.loc[df['email'] == email, 'skills'] = skills
        df.loc[df['email'] == email, 'location'] = location
        df.loc[df['email'] == email, 'education_raw'] = education_raw
        df.loc[df['email'] == email, 'work_experience_raw'] = work_experience_raw
        df.loc[df['email'] == email, 'projects_raw'] = projects_raw
        
        df.to_excel(users_file, index=False)
        
        messagebox.showinfo("Success", "Profile saved successfully!")
        
        # Trigger job matching - FIX: Pass user_data
        self.on_profile_complete(self.user_data)  # This is already correct