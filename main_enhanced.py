from Frontend.GUI import (
    GraphicalUserInterface,
    SetAssistantStatus,
    ShowTextToScreen,
    TempDirectoryPath,
    SetMicrophoneStatus,
    AnswerModifier,
    QueryModifier,
    GetAssistantStatus,
    GetMicrophoneStatus
)
from Backend.model import FirstLayerDMM
from Backend.RealtimeSearchEngine import RealtimeSearchEngine
from Backend.Automation import Automation
from Backend.stt import SpeechRecognition
from Backend.enhanced_chatbot import EnhancedChatBot, RealTimeInformation
from Backend.tts import TextToSpeech
from frontend.auth_ui import authenticate_user
from frontend.chat_ui import start_chat_interface
from frontend.main_menu import show_main_menu
from dotenv import dotenv_values, set_key
from asyncio import run
from time import sleep
import subprocess
import threading
import json
import os
import uvicorn
import multiprocessing
import sys

env_vars = dotenv_values(".env")
Assistantname = env_vars.get("Assistantname")
subprocess_list = []
Functions = ['open', 'close', 'play', 'content', 'google search', 'youtube search']

# Global variables for user session
current_user = None
enhanced_chatbot = None
current_session_id = None

def start_api_server():
    """Start the FastAPI server in a separate process"""
    def run_server():
        from api.main import app
        uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
    
    api_process = multiprocessing.Process(target=run_server)
    api_process.daemon = True
    api_process.start()
    return api_process

def authenticate_and_setup():
    """Authenticate user and setup enhanced chatbot"""
    global current_user, enhanced_chatbot
    
    print("Starting authentication...")
    auth_result = authenticate_user()
    
    if not auth_result:
        print("Authentication failed or cancelled")
        return False
    
    current_user = auth_result
    
    # Update .env file with username
    set_key('.env', 'Username', current_user['user']['username'])
    
    # Initialize enhanced chatbot
    enhanced_chatbot = EnhancedChatBot(
        current_user['user'],
        current_user['access_token']
    )
    
    print(f"Welcome, {current_user['user']['username']}!")
    return True

def ShowDefaultChatIfNoChats():
    """Show default chat if no chats exist"""
    if current_user:
        username = current_user['user']['username']
        DefaultMessage = f'''{username}: Hello {Assistantname}, How are you?
{Assistantname}: Welcome {username}! I remember our previous conversations. How may I help you today?'''
    else:
        DefaultMessage = f'''User: Hello {Assistantname}, How are you?
{Assistantname}: Welcome! How may I help you?'''
    
    with open(TempDirectoryPath('Database.data'), 'w', encoding='utf-8') as file:
        file.write("")
    with open(TempDirectoryPath('Responses.data'), 'w', encoding='utf-8') as file:
        file.write(DefaultMessage)

def ChatLogIntegration():
    """Integrate chat log with enhanced memory"""
    if enhanced_chatbot:
        # Get chat sessions from API
        sessions = enhanced_chatbot.get_chat_sessions()
        
        if sessions:
            # Get the most recent session
            latest_session = sessions[0]
            formatted_chatlog = ""
            
            for message in latest_session.get('messages', []):
                if message['role'] == 'user':
                    formatted_chatlog += f"{current_user['user']['username']}: {message['content']}\n"
                elif message['role'] == 'assistant':
                    formatted_chatlog += f"{Assistantname}: {message['content']}\n"
            
            with open(TempDirectoryPath('Database.data'), 'w', encoding='utf-8') as file:
                file.write(AnswerModifier(formatted_chatlog))
    else:
        # Fallback to local chat log
        try:
            with open(r'Data\ChatLog.json', "r", encoding='utf-8') as file:
                chatlog_data = json.load(file)
            
            formatted_chatlog = ""
            for entry in chatlog_data:
                if entry["role"] == "user":
                    username = current_user['user']['username'] if current_user else "User"
                    formatted_chatlog += f"{username}: {entry['content']}\n"
                elif entry["role"] == "assistant":
                    formatted_chatlog += f"{Assistantname}: {entry['content']}\n"
            
            with open(TempDirectoryPath('Database.data'), 'w', encoding='utf-8') as file:
                file.write(AnswerModifier(formatted_chatlog))
        except:
            pass

def ShowChatsOnGUI():
    """Show chats on GUI"""
    try:
        with open(TempDirectoryPath('Database.data'), 'r', encoding='utf-8') as file:
            data = file.read()
        
        if len(str(data)) > 0:
            lines = data.split('\n')
            result = '\n'.join(lines)
            
            with open(TempDirectoryPath('Responses.data'), 'w', encoding='utf-8') as file:
                file.write(result)
    except:
        pass

def InitialExecution():
    """Initial setup"""
    SetMicrophoneStatus("False")
    ShowTextToScreen("")
    ShowDefaultChatIfNoChats()
    ChatLogIntegration()

