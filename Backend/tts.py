import pygame  #For handling audio playback
import random  #For generating random choices
import asyncio  #For async operations
import edge_tts  #for TTS functionality
import os
from dotenv import dotenv_values

env_vars = dotenv_values(".env")
AssistantVoice = env_vars.get("AssistantVoice")

#Async function to convert text to an audio file
async def TextToAudioFile(text) -> None:
    file_path = r"Data\speech.mp3"   #Define the path where the speech file will be saved

    if os.path.exists(file_path):  #check if the file already exist
        os.remove(file_path)

    #Create the communicate object to generate speech
    communicate = edge_tts.Communicate(text, AssistantVoice, pitch='+5Hz', rate='+13%')
    await communicate.save(r'Data\speech.mp3')  #Save the generated speech as an MP# file

#Function to manage TTS functionality
def TTS(Text, func=lambda r=None: True):
    while True:
        try:
            #Convert text to audio file asynchronously
            asyncio.run(TextToAudioFile(Text))

            #Initialize pygame mixer for audio playback
            pygame.mixer.init()

            #Load the generated speech file into pygame mixer
            pygame.mixer.music.load(r'Data\speech.mp3')
            pygame.mixer.music.play()  #Play the audio

            #Loop until the audio is done playing or the function stops
            while pygame.mixer.music.get_busy():
                if func() == False:
                    break
                pygame.time.Clock().tick(10)
            return True
        except Exception as e:
            print(f"Error in TTS: {e}")
        
        finally:
            try:
                #Call the provided function with false to signal the end of TTS
                func(False)
                pygame.mixer.music.stop()
                pygame.mixer.quit()

            except Exception as e:
                print("Error in finally block: {e}")

#Function to manage TTS with additional responses for long text
def TextToSpeech(Text, func=lambda r=None: True):
    Data = str(Text).split(".")

    #List the predefined responses for cases where the text is too long
    responses = [
        "The rest of the result has been printed to the chat screen, kindly check it out sir.",
        "The rest of the text is now on the chat screen, sir, please check it.",
        "You can see the rest of the text on the chat screen, sir.",
        "The remaining part of the text is now on the chat screen, sir.",
        "Sir, you'll find more text on the chat screen for you to see.",
        "The rest of the answer is now on the chat screen, sir.",
        "Sir, please look at the chat screen, the rest of the answer is there.",
        "You'll find the complete answer on the chat screen, sir.",
        "The next part of the text is on the chat screen, sir.",
        "Sir, please check the chat screen for more information.",
        "There's more text on the chat screen for you, sir.",
        "Sir, take a look at the chat screen for additional text.",
        "You'll find more to read on the chat screen, sir.",
        "Sir, check the chat screen for the rest of the text.",
        "The chat screen has the rest of the text, sir.",
        "There's more to see on the chat screen, sir, please look.",
        "Sir, the chat screen holds the continuation of the text.",
        "You'll find the complete answer on the chat screen, kindly check it out sir.",
        "Please review the chat screen for the rest of the text, sir.",
        "Sir, look at the chat screen for the complete answer."
    ]

    #If the textt is very long (more than 4 sentences and 250 characters), add a response message
    if len(Data) > 4 and len(Text) >= 250:
        TTS(" ".join(Text.split(".")[0:2]) + ". " + random.choice(responses), func)
    
    #Otherwise, just play the whole text
    else:
        TTS(Text,func)

if __name__ == "__main__":
    while True:
        TextToSpeech(input("Enter the text: "))