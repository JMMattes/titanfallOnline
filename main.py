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

        # Get stats-table data and compare for message.
        table = soup.find('table', {'id': 'stats-table'})
        headers = [header.text for header in table.find_all('th')[:5]]
        rows = []
        for row in table.find_all('tr')[2:]:
            cols = row.find_all('td')[:5]
            row_data = [col.text for col in cols]
            rows.append(row_data)

        # Find the largest number in column 2
        col_2_max = max([int(row[1]) for row in rows])
        col_2_max_index = [i for i, row in enumerate(rows) if int(row[1]) == col_2_max]
        col_2_max_index_int = int(col_2_max_index[0])

        # Save the number and relevant data in column 1 as variables
        col_1_max_data = rows[col_2_max_index[0]][0]

        # Find the highest number in columns 3, 4, and 5 only from the row with highest value in column 2
        col_3_4_5 = [int(rows[col_2_max_index_int][2]), int(rows[col_2_max_index_int][3]), int(rows[col_2_max_index_int][4])]
        col_3_4_5_max = max(col_3_4_5)
        col_3_4_5_header_index = [i for i, val in enumerate(col_3_4_5) if val == col_3_4_5_max]
        col_3_4_5_header_text = [headers[2 + i] for i in col_3_4_5_header_index]
        col345_ht_str = str(col_3_4_5_header_text[0])
        
        # Check if current count is greater than 14
        if int(current_count) >= 14:
            message = f"{current_count} players in Titanfall. Let's GOOOO!!!\nMost players ({col_3_4_5_max}) are currently playing mode type {col_1_max_data} on servers in {col345_ht_str}.\n{weburl}"
            for user_id in USER_IDS:
                # Send message to users
                user = client.get_user(user_id)
                await user.send(message)
            # Wait for 2 hours before checking again
            await asyncio.sleep(4*60*60)
        else:
            # Wait for 5 minutes before checking again
            await asyncio.sleep(5*60)

@client.event
async def on_ready():
    # Create task to check players
    task = client.loop.create_task(check_players())

# Run the Discord client
client.run(token)
