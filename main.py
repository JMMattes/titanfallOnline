import os
import asyncio
import discord
import requests
from discord import Intents
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("DISCORD_TOKEN01")
USER_IDS = [int(user_id) for user_id in os.getenv("USER_IDS").split(",")]

# Setup Intents for Discord
client = discord.Client(intents=Intents.all())

print(USER_IDS)

# Function to check website and send message
async def check_players():
    while True:
        # Make a request to website
        weburl = str("https://titanfall.p0358.net/status")
        response = requests.get(weburl)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Get the current count
        current_count = soup.find("strong", id="currentCount").text

        # Check if current count is greater than 6
        if int(current_count) >= 6:
            message = f"{current_count} players in Titanfall. Let's GOOOO!!!\n{weburl}"
            for user_id in USER_IDS:
                # Send message to users
                user = client.get_user(user_id)
                await user.send(message)
            # Wait for 4 hours before checking again
            await asyncio.sleep(1*60)
            #await asyncio.sleep(4*60*60)
        else:
            # Wait for 5 minutes before checking again
            await asyncio.sleep(1*60)
            #await asyncio.sleep(5*60)

@client.event
async def on_ready():
    # Create task to check players
    task = client.loop.create_task(check_players())

# Run the Discord client
client.run(token)
