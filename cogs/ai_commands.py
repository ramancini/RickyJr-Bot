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
ASSISTANT_ID = os.getenv('ASSISTANT_ID')

# Create the OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Retreive the assistant from the OpenAI API
assistant = client.beta.assistants.retrieve(ASSISTANT_ID)

# Create the database operations object
db = dbf.DatabaseOperations()

# Read in the system prompt from prompt.json
with open('data/prompt.json') as f:
    PROMPT = json.load(f)

class AICommands(commands.GroupCog, group_name='ai', group_description='Commands to interact with ChatGPT'):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='chat', description='Talk with ChatGPT')
    async def chat(self, interaction: discord.Interaction, message: str):
        """
        Sends a message to ChatGPT and returns the response in discord
        """
        await interaction.response.defer()
        
        # Get the thread id for a user / setup thread for user
        user_thread_id = db.get_thread(interaction.user.id)

        if user_thread_id is None:
            user_thread = client.beta.threads.create()
            db.add_thread(interaction.user.id, user_thread.id)
        
        # Send message to the thread
        user_thread_msg = client.beta.threads.messages.create(
            thread_id=user_thread_id,
            content=message
        )

        # Run the thread
        user_thread_run = client.beta.threads.runs.create(
            thread_id=user_thread_id,
            assistant_id=ASSISTANT_ID
        )

        # Send the response
        await interaction.followup.send("Done!", ephemeral=True)
    
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