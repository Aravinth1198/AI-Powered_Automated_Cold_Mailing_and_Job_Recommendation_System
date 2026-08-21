import tkinter as tk
from ui.login_page import LoginPage
from ui.dashboard import DashboardPage
from ui.job_matching import JobMatchingPage

class MainApplication:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Job Application System")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Container frame
        self.container = tk.Frame(self.root)
        self.container.pack(fill="both", expand=True)
        
        # Dictionary to hold pages
        self.frames = {}
        
        # Initialize pages
        self.current_user = None
        self.current_jobs = None
        
        self.show_login_page()
    
    def show_login_page(self):
        """Show Page 1 - Welcome/Login"""
        if hasattr(self, 'current_frame'):
            self.current_frame.destroy()
        
        self.current_frame = LoginPage(self.container, self.on_login_success)
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