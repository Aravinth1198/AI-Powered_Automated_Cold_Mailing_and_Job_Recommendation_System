import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os
import sys
import json

# Add project root AND the n8n/ folder to the Python path.
# BUG FIX: the original code did `from n8n_helper import send_to_n8n`
# with no sys.path entry pointing at the n8n/ directory, so this import
# always raised ModuleNotFoundError and the whole Job Matching page
# crashed before it could even display results.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)
sys.path.append(os.path.join(PROJECT_ROOT, 'n8n'))

from models.prediction_service import PredictionService
from n8n_helper import send_to_n8n

class JobMatchingPage(tk.Frame):
    def __init__(self, parent, user_data, on_back):
        super().__init__(parent, bg='#f0f0f0')
        self.user_data = user_data
        self.on_back = on_back
        self.prediction_service = PredictionService()
        
        self.setup_ui()
        self.load_matching_jobs()
    
    def setup_ui(self):
        # Header
        header_frame = tk.Frame(self, bg='#2c3e50', height=100)
        header_frame.pack(fill="x")
        
        tk.Label(
            header_frame,
            text="Matching Jobs",
            font=("Arial", 24, "bold"),
            bg='#2c3e50',
            fg='white'
        ).pack(side="left", padx=30, pady=25)
        
        # Back button
        back_btn = tk.Button(
            header_frame,
            text="← Back",
            font=("Arial", 11),
            bg='#3498db',
            fg='white',
            command=self.on_back,
            cursor="hand2"
        )
        back_btn.pack(side="right", padx=30)
        
        # Status label
        self.status_label = tk.Label(
            self,
            text="Loading model...",
            font=("Arial", 12),
            bg='#f0f0f0',
            fg='#e67e22'
        )
        self.status_label.pack(pady=10)
        
        # Jobs frame
        self.jobs_frame = tk.Frame(self, bg='#f0f0f0')
        self.jobs_frame.pack(fill="both", expand=True, padx=30, pady=20)

    
    def load_matching_jobs(self):

        """Load matching jobs using the saved model"""
        try:
            # Update status
            self.status_label.config(
            text="Loading jobs data...",
            fg='#e67e22'
            )
            self.update_idletasks()
        
            # Load jobs data
            jobs_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'jobs.xlsx')
        
            if not os.path.exists(jobs_file):
                self.status_label.config(
                text="Jobs data not found!",
                fg='#e74c3c'
                )
                return
        
            jobs_df = pd.read_excel(jobs_file)
        
            # Update status
            self.status_label.config(
            text="Running prediction model...",
            fg='#e67e22'
            )
            self.update_idletasks()
        
        # Get predictions
            matching_jobs = self.prediction_service.predict_jobs(
                 self.user_data,
                 jobs_df,
                 top_n=20
            )
        
            if not matching_jobs.empty:
                self.status_label.config(
                text=f"✓ Found {len(matching_jobs)} matching jobs",
                fg='#27ae60'
            )
            else:
                self.status_label.config(
                text="No matching jobs found for your profile",
                fg='#e67e22'
                )
        
            self.display_jobs(matching_jobs)
            
            # Hand the matched jobs + HR contact info off to n8n, which runs
            # the Gemini content generation, builds the LaTeX PDF, and emails
            # every HR contact in the matched job list.
            if not matching_jobs.empty:
                self.process_with_n8n(matching_jobs)
        
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"Error in load_matching_jobs: {error_details}")
        
            self.status_label.config(
            text=f"Error: {str(e)}",
            fg='#e74c3c'
            )
        
            messagebox.showerror("Error", f"Failed to load matching jobs:\n{str(e)}")
    
    def display_jobs(self, jobs):
        """Display matching jobs"""
        for widget in self.jobs_frame.winfo_children():
            widget.destroy()
        
        if jobs.empty:
            tk.Label(
                self.jobs_frame,
                text="No matching jobs found",
                font=("Arial", 14),
                bg='#f0f0f0'
            ).pack(pady=20)
            return
        
        # Scrollable frame
        canvas = tk.Canvas(self.jobs_frame, bg='#f0f0f0')
        scrollbar = ttk.Scrollbar(self.jobs_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f0f0f0')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Display jobs
        for i, (_, job) in enumerate(jobs.iterrows(), 1):
            job_frame = tk.Frame(scrollable_frame, bg='white', relief="solid", borderwidth=1)
            job_frame.pack(fill="x", padx=20, pady=5)
            
            # Job title and company
            header = tk.Frame(job_frame, bg='white')
            header.pack(fill="x", padx=15, pady=(10, 5))
            
            tk.Label(
                header,
                text=f"{i}. {job.get('job_title', 'N/A')}",
                font=("Arial", 13, "bold"),
                bg='white'
            ).pack(side="left")
            
            match_score = job.get('match_probability', 0) * 100
            tk.Label(
                header,
                text=f"Match: {match_score:.1f}%",
                font=("Arial", 12, "bold"),
                bg='white',
                fg='#27ae60' if match_score > 70 else '#f39c12'
            ).pack(side="right")
            
            tk.Label(
                job_frame,
                text=f"Company: {job.get('company', 'N/A')}",
                font=("Arial", 11),
                bg='white'
            ).pack(anchor="w", padx=15)
            
            tk.Label(
                job_frame,
                text=f"Domain: {job.get('domain', 'N/A')}",
                font=("Arial", 11),
                bg='white',
                fg='#7f8c8d'
            ).pack(anchor="w", padx=15)
            
            # Apply button
            apply_btn = tk.Button(
                job_frame,
                text="Apply Now",
                font=("Arial", 10, "bold"),
                bg='#27ae60',
                fg='white',
                command=lambda j=job: self.apply_to_job(j),
                cursor="hand2"
            )
            apply_btn.pack(anchor="w", padx=15, pady=10)
    
    def apply_to_job(self, job):
        """Apply to a job"""
        messagebox.showinfo(
            "Application Submitted",
            f"Application for {job.get('job_title', 'this position')} "
            f"at {job.get('company', 'the company')} submitted!\n\n"
            f"Match Score: {job.get('match_probability', 0) * 100:.1f}%"
        )

    def process_with_n8n(self, jobs):
        """Send matching jobs + HR contact info to n8n for Gemini/PDF/email processing"""
        if jobs.empty:
            return
        
        # BUG FIX: model_info previously referenced self.best_model_name /
        # self.best_accuracy, which were never set anywhere in this class
        # (AttributeError). Pull the real values from the saved model's
        # metadata file instead, generated by RandomForestJobMatcher.save_model().
        model_info = {'model_name': 'Random Forest', 'accuracy': None}
        metadata_path = os.path.join(PROJECT_ROOT, 'models', 'saved', 'model_metadata.json')
        if os.path.exists(metadata_path):
            try:
                with open(metadata_path, 'r') as f:
                    meta = json.load(f)
                model_info['model_name'] = meta.get('model_type', model_info['model_name'])
                model_info['accuracy'] = meta.get('accuracy', model_info['accuracy'])
            except Exception:
                pass
        
        result = send_to_n8n(
            user_data=self.user_data,
            matching_jobs=jobs,
            model_info=model_info
        )
        
        # BUG FIX: this label was called self.loading_label, which does not
        # exist on this page (only self.status_label was created in setup_ui),
        # so this always raised AttributeError and silently killed the
        # n8n hand-off before the user ever saw a result.
        if result['success']:
            self.status_label.config(
                text="✓ Jobs matched and sent to n8n for HR mailing!",
                fg='#27ae60'
            )
        else:
            self.status_label.config(
                text=f"✗ Failed to send to n8n: {result.get('error')}",
                fg='#e74c3c'
            )