def MainExecution():
    """Main execution loop with enhanced features"""
    global current_session_id
    
    TaskExecution = False
    ImageExecution = False
    ImageGenerationQuery = ""

    SetAssistantStatus("Listening...")
    Query = SpeechRecognition()
    
    username = current_user['user']['username'] if current_user else "User"
    ShowTextToScreen(f"{username}: {Query}")
    SetAssistantStatus("Thinking...")
    
    Decision = FirstLayerDMM(Query)
    print(f"Decision: {Decision}")

    G = any([i for i in Decision if i.startswith("general")])
    R = any([i for i in Decision if i.startswith("realtime")])

    Merged_query = " and ".join(
        [" ".join(i.split()[1:]) for i in Decision if i.startswith("general") or i.startswith("realtime")]
    )

    # Handle image generation
    for queries in Decision:
        if "generate" in queries:
            ImageGenerationQuery = str(queries)
            ImageExecution = True

    # Handle automation tasks
    for queries in Decision:
        if TaskExecution == False:
            if any(queries.startswith(func) for func in Functions):
                run(Automation(list(Decision)))
                TaskExecution = True
                SetAssistantStatus("Available...")

    # Handle image generation
    if ImageExecution == True:
        with open(r'Frontend\Files\ImageGenertion.data', 'w') as file:
            file.write(f"{ImageGenerationQuery},True")
        
        try:
            p1 = subprocess.Popen(['python', r"Backend\ImageGeneration.py"],
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                  stdin=subprocess.PIPE, shell=False)
            subprocess_list.append(p1)
        except Exception as e:
            print(f"Error starting ImageGeneration.py: {e}")

    # Handle chat responses with memory
    if G or R:
        if enhanced_chatbot:
            if R:
                SetAssistantStatus("Searching...")
                Answer = RealtimeSearchEngine(QueryModifier(Merged_query))
            else:
                SetAssistantStatus("Thinking...")
                Answer = enhanced_chatbot.chat_with_memory(QueryModifier(Merged_query), current_session_id)
        else:
            # Fallback to original methods
            if R:
                SetAssistantStatus("Searching...")
                Answer = RealtimeSearchEngine(QueryModifier(Merged_query))
            else:
                from Backend.Chatbot import ChatBot
                SetAssistantStatus("Thinking...")
                Answer = ChatBot(QueryModifier(Merged_query))
        
        ShowTextToScreen(f"{Assistantname}: {Answer}")
        SetAssistantStatus("Answering...")
        TextToSpeech(Answer)
        
        # Update chat log integration
        ChatLogIntegration()
        return True

    # Handle exit
    for Queries in Decision:
        if "exit" in Queries:
            QueryFinal = "Okay, Bye!"
            if enhanced_chatbot:
                Answer = enhanced_chatbot.chat_with_memory(QueryFinal, current_session_id)
            else:
                from Backend.Chatbot import ChatBot
                Answer = ChatBot(QueryModifier(QueryFinal))
            
            ShowTextToScreen(f"{Assistantname}: {Answer}")
            SetAssistantStatus("Answering...")
            TextToSpeech(Answer)
            SetAssistantStatus("Turning Off...")
            os._exit(1)

def FirstThread():
    """Main execution thread"""
    while True:
        CurrentStatus = GetMicrophoneStatus()

        if CurrentStatus == "True":
            MainExecution()
        else:
            AIStatus = GetAssistantStatus()
            if "Available..." in AIStatus:
                sleep(0.1)
            else:
                SetAssistantStatus("Available...")

def SecondThread():
    """GUI thread"""
    GraphicalUserInterface()

def start_chat_interface_thread():
    """Start chat interface"""
    start_chat_interface(current_user['user'], current_user['access_token'])
if __name__ == "__main__":
    print("Starting Spectre AI Enhanced...")
    
    # Start API server
    print("Starting API server...")
    api_process = start_api_server()
    
    # Wait a moment for server to start
    sleep(3)
    
    # Authenticate user
    if not authenticate_and_setup():
        print("Exiting due to authentication failure")
        api_process.terminate()
        exit(1)
    
    # Show main menu
    choice = show_main_menu(current_user['user'])
    
    if choice == 1:
        # Original Voice Interface
        print("🎙️ Starting Voice Interface...")
        
        # Initialize
        InitialExecution()
        
        # Start threads
        thread1 = threading.Thread(target=FirstThread, daemon=True)
        thread1.start()
        
        try:
            SecondThread()
        finally:
            # Cleanup
            api_process.terminate()
            for p in subprocess_list:
                p.terminate()
                
    elif choice == 2:
        # Chat Interface
        print("💬 Starting Chat Interface...")
        
        try:
            start_chat_interface_thread()
        finally:
            # Cleanup
            api_process.terminate()
            
    else:
        # Exit
        print("👋 Goodbye!")
        api_process.terminate()
        sys.exit(0)