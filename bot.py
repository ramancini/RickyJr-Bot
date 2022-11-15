import logging
import os
from dotenv import load_dotenv
import discord
from discord import app_commands

import re
import numpy as np
import PIL
from PIL import Image
from io import BytesIO

# Set up logging
handler = logging.FileHandler(filename='data/bot.log', encoding='utf-8', mode='w')
dt_fmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
handler.setFormatter(formatter)

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

# Load environment variables
load_dotenv(dotenv_path='data/.env')
TOKEN = os.getenv('TOKEN')
GUILD_ID = os.getenv('GUILD_ID')
DEV_ID = os.getenv('DEV_ID')

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

# Hex String to RGB converter
def hex_to_rgb(hex):
    hex = hex.lstrip('#')
    hlen = len(hex)
    return tuple(int(hex[i:i+hlen//3], 16) for i in range(0, hlen, hlen//3))

# Convert RGB to a 128 by 128 image
def rgb_to_image(rgb):
    img = PIL.Image.new('RGB', (256, 256), color=rgb)
    return img

# Create client and command tree
client = AClient()
tree = app_commands.CommandTree(client)

# Create command to display color patch based on hex code
@tree.command(name='hex2color', description='Display a color patch based on a hex code')
async def hex2color(interaction: discord.Interaction, hexcode: str):
    # Check if hexcode is valid
    if not re.match("^(#)?([A-Fa-f0-9]){6}$", hexcode):
        await interaction.response.send_message('That is not a valid hex code!', ephemeral=True)
        return

    # Check if hexcode has a # in front
    if hexcode[0] != '#':
        hexcode = '#' + hexcode

    # Convert hex to RGB
    rgb = hex_to_rgb(hexcode)

    # Create image
    img = rgb_to_image(rgb)

    with BytesIO() as image_binary:
        img.save(image_binary, 'PNG')
        image_binary.seek(0)

        # Create embed
        embed = discord.Embed(
            title=f'Generated color patch for {hexcode}',
            color=discord.Color.from_rgb(*rgb),
        )
        embed.add_field(name='RGB Color Code', value=f'{rgb[0]}, {rgb[1]}, {rgb[2]}')
        embed.add_field(name='Hex Color Code', value=hexcode)

        embed.set_image(url='attachment://color.png')

        # Send embed
        await interaction.response.send_message(embed=embed, file=discord.File(fp=image_binary, filename='color.png'))

# Create command to display color patch based on RGB code
@tree.command(name='rgb2color', description='Display a color patch based on RGB values')
async def rgb2color(interaction: discord.Interaction, r: int, g: int, b: int):
    # Check if RGB values are valid
    if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
        await interaction.response.send_message('That is not a valid RGB code!', ephemeral=True)
        return

    # Convert RGB to hex
    hexcode = '#%02x%02x%02x' % (r, g, b)

    # Create image
    img = rgb_to_image((r, g, b))

    with BytesIO() as image_binary:
        img.save(image_binary, 'PNG')
        image_binary.seek(0)

        # Create embed
        embed = discord.Embed(
            title=f'Generated color patch for ({r}, {g}, {b})',
            color=discord.Color.from_rgb(r, g, b),
        )
        embed.add_field(name='RGB Color Code', value=f'{r}, {g}, {b}')
        embed.add_field(name='Hex Color Code', value=hexcode)

        embed.set_image(url='attachment://color.png')

        # Send embed
        await interaction.response.send_message(embed=embed, file=discord.File(fp=image_binary, filename='color.png'))

# Start the bot
if __name__ == '__main__':
    logger.info("Starting!")
    client.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)
