import discord
from discord import app_commands
from discord.ext import commands

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='ping', description='Pong!')
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Pong! The bot latency is {round(self.bot.latency * 1000)}ms')

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Ping(bot))