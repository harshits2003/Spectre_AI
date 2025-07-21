import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import requests
import json
from datetime import datetime
from typing import Optional, Dict, Any, List
import threading
import time

class ChatUI:
    def __init__(self, user_data: Dict[str, Any], access_token: str, api_base_url: str = "http://localhost:8000"):
        self.user_data = user_data
        self.access_token = access_token
        self.api_base_url = api_base_url
        self.headers = {'Authorization': f'Bearer {access_token}'}
        
        self.root = tk.Tk()
        self.root.title(f"Spectre AI - Chat with {user_data['username']}")
        self.root.geometry("800x600")
        self.root.configure(bg='#1a1a2e')
        
        # Chat variables
        self.current_session_id = None
        self.chat_sessions = []
        self.is_typing = False
        
        self.setup_ui()
        self.load_chat_sessions()
        
    def setup_ui(self):
        # Main container
        main_container = tk.Frame(self.root, bg='#1a1a2e')
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Header
        self.setup_header(main_container)
        
        # Chat area container
        chat_container = tk.Frame(main_container, bg='#1a1a2e')
        chat_container.pack(fill='both', expand=True, pady=(10, 0))
        
        # Sidebar for chat sessions
        self.setup_sidebar(chat_container)
        
        # Main chat area
        self.setup_chat_area(chat_container)
        
    def setup_header(self, parent):
        header_frame = tk.Frame(parent, bg='#2d1b69', height=60)
        header_frame.pack(fill='x', pady=(0, 10))
        header_frame.pack_propagate(False)
        
        # Title and user info
        title_frame = tk.Frame(header_frame, bg='#2d1b69')
        title_frame.pack(side='left', fill='y', padx=20, pady=10)
        
        title_label = tk.Label(
            title_frame,
            text="Spectre AI",
            font=('Arial', 18, 'bold'),
            fg='#8b5cf6',
            bg='#2d1b69'
        )
        title_label.pack(anchor='w')
        
        user_label = tk.Label(
            title_frame,
            text=f"Welcome, {self.user_data['username']}",
            font=('Arial', 12),
            fg='#9ca3af',
            bg='#2d1b69'
        )
        user_label.pack(anchor='w')
        
        # Control buttons
        controls_frame = tk.Frame(header_frame, bg='#2d1b69')
        controls_frame.pack(side='right', fill='y', padx=20, pady=10)
        
        new_chat_btn = tk.Button(
            controls_frame,
            text="New Chat",
            font=('Arial', 10, 'bold'),
            bg='#8b5cf6',
            fg='white',
            relief='flat',
            bd=0,
            padx=15,
            pady=5,
            command=self.create_new_chat
        )
        new_chat_btn.pack(side='right', padx=(10, 0))
        
        refresh_btn = tk.Button(
            controls_frame,
            text="Refresh",
            font=('Arial', 10),
            bg='#374151',
            fg='white',
            relief='flat',
            bd=0,
            padx=15,
            pady=5,
            command=self.load_chat_sessions
        )
        refresh_btn.pack(side='right')
        
    def setup_sidebar(self, parent):
        sidebar_frame = tk.Frame(parent, bg='#16213e', width=250)
        sidebar_frame.pack(side='left', fill='y', padx=(0, 10))
        sidebar_frame.pack_propagate(False)
        
        # Sidebar header
        sidebar_header = tk.Label(
            sidebar_frame,
            text="Chat Sessions",
            font=('Arial', 14, 'bold'),
            fg='white',
            bg='#16213e',
            pady=15
        )
        sidebar_header.pack(fill='x')
        
        # Sessions list
        sessions_frame = tk.Frame(sidebar_frame, bg='#16213e')
        sessions_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        # Scrollable sessions list
        self.sessions_canvas = tk.Canvas(sessions_frame, bg='#16213e', highlightthickness=0)
        sessions_scrollbar = ttk.Scrollbar(sessions_frame, orient="vertical", command=self.sessions_canvas.yview)
        self.sessions_scrollable_frame = tk.Frame(self.sessions_canvas, bg='#16213e')
        
        self.sessions_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.sessions_canvas.configure(scrollregion=self.sessions_canvas.bbox("all"))
        )
        
        self.sessions_canvas.create_window((0, 0), window=self.sessions_scrollable_frame, anchor="nw")
        self.sessions_canvas.configure(yscrollcommand=sessions_scrollbar.set)
        
        self.sessions_canvas.pack(side="left", fill="both", expand=True)
        sessions_scrollbar.pack(side="right", fill="y")
        
    def setup_chat_area(self, parent):
        chat_frame = tk.Frame(parent, bg='#1a1a2e')
        chat_frame.pack(side='right', fill='both', expand=True)
        
        # Chat display area
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            font=('Arial', 11),
            bg='#0f172a',
            fg='white',
            insertbackground='white',
            selectbackground='#8b5cf6',
            selectforeground='white',
            relief='flat',
            bd=0,
            padx=15,
            pady=15,
            state='disabled'
        )
        self.chat_display.pack(fill='both', expand=True, pady=(0, 10))
        
        # Configure text tags for styling
        self.chat_display.tag_configure("user", foreground="#8b5cf6", font=('Arial', 11, 'bold'))
        self.chat_display.tag_configure("assistant", foreground="#10b981", font=('Arial', 11, 'bold'))
        self.chat_display.tag_configure("timestamp", foreground="#6b7280", font=('Arial', 9))
        self.chat_display.tag_configure("typing", foreground="#fbbf24", font=('Arial', 10, 'italic'))
        
        # Input area
        input_frame = tk.Frame(chat_frame, bg='#1a1a2e')
        input_frame.pack(fill='x')
        
        # Message input
        self.message_entry = tk.Text(
            input_frame,
            height=3,
            font=('Arial', 11),
            bg='#374151',
            fg='white',
            insertbackground='white',
            relief='flat',
            bd=0,
            padx=10,
            pady=10,
            wrap=tk.WORD
        )
        self.message_entry.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Send button
        send_btn = tk.Button(
            input_frame,
            text="Send",
            font=('Arial', 11, 'bold'),
            bg='#8b5cf6',
            fg='white',
            relief='flat',
            bd=0,
            padx=20,
            pady=10,
            command=self.send_message
        )
        send_btn.pack(side='right')
        
        # Bind Enter key to send message
        self.message_entry.bind('<Control-Return>', lambda e: self.send_message())
        
        # Status label
        self.status_label = tk.Label(
            chat_frame,
            text="Ready to chat...",
            font=('Arial', 9),
            fg='#6b7280',
            bg='#1a1a2e',
            anchor='w'
        )
        self.status_label.pack(fill='x', pady=(5, 0))
        
    def load_chat_sessions(self):
        """Load chat sessions from API"""
        try:
            response = requests.get(f"{self.api_base_url}/chat/sessions", headers=self.headers)
            if response.status_code == 200:
                self.chat_sessions = response.json()
                self.update_sessions_display()
            else:
                messagebox.showerror("Error", "Failed to load chat sessions")
        except Exception as e:
            messagebox.showerror("Error", f"Connection error: {str(e)}")
    
    def update_sessions_display(self):
        """Update the sessions display in sidebar"""
        # Clear existing sessions
        for widget in self.sessions_scrollable_frame.winfo_children():
            widget.destroy()
        
        if not self.chat_sessions:
            no_sessions_label = tk.Label(
                self.sessions_scrollable_frame,
                text="No chat sessions yet.\nClick 'New Chat' to start!",
                font=('Arial', 10),
                fg='#6b7280',
                bg='#16213e',
                justify='center'
            )
            no_sessions_label.pack(pady=20)
            return
        
        for session in self.chat_sessions:
            session_frame = tk.Frame(
                self.sessions_scrollable_frame,
                bg='#1f2937' if session['id'] != self.current_session_id else '#8b5cf6',
                relief='flat',
                bd=1
            )
            session_frame.pack(fill='x', pady=2, padx=5)
            
            # Session title
            title_label = tk.Label(
                session_frame,
                text=session['title'][:30] + "..." if len(session['title']) > 30 else session['title'],
                font=('Arial', 10, 'bold'),
                fg='white',
                bg=session_frame['bg'],
                anchor='w'
            )
            title_label.pack(fill='x', padx=10, pady=(8, 2))
            
            # Session info
            message_count = len(session.get('messages', []))
            updated_at = datetime.fromisoformat(session['updated_at'].replace('Z', '+00:00'))
            time_str = updated_at.strftime('%m/%d %H:%M')
            
            info_label = tk.Label(
                session_frame,
                text=f"{message_count} messages • {time_str}",
                font=('Arial', 8),
                fg='#9ca3af',
                bg=session_frame['bg'],
                anchor='w'
            )
            info_label.pack(fill='x', padx=10, pady=(0, 8))
            
            # Bind click event
            session_frame.bind("<Button-1>", lambda e, s=session: self.select_session(s))
            title_label.bind("<Button-1>", lambda e, s=session: self.select_session(s))
            info_label.bind("<Button-1>", lambda e, s=session: self.select_session(s))
    
    def select_session(self, session):
        """Select and load a chat session"""
        self.current_session_id = session['id']
        self.load_session_messages(session)
        self.update_sessions_display()
    
    def load_session_messages(self, session):
        """Load messages for the selected session"""
        self.chat_display.config(state='normal')
        self.chat_display.delete(1.0, tk.END)
        
        messages = session.get('messages', [])
        for message in messages:
            self.display_message(
                message['role'],
                message['content'],
                datetime.fromisoformat(message['timestamp'].replace('Z', '+00:00'))
            )
        
        self.chat_display.config(state='disabled')
        self.chat_display.see(tk.END)
    
    def create_new_chat(self):
        """Create a new chat session"""
        self.current_session_id = None
        self.chat_display.config(state='normal')
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.config(state='disabled')
        
        # Add welcome message
        self.display_message(
            "assistant",
            f"Hello {self.user_data['username']}! I'm Spectre AI. How can I help you today?",
            datetime.now()
        )
        
        self.update_sessions_display()
    
    def display_message(self, role, content, timestamp):
        """Display a message in the chat area"""
        self.chat_display.config(state='normal')
        
        # Add timestamp
        time_str = timestamp.strftime('%H:%M')
        self.chat_display.insert(tk.END, f"[{time_str}] ", "timestamp")
        
        # Add sender name
        sender = self.user_data['username'] if role == 'user' else 'Spectre AI'
        self.chat_display.insert(tk.END, f"{sender}: ", role)
        
        # Add message content
        self.chat_display.insert(tk.END, f"{content}\n\n")
        
        self.chat_display.config(state='disabled')
        self.chat_display.see(tk.END)
    
    def show_typing_indicator(self):
        """Show typing indicator"""
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, "Spectre AI is thinking...\n", "typing")
        self.chat_display.config(state='disabled')
        self.chat_display.see(tk.END)
    
    def remove_typing_indicator(self):
        """Remove typing indicator"""
        self.chat_display.config(state='normal')
        content = self.chat_display.get(1.0, tk.END)
        if "Spectre AI is thinking..." in content:
            lines = content.split('\n')
            lines = [line for line in lines if "Spectre AI is thinking..." not in line]
            self.chat_display.delete(1.0, tk.END)
            self.chat_display.insert(1.0, '\n'.join(lines))
        self.chat_display.config(state='disabled')
    
    def send_message(self):
        """Send a message to the AI"""
        message = self.message_entry.get(1.0, tk.END).strip()
        if not message:
            return
        
        # Clear input
        self.message_entry.delete(1.0, tk.END)
        
        # Display user message
        self.display_message("user", message, datetime.now())
        
        # Show typing indicator
        self.show_typing_indicator()
        self.status_label.config(text="Sending message...")
        
        # Send message in background thread
        threading.Thread(target=self._send_message_thread, args=(message,), daemon=True).start()
    
    def _send_message_thread(self, message):
        """Send message in background thread"""
        try:
            chat_data = {
                'message': message,
                'session_id': self.current_session_id
            }
            
            response = requests.post(
                f"{self.api_base_url}/chat",
                json=chat_data,
                headers=self.headers
            )
            
            if response.status_code == 200:
                message_data = response.json()
                
                # Update UI in main thread
                self.root.after(0, self._handle_response_success, message_data)
                
                # If this was a new chat, update session ID
                if not self.current_session_id:
                    self.current_session_id = message_data.get('session_id')
                
            else:
                error_data = response.json()
                error_msg = error_data.get('detail', 'Unknown error')
                self.root.after(0, self._handle_response_error, error_msg)
                
        except Exception as e:
            self.root.after(0, self._handle_response_error, str(e))
    
    def _handle_response_success(self, message_data):
        """Handle successful response in main thread"""
        self.remove_typing_indicator()
        
        # Display AI response
        timestamp = datetime.fromisoformat(message_data['timestamp'].replace('Z', '+00:00'))
        self.display_message("assistant", message_data['content'], timestamp)
        
        # Update status
        self.status_label.config(text="Ready to chat...")
        
        # Reload sessions to update sidebar
        self.load_chat_sessions()
    
    def _handle_response_error(self, error_msg):
        """Handle error response in main thread"""
        self.remove_typing_indicator()
        
        # Display error message
        self.display_message("assistant", f"Sorry, I encountered an error: {error_msg}", datetime.now())
        
        # Update status
        self.status_label.config(text="Error occurred. Please try again.")
    
    def run(self):
        """Run the chat UI"""
        # Start with a new chat
        self.create_new_chat()
        
        # Start the main loop
        self.root.mainloop()

def start_chat_interface(user_data: Dict[str, Any], access_token: str) -> None:
    """Start the chat interface"""
    chat_ui = ChatUI(user_data, access_token)
    chat_ui.run()

if __name__ == "__main__":
    # Example usage
    sample_user = {
        'username': 'testuser',
        'email': 'test@example.com'
    }
    sample_token = 'sample_token'
    start_chat_interface(sample_user, sample_token)