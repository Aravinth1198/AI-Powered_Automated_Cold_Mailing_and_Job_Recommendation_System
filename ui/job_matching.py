import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os
from models.model_trainer import ModelTrainer
from integration.n8n_integration import N8NIntegration

class JobMatchingPage(tk.Frame):
    def __init__(self, parent, user_data, on_back):
        super().__init__(parent, bg='#f0f0f0')
        self.user_data = user_data
        self.on_back = on_back
        
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
            text="← Back to Dashboard",
            font=("Arial", 11),
            bg='#3498db',
            fg='white',
            command=self.on_back,
            cursor="hand2"
        )
        back_btn.pack(side="right", padx=30)
        
        # Loading indicator
        self.loading_label = tk.Label(
            self,
            text="Finding matching jobs...",
            font=("Arial", 14),
            bg='#f0f0f0'
        )
        self.loading_label.pack(pady=50)
        
        # Jobs frame
        self.jobs_frame = tk.Frame(self, bg='#f0f0f0')
        self.jobs_frame.pack(fill="both", expand=True, padx=30, pady=20)
    
    def load_matching_jobs(self):
        """Load and display matching jobs using ML models"""
        # Use the best model to predict matching jobs
        model_trainer = ModelTrainer()
        
        # Train all models and get the best one
        best_model, best_accuracy, matching_jobs = model_trainer.train_and_predict(
            self.user_data
        )
        
        # Update loading label
        self.loading_label.config(
            text=f"Best Model: {best_model} (Accuracy: {best_accuracy:.2f}%)",
            font=("Arial", 12, "bold"),
            fg='#27ae60'
        )
        
        # Display matching jobs
        self.display_jobs(matching_jobs)
        
        # Send to n8n for processing
        self.process_with_n8n(matching_jobs)
    
    def display_jobs(self, jobs):
        """Display matching jobs in the UI"""
        # Clear previous jobs
        for widget in self.jobs_frame.winfo_children():
            widget.destroy()
        
        if not jobs:
            tk.Label(
                self.jobs_frame,
                text="No matching jobs found",
                font=("Arial", 14),
                bg='#f0f0f0'
            ).pack(pady=20)
            return
        
        tk.Label(
            self.jobs_frame,
            text=f"Found {len(jobs)} matching jobs:",
            font=("Arial", 14, "bold"),
            bg='#f0f0f0'
        ).pack(pady=10)
        
        # Create scrollable frame for jobs
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
        
        # Display each job
        for i, (_, job) in enumerate(jobs.iterrows()):
            job_frame = tk.Frame(
                scrollable_frame,
                bg='white',
                relief="solid",
                borderwidth=1
            )
            job_frame.pack(fill="x", padx=20, pady=5)
            
            # Job title
            tk.Label(
                job_frame,
                text=job.get('job_title', 'N/A'),
                font=("Arial", 13, "bold"),
                bg='white'
            ).pack(anchor="w", padx=15, pady=(10, 5))
            
            # Company
            tk.Label(
                job_frame,
                text=f"Company: {job.get('company', 'N/A')}",
                font=("Arial", 11),
                bg='white'
            ).pack(anchor="w", padx=15)
            
            # Domain
            tk.Label(
                job_frame,
                text=f"Domain: {job.get('domain', 'N/A')}",
                font=("Arial", 11),
                bg='white',
                fg='#7f8c8d'
            ).pack(anchor="w", padx=15)
            
            # Skills match
            tk.Label(
                job_frame,
                text=f"Required Skills: {job.get('required_skills', 'N/A')}",
                font=("Arial", 10),
                bg='white',
                fg='#34495e'
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
        """Apply to a specific job"""
        messagebox.showinfo(
            "Application Submitted",
            f"Your application for {job.get('job_title', 'this position')} "
            f"at {job.get('company', 'the company')} has been submitted!"
        )
    
    def process_with_n8n(self, jobs):
        """Send matching jobs to n8n for processing"""
        if not jobs.empty:
            n8n = N8NIntegration()
            result = n8n.send_to_n8n(self.user_data, jobs)
            
            if result:
                self.loading_label.config(
                    text=f"Applications sent to n8n workflow successfully!",
                    fg='#27ae60'
                )