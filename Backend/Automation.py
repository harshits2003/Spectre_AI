#It contains functions for opening and closing apps, performing Google and YouTube searches, generating content using AI, controlling system volume, and asynchronously executing commands.

from AppOpener import close , open as appopen   #Opens and closes apps
from webbrowser import open as webopen #Opens websites in default browser
from pywhatkit import search, playonyt   #Import functions for Google searches and YouTube playback
from dotenv import dotenv_values
from bs4 import BeautifulSoup   #For parsing HTML content
from rich import print   #For styled console output
from groq import Groq
import webbrowser   #For opening URLs
import subprocess   #For interacting with system
import os   #For interacting with system
import requests  #For making HTTP requests
import keyboard  #For keyboard related actions
import asyncio   #For Aync programming
from ics import Calendar, Event
from datetime import datetime
import os
import webbrowser
from Backend.SystemControl import set_volume, mute_mic, adjust_brightness


env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")

#Define CSS classes for parsing specific elements in HTML content
classes = ["zCubwf","hgKElc","LTKOO sY7ric","Z0LcW","gsrt vk_bk FzvWSb YwPhnf","pclqee","tw-Data-text tw-text-small tw-ta","IZ6rdc","O5uR6d LTKOO","vlzY6d","webanswers-webanswers_table__webanswers-table","dDoNo ikb4Bb gsrt","sXLaOe","LWkfKe","VQF4g","qv3Wpe","kno-rdesc","SPZz6b"]

#Define a user-agent for making web requests
useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36"

#Initialize the Groq client
client = Groq(api_key=GroqAPIKey)

#Predefined professional responses for user interactions 
professional_responses = [
    "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
    "I'm at your service for any additional questions or suppport you may need-don't hesitate to ask.",
    "Your feedback is invaluable to me; please let me know if there's anything else I can help you with."
]

#List to store chatbot messages
messages = []


#System messahe to provide context to the chatbot
SystemChatBot = [{"role": "system", "content": f"Hello, I'm {os.environ['Username']}, You're a content writer. You have to write content like letter, codes, applications, essays, notes, songs, poems, captions, emails etc"}]

#Function to perform a Google search
def GoogleSearch(Topic):
    search(Topic)
    return True

#Function to generate content using AI and save it to a file
def OpenNotepad(filepath):
    os.system(f"notepad.exe {filepath}")

