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
def Content(Topic):

    #Nested function to open a file in Notepad
    def OpenNotepad(File):
        default_text_editor = 'notepad.exe'
        subprocess.Popen([default_text_editor, File])  #Open the file in Notepad

    #Nested function to generate content using the AI chatbot
    def ContentWriterAI(prompt):
        messages.append({"role": "user", "content": f"{prompt}"})

        completion = client.chat.completions.create(
            model = "mixtral-8x7b-32768",   #specify the AI model
            messages = SystemChatBot + messages,   #Include system instructions and chat history
            max_tokens=2048,
            temperature=0.7,
            top_p=1,   #Use nucleus samping for response diversity
            stream=True,   #Enables Streaming responses
            stop=None   #Allow model to decide the stopping conditions
        )

        Answer = ""

        #Process streamed response chunks
        for chunk in completion:
            if chunk.choices[0].delta.content:   #Check for content in the current chunk
                Answer += chunk.choices[0].delta.content   #append the cintent to the answer
        
        Answer = Answer.replace("</s>", "")   #Remove unwanted tokens from the response
        messages.append({"role": "assistant", "content": Answer})   #Add the AI's response to messages
        return Answer
    
    Topic: str = Topic.replace("Content ", "")  #Remove 'Content' from the topic
    ContentByAI = ContentWriterAI(Topic)   #Generate content using AI

    #Save the generated content to a text file
    with open(rf"Data\{Topic.lower.replace(' ','')}.txt", "w", encoding="utf-8") as file:
        file.write(ContentByAI)   #Write the generated content to the file
        file.close()

        OpenNotepad(rf"Data\{Topic.lower().replace(' '),''}.txt")   #Open file in Notepad
        return True
    
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
                link = extract_links(html)[0]   #Extract the first link from the search results
                webopen(link)   #Opens the link in a web browser

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
    def System(command):

        #Nested function to mute the system volume
        def mute():
            keyboard.press_and_release("volume mute")

        #Nested function to unmute the system
        def unmute():
            keyboard.press_and_release("volume mute")

        #Nested function to turn the volume up
        def volume_up():
            keyboard.press_and_release("volume up")

        #Nested funtion to turn the volume down
        def volume_down():
            keyboard.press_and_release("volume down")

        #Execute appropriate commands
        if command == "mute":
            mute()
        elif command == "unmute":
            unmute()
        elif command == "volume up":
            volume_up()
        elif command == "volume down":
            volume_down()
        return True
    
    #Async function to translate and execute user commands
    async def TranslateAndExecute(commands: list[str]):

        funcs = []  #List to store async tasks

        for command in commands:
            if command.startswith("open "):

                if "open it" in command:
                    pass
                if "open file" in command:
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
            elif command.startswith("system "):
                fun = asyncio.to_thread(System, command.removeprefix("system "))
                funcs.append(fun)
            else:
                print(f"No Function Found. For {command}")
        results = await asyncio.gather(*funcs)  #Executes all tasks concurrantly

        for result in results:   #Process the results
            if isinstance(result, str):
                yield result
            else:
                yield result

    #Async function to automate command execution
    async def Automation(commands: list[str]):

        async for result in TranslateAndExecute(commands):
            pass

        return True


            

