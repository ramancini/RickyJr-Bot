import os
import logging
from logging import handlers

from dotenv import load_dotenv
import discord
from discord.ext import commands

# Load environment variables
load_dotenv(dotenv_path='data/.env')
TOKEN = os.getenv('TOKEN')
GUILD_ID = os.getenv('GUILD_ID')
DEV_ID = os.getenv('DEV_ID')
APP_ID = os.getenv('APPLICATION_ID')

# Check for the logs directory and create it if it doesn't exist
if not os.path.exists('logs'):
    os.mkdir('logs')

# Set up rotating log file which generates a new file every day (Currently saves up to 7 days)
logHandler = handlers.TimedRotatingFileHandler('logs/bot.log', when='midnight', backupCount=7)
logHandler.suffix = '%Y_%m_%d'

# Formatting for log file
date_format = '%d-%m-%Y %H:%M:%S'
formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', date_format, style='{')


class RickyJr(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='!',
            intents=discord.Intents.all(),
            application_id=APP_ID)

    async def setup_hook(self):
        # Load all cogs in cogs directory
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await self.load_extension(f'cogs.{filename[:-3]}')
                print(f'Loaded {filename[:-3]}')
        await bot.tree.sync()

    async def on_ready(self):
        await self.wait_until_ready()
        print(f'We have logged in as {self.user}')


bot = RickyJr()


@bot.command(name='reload')
async def reload(ctx):
    if ctx.author.id == int(DEV_ID):
        await ctx.send('Reloading cogs...')
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await bot.reload_extension(f'cogs.{filename[:-3]}')
        await bot.tree.sync()
        await ctx.send('Reloaded cogs and command tree')
    else:
        await ctx.send('You are not permitted to use this command')


bot.run(TOKEN, log_handler=logHandler, log_formatter=formatter, log_level=logging.INFO)
