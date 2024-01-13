from discord import *
import requests
from discord.ext import commands
import os
import openai
import json
from dotenv import load_dotenv    
from helper import *

#Define intentions, due to changes in Ts&Cs policy.
intents = Intents.all()
intents.message_content = True


#Creates an environment for what we are currently in.
load_dotenv()

#Gets the discord token from the environment.
TOKEN = os.getenv('DISCORD_TOKEN')
openai.api_key = os.getenv('OPENAI_TOKEN')

# Create the bot instance with command prefix
bot = commands.Bot(command_prefix='!', intents=intents)



wordDictionary = {}

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.event
async def on_message(message):
    #Avoid self-looping
    if message.author == bot.user:
        return

    print("A message has been detected by someone!")
    
    #Create a new dictionary for the user if they've not already spoken.
    if wordDictionary.get(message.author) == None:
        wordDictionary[message.author] = {}
    
    #Change our working dictionary
    currentDictionary = wordDictionary[message.author]
    

    
    
    #UPDATE THIS TO BE PUT INTO THE BOT.COMMANDS SEGEMENT!!!!
    
    #If we didn't input the command to check the contents.
    if message.content != "Check Contents":
        
        #Transform the message contents and split it up for words.
        currentMessage = remove_special_characters(message.content).split(' ')
        
        #Add word counts to the database.
        for word in currentMessage:
            if word != "":
                if currentDictionary.get(word) == None:
                    currentDictionary[word] = 1
                else:
                    currentDictionary[word] += 1
    
    else:
        #Send a title message
        await message.channel.send(f"{message.author}'s word count database:")
        
        #Assemble a string to send on discord.
        finalString = ""
        for word, count in currentDictionary.items():
            finalString += f"{word}: {count}\n"
        
        #Send the message
        await message.channel.send(finalString)
    
    #Custom hello message
    if message.content == "Hello!":
       await message.channel.send(f'Hello, {message.author}!')
    
    print(f"User: {message.author}\nMessage: {message.content}")
       
    await bot.process_commands(message)
    
    
@bot.command()
async def chat_request(ctx, *args):
    print("Attempting to reach chatgpt")
    request_message = ' '.join(args)
    
    if openai.api_key is None:
        await message.channel.send(f"The API key was set incorrectly!")
        raise ValueError("OpenAI API key is invalid!")
    
    url = "https://api.openai.com/v1/completions"
    print(openai.api_key)
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai.api_key}"
    }
    
    data = {
    "model": "gpt-3.5-turbo",
    "messages": [
        {
            "role": "system",
            "content": f"{request_message}"
        },
        {
            "role": "user",
            "content": "Hello!"
        }
    ]}

    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        print("Response successful!")
        await message.channel.send(response.json())
    else:
        print("Connection unsuccessful")
        print(response.status_code)
    

bot.run(TOKEN)