def Content(Topic):
    try:
        # Extract actual topic (removes the "content " prefix)
        Topic = Topic.replace("content ", "").strip()

        print(f"⏳ Generating content for: {Topic}")

        # Call the Groq LLM API with updated model
        completion = client.chat.completions.create(
            model="llama3-70b-8192",  # ✅ Updated from deprecated mixtral
            messages=[
                {"role": "system", "content": "You're a professional content creator. Create informative, creative, and well-structured content."},
                {"role": "user", "content": f"Write content on the topic: {Topic}"}
            ],
            temperature=0.8,
            stream=True
        )

        # Collect the streamed content
        ContentByAI = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                ContentByAI += chunk.choices[0].delta.content
                print(chunk.choices[0].delta.content, end="")

        # Ensure filename is safe
        safe_filename = Topic.lower().replace(' ', '_').replace('/', '_')
        filepath = os.path.join("Data", f"{safe_filename}.txt")

        # Write content to a file
        os.makedirs("Data", exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(ContentByAI)

        print(f"\n✅ Content saved to {filepath}")
        OpenNotepad(filepath)

    except Exception as e:
        print(f"❌ Error generating content: {e}")
    
#Function to search for a topic on YouTube
def YoutubeSearch(Topic):
    URL4Search = f"https://www.youtube.com/results?search_query={Topic}"
    webbrowser.open(URL4Search)
    return True
    
#Function to play a video on YouTube
def PlayYoutube(query):
    playonyt(query)
    return True
    
#Function to oopen an application or a relevant webpage
def OpenApp(app, sess=requests.session()):
        
    try:
        appopen(app, match_closest=True, output=True, throw_error=True)  #Attempt to open the app
        return True
    except:

        #Nested Function to extract links from HTML content
        def extract_links(html):
            if html is None:
                return []
            soup = BeautifulSoup(html, 'html.parser')   #Parse the HTML content
            links = soup.find_all('a', {'jsname': 'UWckNb'})   #find relevant links
            return [link.get('href') for link in links]   #Return the links
            
        #Nested function to perform Google search and retrieve HTML
        def search_google(query):
            url = f"https://www.google.com/search?q={query}"   
            headers = {"User-Agent": useragent}
            response = sess.get(url, headers=headers)   #Perform the search

            if response.status_code == 200:
                return response.text   #Return the HTML content if the search is successful
            else:
                print("Failed to retrieve search results")
            return None
            
        html = search_google(app)

        if html:
            links = extract_links(html)
            if links:
                link = links[0]  # Extract the first link
                webopen(link)
            else:
                print("No links found in the search results.")
        return True


        
#Function to Close an application
def CloseApp(app):

    if "chrome" in app:
        pass
    else:
        try:
            close(app, match_closest=True, output=True, throw_error=True)
            return True  #Indicates success
        except:
            return False #Indicated failure
    
#Function to execute system-level commands
def System(command: str):
    command = command.lower()

    if "volume up" in command:
        percent = extract_percent(command) or 10
        set_volume(percent)
        print(f"🔊 Volume increased by {percent}%")

    elif "volume down" in command:
        percent = extract_percent(command) or 10
        set_volume(-percent)
        print(f"🔉 Volume decreased by {percent}%")

    elif "brightness up" in command:
        percent = extract_percent(command) or 10
        adjust_brightness(percent)
        print(f"💡 Brightness increased by {percent}%")

    elif "brightness down" in command:
        percent = extract_percent(command) or 10
        adjust_brightness(-percent)
        print(f"🌙 Brightness decreased by {percent}%")

    elif "mute mic" in command or "unmute mic" in command:
        mute_mic()
        print("🎙️ Mic toggled")

    else:
        print("❓ Unknown system command.")

# Helper: Extract percentage
def extract_percent(text):
    import re
    match = re.search(r'\b(\d+)%?', text)
    return int(match.group(1)) if match else None

#Async function to translate and execute user commands
async def TranslateAndExecute(commands: list[str]):

    funcs = []  #List to store async tasks
    

    for command in commands:
        cmd = command.lower().strip()
        if command.startswith("open "):

            if "open it" in cmd:
                pass
            if "open file" in cmd:
                pass
            else:
                fun = asyncio.to_thread(OpenApp, command.removeprefix("open "))  #Schedule app opening
                funcs.append(fun)
        elif command.startswith("general "):
            pass
        elif command.startswith("realtime "):
            pass
        elif command.startswith("close "):
            fun = asyncio.to_thread(CloseApp, command.removeprefix("close "))  #Schedule app closing
            funcs.append(fun)
        elif command.startswith("play "):
            fun = asyncio.to_thread(PlayYoutube, command.removeprefix("play "))
            funcs.append(fun)
        elif command.startswith("content "):
            fun = asyncio.to_thread(Content, command.removeprefix("content "))
            funcs.append(fun)
        elif command.startswith("google search "):
            fun = asyncio.to_thread(GoogleSearch, command.removeprefix('google search '))
        elif command.startswith("youtube search "):
            fun = asyncio.to_thread(YoutubeSearch, command.removeprefix('youtube search '))
            funcs.append(fun)
            
        elif "volume up" in cmd:
            percent = extract_percentage(cmd) or 10
            funcs.append(asyncio.to_thread(set_volume, percent))

        elif "volume down" in cmd:
            percent = extract_percentage(cmd) or 10
            funcs.append(asyncio.to_thread(set_volume, -percent))

        elif "brightness up" in cmd:
            percent = extract_percentage(cmd) or 10
            funcs.append(asyncio.to_thread(adjust_brightness, percent))

        elif "brightness down" in cmd:
            percent = extract_percentage(cmd) or 10
            funcs.append(asyncio.to_thread(adjust_brightness, -percent))

        elif "mute mic" in cmd or "unmute mic" in cmd:
            funcs.append(asyncio.to_thread(mute_mic))

        
        else:
            print(f"No Function Found. For {command}")
    results = await asyncio.gather(*funcs)  #Executes all tasks concurrantly

    for result in results:   #Process the results
        if isinstance(result, str):
            yield result
        else:
            yield result

def extract_percentage(text):
    """Extract % value from text like 'volume up 20%'"""
    import re
    match = re.search(r'(\d+)\s*%', text)
    return int(match.group(1)) if match else None

#Async function to automate command execution
async def Automation(commands: list[str]):

    async for result in TranslateAndExecute(commands):
        pass

    return True

def create_reminder(datetime_str: str, message: str) -> bool:
    
    try:
        # Parse the datetime string
        event_time = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")

        # Create a calendar and event
        cal = Calendar()
        event = Event()
        event.name = message
        event.begin = event_time
        event.duration = {"minutes": 30}  # Default duration 30 minutes
        cal.events.add(event)

        # Prepare the reminders directory
        reminders_dir = os.path.join(os.getcwd(), "Data", "Reminders")
        os.makedirs(reminders_dir, exist_ok=True)

        # Save the .ics file
        filename = f"reminder_{event_time.strftime('%Y%m%d_%H%M')}.ics"
        filepath = os.path.join(reminders_dir, filename)
        with open(filepath, "w") as f:
            f.writelines(cal)

        # Open the .ics file with the default calendar app
        webbrowser.open(filepath)

        return True
    except Exception as e:
        print(f"Error creating reminder: {e}")
        return False


            

