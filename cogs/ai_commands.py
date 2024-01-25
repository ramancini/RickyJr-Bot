import os
import discord
from discord import app_commands
from discord.ext import commands
import json
from dotenv import load_dotenv
from openai import OpenAI
import datetime
import database_fns as dbf

# Load environment variables
load_dotenv(dotenv_path='data/.env')
OPENAI_API_KEY = os.getenv('OPENAI_KEY')

# Create the OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Create the database operations object
db = dbf.DatabaseOperations()

# Read in the system prompt from prompt.json
with open('data/prompt.json') as f:
    PROMPT = json.load(f)

def create_completion(message_log: str):
    """
    Creates and returns a completion object based on the message log
    """
    # Create the message log list
    message_log_list = [PROMPT]
    message_log_list.extend(message_log)

    # Create the completion object
    completion = client.chat.completions.create(
        model='gpt-3.5-turbo',
        max_tokens=200,
        messages=message_log_list
    )

    return completion

class AICommands(commands.GroupCog, group_name='ai', group_description='Commands to interact with ChatGPT'):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='chat', description='Talk with ChatGPT')
    async def chat(self, interaction: discord.Interaction, message: str):
        """
        Sends a message to ChatGPT and returns the response in discord
        """
        await interaction.response.defer()

        # Add the message to the database
        db.add_message(interaction.user.id, datetime.datetime.now(), 'user', message)

        # Get the message log
        message_log = db.get_message_log(interaction.user.id)

        # Create the completion object
        completion = create_completion(message_log)

        # Get the response from the completion object
        response = completion.choices[0].message.content

        # Send the response
        await interaction.followup.send(response)

        # Add the message to the database
        db.add_message(interaction.user.id, datetime.datetime.now(), 'assistant', response)
    
    @app_commands.command(name='clear', description='Clear the message log')
    async def reset(self, interaction: discord.Interaction):
        """
        Clears the message log
        """

        # Reset the message log
        db.clear_message_log(interaction.user.id)

        # Send a response
        await interaction.response.send_message('Message log cleared')

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(AICommands(bot))