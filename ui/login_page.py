import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os

class LoginPage(tk.Frame):
    def __init__(self, parent, on_login_success, on_register_click=None):
        super().__init__(parent, bg='#f0f0f0')
        self.on_login_success = on_login_success
        # BUG FIX: registration now lives on its own screen (ui/register_page.py)
        # instead of silently reusing these login boxes. If a caller doesn't
        # pass on_register_click, fall back to a clear error rather than a
        # silent no-op.
        self.on_register_click = on_register_click or (
            lambda: messagebox.showerror("Error", "Registration is not wired up in main.py")
        )
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
        
        # New User Button — now navigates to a dedicated Register screen
        # instead of reusing these same email/password boxes.
        new_user_button = tk.Button(
            login_frame,
            text="New User? Create Account",
            font=("Arial", 11),
            bg='#f0f0f0',
            fg='#3498db',
            command=self.on_register_click,
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