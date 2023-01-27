import time
import requests
from bs4 import BeautifulSoup
import discord
from discord import Intents
from discord import app_commands
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("DISCORD_TOKEN01")
user_ids_string = os.environ.get("USER_IDS")
user_ids = list(map(int, user_ids_string.split(",")))  # list of user ids to send the message to

# Setup Intents for Discord
class aclient(discord.Client):
    def __init__(self) -> None:
        super().__init__(intents=discord.Intents.default())
        #self.tree = app_commands.CommandTree(self)
        #self.activity = discord.Activity(type=discord.ActivityType.watching, name="/chat | /help")

# Discord client
client = aclient()

# Constants
CHECK_INTERVAL = 300  # check website every 5 minutes, in seconds
MESSAGE_WAIT_TIME = 3600  # wait this many seconds (default = 1 hour or 3600 seconds) before sending another message
last_message_time = 0  # time of last message sent

# Send message function
async def send_message(message):
    global last_message_time
    # Check if enough time has passed since the last message
    if time.time() - last_message_time > MESSAGE_WAIT_TIME:
        for user_id in user_ids:
            user = client.get_user(user_id)
            await user.send(message)
        last_message_time = time.time()
    else:
        print("Not sending message, last message sent too recently.")

@client.event
async def main_loop():
    while True:
        try:
            # URL to explore
            website = "https://titanfall.p0358.net/status"
            
            # Send a GET request to the website
            response = requests.get(website)

            # Parse the HTML content
            soup = BeautifulSoup(response.content, "html.parser")

            # Find the tag with the ID "currentCount"
            current_count = soup.find("strong", {"id": "currentCount"})

            # Extract the contents of the tag
            current_count = int(current_count.text)

            # Check if the contents is greater than 6
            output = current_count >= 6

            if output:
                message = f"{current_count} players in Titanfall. Let's GOOOO!!!\n{website}"
                await send_message(message)
            else:
                print("Output not true, not sending message.")

        except:
            print("Error occured while checking website.")

        # Wait for the next check
        time.sleep(CHECK_INTERVAL)

client.run(token)
client.loop.create_task(main_loop())
