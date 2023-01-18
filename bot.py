import os

from discord import app_commands
from dotenv import load_dotenv
import discord
from discord.ext import commands

# Load environment variables
load_dotenv(dotenv_path='data/.env')
TOKEN = os.getenv('TOKEN')
GUILD_ID = os.getenv('GUILD_ID')
DEV_ID = os.getenv('DEV_ID')
APP_ID = os.getenv('APPLICATION_ID')


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

bot.run(TOKEN)