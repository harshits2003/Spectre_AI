from groq import Groq  #Groq Library to use its API
from json import load,dump  #Functions to read, write JSON fles
import datetime  #Module for real-time date & time info
from dotenv import dotenv_values  

env_vars = dotenv_values(".env")

#Retrieve specific environment variables for username, assisstant name, and API key
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")

#Initialize Groq client
client = Groq(api_key=GroqAPIKey)

messages=[]

#Define a system message that provides context to the chatbot about its roles and behavior
System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
*** Be a little fun to talk to. Adapt the way the user talks and try to match the vibe. ***
*** Avoid giving answers in a rigid format. For example: You don't have to say "According to my real-time google search" everytime you are asked about a search from the internet***
"""

#A list of system instructions for the chatbot
SystemChatBot = [
    {"role": "system", "content": System}
]

#Attempt to load the chat log from a JSON file
try:
    with open(r"Data\ChatLog.json", "r") as f:
        messages = load(f)  #Load existing messages from the chat log
except FileNotFoundError:
    #If file doesn't exist, create an empty JSON file to store chat logs
    with open(r"Data\ChatLog.json", "w") as f:
        dump([], f)

#Function to get real-time date and time info
def RealTimeInformation():
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")

    #Format the info into string
    data = f"Please use this real-time information if needed, \n"
    data += f"Day: {day}\nDate: {date}\nMonth: {month}\nYear: {year}\n"
    data += f"Time: {hour} hours: {minute} minutes: {second} seconds.\n"
    return data

#Function to modify the chatbot's response for better formatting
def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

#Main chatbot function to handle user queries
def ChatBot(Query):
    """ This functiokn sends the user's query to the chatbot and returns the AI's response """

    try:
        with open(r"Data\ChatLog.json", "r") as f:
            messages = load(f)
        
        #Append the user's query to the messages list
        messages.append({"role": "user", "content": f"{Query}"})

        #Make a request to the Groq API for a response
        completion = client.chat.completions.create(
            model = "llama3-70b-8192",
            messages = SystemChatBot + [{"role": "system", "content": RealTimeInformation()}] + messages,
            max_tokens = 1024,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop = None
        )

        Answer = ""   #Initialize empty string to store AI's response


        #Process the streamed response chunks
        for chunk in completion:
            if chunk.choices[0].delta.content:   #Check if there's content in the current chunk
                Answer += chunk.choices[0].delta.content   #Append the content from the response

        Answer = Answer.replace("</s>", "")  #Clean up any unwanted tokens from the response

        #Append the chatbot's response to the message list
        messages.append({"role": "assistant", "content": Answer})

        #Save the updated chat log to the JSON file
        with open(r"Data\ChatLog.json", "w") as f:
            dump(messages,f,indent=4)
    
        #Return the formatted response
        return AnswerModifier(Answer = Answer)
    
    except Exception as e:
        #Handle errors by printing the exception and resetting the chat log
        print(f"Error: {e}")
        with open(r"Data\ChatLog.json", "w") as f:
            dump([],f,indent = 4)
        return ChatBot(Query)   #Retry the query after resetting the log
    

#Main program entry point
if __name__ == "__main__":
    while True:
        user_input = input("Enter your Question : ")
        print(ChatBot(user_input))
