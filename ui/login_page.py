import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os

class LoginPage(tk.Frame):
    def __init__(self, parent, on_login_success):
        super().__init__(parent, bg='#f0f0f0')
        self.on_login_success = on_login_success
        self.setup_ui()
    
    def setup_ui(self):
        # Welcome Screen
        welcome_frame = tk.Frame(self, bg='#2c3e50', height=200)
        welcome_frame.pack(fill="x")
        
        tk.Label(
            welcome_frame,
            text="Welcome to JobMatch AI",
            font=("Arial", 28, "bold"),
            bg='#2c3e50',
            fg='white'
        ).pack(pady=30)
        
        tk.Label(
            welcome_frame,
            text="Your AI-Powered Job Application Assistant",
            font=("Arial", 14),
            bg='#2c3e50',
            fg='#ecf0f1'
        ).pack()
        
        # Login Form
        login_frame = tk.Frame(self, bg='#f0f0f0')
        login_frame.pack(pady=50, padx=100)
        
        tk.Label(
            login_frame,
            text="Login to Your Account",
            font=("Arial", 18, "bold"),
            bg='#f0f0f0'
        ).pack(pady=20)
        
        # Email
        tk.Label(
            login_frame,
            text="Email Address:",
            font=("Arial", 12),
            bg='#f0f0f0'
        ).pack(anchor="w", pady=(10, 5))
        
        self.email_entry = tk.Entry(
            login_frame,
            font=("Arial", 12),
            width=35,
            relief="solid"
        )
        self.email_entry.pack(pady=5)
        
        # Password
        tk.Label(
            login_frame,
            text="Password:",
            font=("Arial", 12),
            bg='#f0f0f0'
        ).pack(anchor="w", pady=(10, 5))
        
        self.password_entry = tk.Entry(
            login_frame,
            font=("Arial", 12),
            width=35,
            show="•",
            relief="solid"
        )
        self.password_entry.pack(pady=5)
        
        # Login Button
        login_button = tk.Button(
            login_frame,
            text="Login",
            font=("Arial", 14, "bold"),
            bg='#3498db',
            fg='white',
            command=self.handle_login,
            cursor="hand2",
            padx=20,
            pady=5
        )
        login_button.pack(pady=20)
        
        # New User Button
        new_user_button = tk.Button(
            login_frame,
            text="New User? Create Account",
            font=("Arial", 11),
            bg='#f0f0f0',
            fg='#3498db',
            command=self.handle_new_user,
            cursor="hand2",
            relief="flat"
        )
        new_user_button.pack()
    
    def handle_login(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get()
        
        if not email or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        # Check if user exists
        users_file = 'data/users.xlsx'
        if os.path.exists(users_file):
            df = pd.read_excel(users_file)
            user = df[(df['email'] == email) & (df['password'] == password)]
            
            if not user.empty:
                user_data = user.iloc[0].to_dict()
                self.on_login_success(user_data)
                return
        
        messagebox.showerror("Error", "Invalid email or password")
    
    def handle_new_user(self):
        """Open registration form"""
        self.clear_fields()
        # Change button texts for registration
        messagebox.showinfo("Registration", "Please enter your email and password to register")
        
        # Here you would implement registration logic
        # For simplicity, we'll just collect email and password
        email = self.email_entry.get().strip()
        password = self.password_entry.get()
        
        if email and password:
            self.save_new_user(email, password)
    
    def save_new_user(self, email, password):
        """Save new user to Excel"""
        users_file = 'data/users.xlsx'
        
        new_user = pd.DataFrame({
            'email': [email],
            'password': [password],
            'first_name': [''],
            'last_name': [''],
            'profession': [''],
            'experience': [0],
            'preferred_domain_1': [''],
            'preferred_domain_2': [''],
            'preferred_domain_3': [''],
            'skills': ['']
        })
        
        if os.path.exists(users_file):
            df = pd.read_excel(users_file)
            df = pd.concat([df, new_user], ignore_index=True)
        else:
            os.makedirs('data', exist_ok=True)
            df = new_user
        
        df.to_excel(users_file, index=False)
        messagebox.showinfo("Success", "Account created! Please login now.")
    
    def clear_fields(self):
        self.email_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)