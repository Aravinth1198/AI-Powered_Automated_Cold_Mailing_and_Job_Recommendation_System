import tkinter as tk
from tkinter import messagebox
import pandas as pd
import os

class RegisterPage(tk.Frame):
    """
    A dedicated 'Create Account' screen. Previously registration reused the
    Login page's own email/password boxes, so clicking "New User? Create
    Account" before typing anything just showed an error and looked broken.
    This is a proper, separate form so the flow is unambiguous.
    """
    def __init__(self, parent, on_register_success, on_back_to_login):
        super().__init__(parent, bg='#f0f0f0')
        self.on_register_success = on_register_success
        self.on_back_to_login = on_back_to_login
        self.setup_ui()

    def setup_ui(self):
        header_frame = tk.Frame(self, bg='#2c3e50', height=200)
        header_frame.pack(fill="x")

        tk.Label(
            header_frame,
            text="Create Your Account",
            font=("Arial", 28, "bold"),
            bg='#2c3e50',
            fg='white'
        ).pack(pady=30)

        tk.Label(
            header_frame,
            text="Join JobMatch AI in a few seconds",
            font=("Arial", 14),
            bg='#2c3e50',
            fg='#ecf0f1'
        ).pack()

        form_frame = tk.Frame(self, bg='#f0f0f0')
        form_frame.pack(pady=50, padx=100)

        tk.Label(form_frame, text="Email Address:", font=("Arial", 12), bg='#f0f0f0').pack(anchor="w", pady=(10, 5))
        self.email_entry = tk.Entry(form_frame, font=("Arial", 12), width=35, relief="solid")
        self.email_entry.pack(pady=5)

        tk.Label(form_frame, text="Password:", font=("Arial", 12), bg='#f0f0f0').pack(anchor="w", pady=(10, 5))
        self.password_entry = tk.Entry(form_frame, font=("Arial", 12), width=35, show="•", relief="solid")
        self.password_entry.pack(pady=5)

        tk.Label(form_frame, text="Confirm Password:", font=("Arial", 12), bg='#f0f0f0').pack(anchor="w", pady=(10, 5))
        self.confirm_entry = tk.Entry(form_frame, font=("Arial", 12), width=35, show="•", relief="solid")
        self.confirm_entry.pack(pady=5)

        register_button = tk.Button(
            form_frame,
            text="Register",
            font=("Arial", 14, "bold"),
            bg='#27ae60',
            fg='white',
            command=self.handle_register,
            cursor="hand2",
            padx=20,
            pady=5
        )
        register_button.pack(pady=20)

        back_button = tk.Button(
            form_frame,
            text="\u2190 Back to Login",
            font=("Arial", 11),
            bg='#f0f0f0',
            fg='#3498db',
            command=self.on_back_to_login,
            cursor="hand2",
            relief="flat"
        )
        back_button.pack()

    def handle_register(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get()
        confirm = self.confirm_entry.get()

        if not email or not password or not confirm:
            messagebox.showerror("Error", "Please fill in all fields")
            return

        if '@' not in email or '.' not in email.split('@')[-1]:
            messagebox.showerror("Error", "Please enter a valid email address")
            return

        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match")
            return

        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters")
            return

        user_data = self.save_new_user(email, password)
        if user_data is not None:
            messagebox.showinfo("Success", "Account created! Taking you to your profile now.")
            self.on_register_success(user_data)

    def save_new_user(self, email, password):
        """Save the new account to users.xlsx. Returns the new user's row as a dict, or None on failure."""
        users_file = 'data/users.xlsx'

        if os.path.exists(users_file):
            existing = pd.read_excel(users_file)
            if email in existing.get('email', pd.Series(dtype=str)).values:
                messagebox.showerror("Error", "An account with this email already exists. Please login instead.")
                return None

        new_user_row = {
            'email': email,
            'password': password,
            'first_name': '',
            'last_name': '',
            'profession': '',
            'experience': 0,
            'preferred_domain_1': '',
            'preferred_domain_2': '',
            'preferred_domain_3': '',
            'skills': '',
            'location': '',
            'education_raw': '',
            'work_experience_raw': '',
            'projects_raw': ''
        }
        new_user = pd.DataFrame({k: [v] for k, v in new_user_row.items()})

        if os.path.exists(users_file):
            df = pd.read_excel(users_file)
            for col in new_user_row:
                if col not in df.columns:
                    df[col] = '' if col not in ('experience',) else 0
            df = pd.concat([df, new_user], ignore_index=True)
        else:
            os.makedirs('data', exist_ok=True)
            df = new_user

        df.to_excel(users_file, index=False)
        return new_user_row
