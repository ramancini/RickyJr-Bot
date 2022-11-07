import logging
import os
from dotenv import load_dotenv
import discord
from discord import app_commands

# Set up logging
handler = logging.FileHandler(filename='bot.log', encoding='utf-8', mode='w')
dt_fmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
handler.setFormatter(formatter)

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

# Load environment variables
load_dotenv()
TOKEN = os.getenv('TOKEN')


# Define Client class
class AClient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.all())
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync(guild=None)
            self.synced = True
        print(f'We have logged in as {self.user}')


# Create client and command tree
client = AClient()
tree = app_commands.CommandTree(client)

# Start the bot
if __name__ == '__main__':
    logger.info("Starting!")
    client.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)
