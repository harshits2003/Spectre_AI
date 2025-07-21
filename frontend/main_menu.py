import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any, Callable
import sys

class MainMenuUI:
    def __init__(self, user_data: Dict[str, Any], on_choice: Callable[[int], None]):
        self.user_data = user_data
        self.on_choice = on_choice
        self.choice = None
        
        self.root = tk.Tk()
        self.root.title("Spectre AI - Main Menu")
        self.root.geometry("500x400")
        self.root.configure(bg='#1a1a2e')
        self.root.resizable(False, False)
        
        # Center the window
        self.center_window()
        
        self.setup_ui()
        
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.root.winfo_screenheight() // 2) - (400 // 2)
        self.root.geometry(f"500x400+{x}+{y}")
        
    def setup_ui(self):
        # Main container
        main_frame = tk.Frame(self.root, bg='#1a1a2e')
        main_frame.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Header
        header_frame = tk.Frame(main_frame, bg='#1a1a2e')
        header_frame.pack(fill='x', pady=(0, 30))
        
        # Title
        title_label = tk.Label(
            header_frame,
            text="🌌 SPECTRE AI",
            font=('Arial', 24, 'bold'),
            fg='#8b5cf6',
            bg='#1a1a2e'
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            header_frame,
            text="Enhanced Multi-User AI Assistant",
            font=('Arial', 12),
            fg='#9ca3af',
            bg='#1a1a2e'
        )
        subtitle_label.pack(pady=(5, 0))
        
        # Welcome message
        welcome_frame = tk.Frame(main_frame, bg='#2d1b69', relief='flat', bd=1)
        welcome_frame.pack(fill='x', pady=(0, 30))
        
        welcome_label = tk.Label(
            welcome_frame,
            text=f"Welcome back, {self.user_data['username']}! 👋",
            font=('Arial', 14, 'bold'),
            fg='white',
            bg='#2d1b69',
            pady=15
        )
        welcome_label.pack()
        
        # Interface options
        options_frame = tk.Frame(main_frame, bg='#1a1a2e')
        options_frame.pack(fill='both', expand=True)
        
        options_label = tk.Label(
            options_frame,
            text="Choose your interface:",
            font=('Arial', 14, 'bold'),
            fg='white',
            bg='#1a1a2e'
        )
        options_label.pack(pady=(0, 20))
        
        # Voice Interface Button
        voice_btn = tk.Button(
            options_frame,
            text="🎙️ Voice Interface",
            font=('Arial', 12, 'bold'),
            bg='#8b5cf6',
            fg='white',
            relief='flat',
            bd=0,
            pady=15,
            command=lambda: self.make_choice(1)
        )
        voice_btn.pack(fill='x', pady=(0, 10))
        
        voice_desc = tk.Label(
            options_frame,
            text="Original GUI with voice commands and speech recognition",
            font=('Arial', 10),
            fg='#9ca3af',
            bg='#1a1a2e'
        )
        voice_desc.pack(pady=(0, 20))
        
        # Chat Interface Button
        chat_btn = tk.Button(
            options_frame,
            text="💬 Chat Interface",
            font=('Arial', 12, 'bold'),
            bg='#10b981',
            fg='white',
            relief='flat',
            bd=0,
            pady=15,
            command=lambda: self.make_choice(2)
        )
        chat_btn.pack(fill='x', pady=(0, 10))
        
        chat_desc = tk.Label(
            options_frame,
            text="Modern text-based chat interface with persistent memory",
            font=('Arial', 10),
            fg='#9ca3af',
            bg='#1a1a2e'
        )
        chat_desc.pack(pady=(0, 30))
        
        # Exit button
        exit_btn = tk.Button(
            options_frame,
            text="🚪 Exit",
            font=('Arial', 11),
            bg='#374151',
            fg='white',
            relief='flat',
            bd=0,
            pady=10,
            command=lambda: self.make_choice(3)
        )
        exit_btn.pack(fill='x')
        
        # Bind escape key to exit
        self.root.bind('<Escape>', lambda e: self.make_choice(3))
        
    def make_choice(self, choice: int):
        """Handle user choice"""
        self.choice = choice
        self.root.quit()
        
    def run(self) -> int:
        """Run the menu and return user choice"""
        self.root.mainloop()
        self.root.destroy()
        return self.choice if self.choice else 3

def show_main_menu(user_data: Dict[str, Any]) -> int:
    """Show main menu and return user choice"""
    menu = MainMenuUI(user_data, lambda x: None)
    return menu.run()

if __name__ == "__main__":
    # Example usage
    sample_user = {
        'username': 'testuser',
        'email': 'test@example.com'
    }
    choice = show_main_menu(sample_user)
    print(f"User chose: {choice}")