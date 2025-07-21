import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
from typing import Optional, Dict, Any

class AuthUI:
    def __init__(self, api_base_url: str = "http://localhost:8000"):
        self.api_base_url = api_base_url
        self.root = tk.Tk()
        self.root.title("Spectre AI - Authentication")
        self.root.geometry("400x500")
        self.root.configure(bg='#1a1a2e')
        
        # Variables
        self.username_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.confirm_password_var = tk.StringVar()
        
        self.user_data: Optional[Dict[str, Any]] = None
        self.access_token: Optional[str] = None
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg='#1a1a2e')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            main_frame, 
            text="Spectre AI", 
            font=('Arial', 24, 'bold'),
            fg='#8b5cf6',
            bg='#1a1a2e'
        )
        title_label.pack(pady=(0, 10))
        
        subtitle_label = tk.Label(
            main_frame,
            text="Your Intelligent Personal Assistant",
            font=('Arial', 12),
            fg='#9ca3af',
            bg='#1a1a2e'
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(expand=True, fill='both')
        
        # Login tab
        self.login_frame = tk.Frame(self.notebook, bg='#1a1a2e')
        self.notebook.add(self.login_frame, text="Sign In")
        
        # Register tab
        self.register_frame = tk.Frame(self.notebook, bg='#1a1a2e')
        self.notebook.add(self.register_frame, text="Sign Up")
        
        self.setup_login_tab()
        self.setup_register_tab()
        
    def setup_login_tab(self):
        # Login form
        login_form = tk.Frame(self.login_frame, bg='#1a1a2e')
        login_form.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Username
        tk.Label(login_form, text="Username:", font=('Arial', 12), fg='white', bg='#1a1a2e').pack(anchor='w', pady=(0, 5))
        username_entry = tk.Entry(
            login_form, 
            textvariable=self.username_var,
            font=('Arial', 12),
            bg='#374151',
            fg='white',
            insertbackground='white',
            relief='flat',
            bd=5
        )
        username_entry.pack(fill='x', pady=(0, 15), ipady=8)
        
        # Password
        tk.Label(login_form, text="Password:", font=('Arial', 12), fg='white', bg='#1a1a2e').pack(anchor='w', pady=(0, 5))
        password_entry = tk.Entry(
            login_form,
            textvariable=self.password_var,
            font=('Arial', 12),
            bg='#374151',
            fg='white',
            insertbackground='white',
            relief='flat',
            bd=5,
            show='*'
        )
        password_entry.pack(fill='x', pady=(0, 20), ipady=8)
        
        # Login button
        login_btn = tk.Button(
            login_form,
            text="Sign In",
            font=('Arial', 12, 'bold'),
            bg='#8b5cf6',
            fg='white',
            relief='flat',
            bd=0,
            pady=10,
            command=self.login
        )
        login_btn.pack(fill='x', pady=(0, 10))
        
    def setup_register_tab(self):
        # Register form
        register_form = tk.Frame(self.register_frame, bg='#1a1a2e')
        register_form.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Username
        tk.Label(register_form, text="Username:", font=('Arial', 12), fg='white', bg='#1a1a2e').pack(anchor='w', pady=(0, 5))
        reg_username_entry = tk.Entry(
            register_form,
            textvariable=self.username_var,
            font=('Arial', 12),
            bg='#374151',
            fg='white',
            insertbackground='white',
            relief='flat',
            bd=5
        )
        reg_username_entry.pack(fill='x', pady=(0, 15), ipady=8)
        
        # Email
        tk.Label(register_form, text="Email:", font=('Arial', 12), fg='white', bg='#1a1a2e').pack(anchor='w', pady=(0, 5))
        email_entry = tk.Entry(
            register_form,
            textvariable=self.email_var,
            font=('Arial', 12),
            bg='#374151',
            fg='white',
            insertbackground='white',
            relief='flat',
            bd=5
        )
        email_entry.pack(fill='x', pady=(0, 15), ipady=8)
        
        # Password
        tk.Label(register_form, text="Password:", font=('Arial', 12), fg='white', bg='#1a1a2e').pack(anchor='w', pady=(0, 5))
        reg_password_entry = tk.Entry(
            register_form,
            textvariable=self.password_var,
            font=('Arial', 12),
            bg='#374151',
            fg='white',
            insertbackground='white',
            relief='flat',
            bd=5,
            show='*'
        )
        reg_password_entry.pack(fill='x', pady=(0, 15), ipady=8)
        
        # Confirm Password
        tk.Label(register_form, text="Confirm Password:", font=('Arial', 12), fg='white', bg='#1a1a2e').pack(anchor='w', pady=(0, 5))
        confirm_password_entry = tk.Entry(
            register_form,
            textvariable=self.confirm_password_var,
            font=('Arial', 12),
            bg='#374151',
            fg='white',
            insertbackground='white',
            relief='flat',
            bd=5,
            show='*'
        )
        confirm_password_entry.pack(fill='x', pady=(0, 20), ipady=8)
        
        # Register button
        register_btn = tk.Button(
            register_form,
            text="Sign Up",
            font=('Arial', 12, 'bold'),
            bg='#8b5cf6',
            fg='white',
            relief='flat',
            bd=0,
            pady=10,
            command=self.register
        )
        register_btn.pack(fill='x', pady=(0, 10))
        
    def login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
            
        try:
            # Prepare form data for OAuth2
            form_data = {
                'username': username,
                'password': password
            }
            
            response = requests.post(
                f"{self.api_base_url}/token",
                data=form_data,
                headers={'Content-Type': 'application/x-www-form-urlencoded'}
            )
            
            if response.status_code == 200:
                token_data = response.json()
                self.access_token = token_data['access_token']
                
                # Get user data
                headers = {'Authorization': f'Bearer {self.access_token}'}
                user_response = requests.get(f"{self.api_base_url}/users/me", headers=headers)
                
                if user_response.status_code == 200:
                    self.user_data = user_response.json()
                    messagebox.showinfo("Success", f"Welcome back, {self.user_data['username']}!")
                    self.root.quit()
                else:
                    messagebox.showerror("Error", "Failed to get user data")
            else:
                error_data = response.json()
                messagebox.showerror("Error", error_data.get('detail', 'Login failed'))
                
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Connection error: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            
    def register(self):
        username = self.username_var.get().strip()
        email = self.email_var.get().strip()
        password = self.password_var.get().strip()
        confirm_password = self.confirm_password_var.get().strip()
        
        if not all([username, email, password, confirm_password]):
            messagebox.showerror("Error", "Please fill in all fields")
            return
            
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return
            
        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters long")
            return
            
        try:
            user_data = {
                'username': username,
                'email': email,
                'password': password
            }
            
            response = requests.post(
                f"{self.api_base_url}/register",
                json=user_data,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                messagebox.showinfo("Success", "Account created successfully! Please sign in.")
                self.notebook.select(0)  # Switch to login tab
                self.password_var.set("")
                self.confirm_password_var.set("")
            else:
                error_data = response.json()
                messagebox.showerror("Error", error_data.get('detail', 'Registration failed'))
                
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Connection error: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            
    def run(self) -> Optional[Dict[str, Any]]:
        """Run the authentication UI and return user data if successful"""
        self.root.mainloop()
        self.root.destroy()
        
        if self.user_data and self.access_token:
            return {
                'user': self.user_data,
                'access_token': self.access_token
            }
        return None

def authenticate_user() -> Optional[Dict[str, Any]]:
    """Convenience function to run authentication"""
    auth_ui = AuthUI()
    return auth_ui.run()

if __name__ == "__main__":
    result = authenticate_user()
    if result:
        print(f"Authenticated user: {result['user']['username']}")
    else:
        print("Authentication cancelled or failed")