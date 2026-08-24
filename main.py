import tkinter as tk
from tkinter import messagebox
import os
import sys
import pandas as pd

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ui.login_page import LoginPage
from ui.register_page import RegisterPage
from ui.dashboard import DashboardPage
from ui.job_matching import JobMatchingPage

class MainApplication:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("JobMatch AI - Intelligent Job Application System")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f0f0')
        
        # Container frame
        self.container = tk.Frame(self.root)
        self.container.pack(fill="both", expand=True)
        
        # Initialize variables
        self.current_user = None
        self.current_jobs = None
        
        # Check data files
        self.check_data_files()
        
        # Show login page
        self.show_login_page()
    
    def check_data_files(self):
        """Check if data files exist"""
        data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
        os.makedirs(data_dir, exist_ok=True)
        
        jobs_file = os.path.join(data_dir, 'jobs.xlsx')
        users_file = os.path.join(data_dir, 'users.xlsx')
        
        if not os.path.exists(jobs_file) or not os.path.exists(users_file):
            print("Generating datasets...")
            from generate_datasets import generate_jobs_dataset, generate_users_dataset, generate_training_data
            generate_jobs_dataset()
            generate_users_dataset()
            generate_training_data()
    
    def show_login_page(self):
        """Show Page 1 - Welcome/Login"""
        if hasattr(self, 'current_frame'):
            self.current_frame.destroy()
        
        self.current_frame = LoginPage(self.container, self.on_login_success, self.show_register_page)
        self.current_frame.pack(fill="both", expand=True)
    
    def show_register_page(self):
        """Show the dedicated Create Account screen"""
        if hasattr(self, 'current_frame'):
            self.current_frame.destroy()
        
        self.current_frame = RegisterPage(self.container, self.on_register_success, self.show_login_page)
        self.current_frame.pack(fill="both", expand=True)
    
    def show_dashboard(self, user_data=None):
        """Show Page 2 - Dashboard"""
        if hasattr(self, 'current_frame'):
            self.current_frame.destroy()
        
        self.current_user = user_data
        self.current_frame = DashboardPage(
            self.container, 
            self.current_user,
            self.on_profile_complete,
            self.on_logout
        )
        self.current_frame.pack(fill="both", expand=True)
    
    def show_job_matching(self):
        """Show Page 3 - Job Matching Results"""
        if hasattr(self, 'current_frame'):
            self.current_frame.destroy()
        
        self.current_frame = JobMatchingPage(
            self.container,
            self.current_user,
            self.on_back_to_dashboard
        )
        self.current_frame.pack(fill="both", expand=True)
    
    def on_login_success(self, user_data):
        """Callback when login is successful"""
        self.show_dashboard(user_data)
    
    def on_register_success(self, user_data):
        """Callback when a new account is created — logs the user straight
        in and takes them to their (empty) profile, instead of bouncing
        them back to Login to type everything in again."""
        self.show_dashboard(user_data)
    
    def on_profile_complete(self, user_data):
        """Callback when profile is completed"""
        self.current_user = user_data
        self.show_job_matching()
    
    def on_logout(self):
        """Callback for logout"""
        self.current_user = None
        self.show_login_page()
    
    def on_back_to_dashboard(self):
        """Callback to go back to dashboard"""
        self.show_dashboard(self.current_user)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MainApplication()
    app.run()