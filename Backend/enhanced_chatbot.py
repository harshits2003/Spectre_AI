from groq import Groq
from json import load, dump
import datetime
from dotenv import dotenv_values
import requests
from typing import Optional, Dict, Any

env_vars = dotenv_values(".env")

Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")

client = Groq(api_key=GroqAPIKey)

class EnhancedChatBot:
    def __init__(self, user_data: Dict[str, Any], access_token: str, api_base_url: str = "http://localhost:8000"):
        self.user_data = user_data
        self.access_token = access_token
        self.api_base_url = api_base_url
        self.headers = {'Authorization': f'Bearer {access_token}'}
        
        # Update system message with user context
        self.system_message = f"""Hello, I am {self.user_data['username']}, You are a very accurate and advanced AI chatbot named {Assistantname} which also has real-time up-to-date information from the internet.

You have persistent memory about this user and can remember previous conversations, preferences, and important information.

*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
*** Be a little fun to talk to. Adapt the way the user talks and try to match the vibe. ***
*** Use the user's name ({self.user_data['username']}) when appropriate to make conversations more personal. ***
*** Remember important information from our conversations for future reference. ***
"""

    def get_user_memories(self) -> str:
        """Fetch user memories from the API"""
        try:
            response = requests.get(f"{self.api_base_url}/memories", headers=self.headers)
            if response.status_code == 200:
                memories = response.json()
                
                if not memories:
                    return ""
                
                context_parts = []
                context_parts.append(f"What I remember about {self.user_data['username']}:")
                
                # Group memories by type
                preferences = [m for m in memories if m['memory_type'] == 'preference']
                facts = [m for m in memories if m['memory_type'] == 'fact']
                contexts = [m for m in memories if m['memory_type'] == 'context']
                
                if preferences:
                    context_parts.append("Preferences:")
                    for pref in preferences[:5]:
                        context_parts.append(f"- {pref['key']}: {pref['value']}")
                
                if facts:
                    context_parts.append("Important facts:")
                    for fact in facts[:5]:
                        context_parts.append(f"- {fact['key']}: {fact['value']}")
                
                return "\n".join(context_parts)
        except Exception as e:
            print(f"Error fetching memories: {e}")
            return ""
    
    def chat_with_memory(self, query: str, session_id: Optional[int] = None) -> str:
        """Send message to API with memory context"""
        try:
            chat_data = {
                'message': query,
                'session_id': session_id
            }
            
            response = requests.post(
                f"{self.api_base_url}/chat",
                json=chat_data,
                headers=self.headers
            )
            
            if response.status_code == 200:
                message_data = response.json()
                return message_data['content']
            else:
                error_data = response.json()
                return f"Error: {error_data.get('detail', 'Unknown error')}"
                
        except Exception as e:
            print(f"Error in chat_with_memory: {e}")
            # Fallback to local chat without memory
            return self.local_chat(query)
    
    def local_chat(self, query: str) -> str:
        """Fallback local chat without API"""
        try:
            # Get memory context
            memory_context = self.get_user_memories()
            
            # Prepare messages
            messages = [
                {"role": "system", "content": self.system_message},
                {"role": "system", "content": memory_context},
                {"role": "user", "content": query}
            ]
            
            completion = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=messages,
                max_tokens=1024,
                temperature=0.7,
                top_p=1,
                stream=True,
                stop=None
            )
            
            answer = ""
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    answer += chunk.choices[0].delta.content
            
            return answer.replace("</s>", "").strip()
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    def get_chat_sessions(self):
        """Get user's chat sessions"""
        try:
            response = requests.get(f"{self.api_base_url}/chat/sessions", headers=self.headers)
            if response.status_code == 200:
                return response.json()
            return []
        except Exception as e:
            print(f"Error fetching chat sessions: {e}")
            return []

def RealTimeInformation():
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")

    data = f"Please use this real-time information if needed, \n"
    data += f"Day: {day}\nDate: {date}\nMonth: {month}\nYear: {year}\n"
    data += f"Time: {hour} hours: {minute} minutes: {second} seconds.\n"
    return data

def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer