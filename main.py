import praw
import discord
import asyncio
import os
from discord import Intents
from dotenv import load_dotenv

# Replace these values with your own
load_dotenv()
reddit_client_id = os.getenv("REDDIT_CLIENT_ID")
reddit_client_secret = os.getenv("REDDIT_CLIENT_SECRET")
reddit_username = os.getenv("REDDIT_USERNAME")
reddit_password = os.getenv("REDDIT_PASSWORD")
discord_token = os.getenv("DISCORD_BOT_TOKEN02")
user_ids = [int(user_id) for user_id in os.getenv("DISCORD_USER_IDS02").split(",")]

# Create the Reddit and Discord clients
reddit = praw.Reddit(client_id=reddit_client_id,
                     client_secret=reddit_client_secret,
                     username=reddit_username,
                     password=reddit_password,
                     user_agent='myBot/0.0.1')

# Setup Intents for Discord client
discord_client = discord.Client(intents=Intents.all())

# Keep track of the last post ID seen
last_post_id = None

# Define a function to send a Discord message
async def send_discord_message(title, url, user_ids):
    for user_id in user_ids:
        user = await discord_client.fetch_user(user_id)
        message = f'New post on r/movieleaks: **{title}**\n{url}'
        await user.send(message)

# Define a function to check for new posts
async def check_for_new_posts():
    global last_post_id
    subreddit = reddit.subreddit('movieleaks')
    new_post = subreddit.new(limit=1).__next__()
    if last_post_id is None or new_post.id != last_post_id:
        last_post_id = new_post.id
        await send_discord_message(new_post.title, new_post.url, user_ids)

# Define a coroutine to run the bot
async def run_bot():
    await discord_client.wait_until_ready()
    while True:
        await check_for_new_posts()
        await asyncio.sleep(60) # Check every minute

# Start the bot
@discord_client.event
async def on_ready():
    # Create task to run bot
    task = discord_client.loop.create_task(run_bot())

# Run the Discord client
discord_client.run(discord_token)
