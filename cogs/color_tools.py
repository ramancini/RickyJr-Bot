import discord
from discord import app_commands
from discord.ext import commands

import PIL
from PIL import Image
import re
from io import BytesIO


# Hex String to RGB converter
def hex_to_rgb(hex):
    hex = hex.lstrip('#')
    hlen = len(hex)
    return tuple(int(hex[i:i + hlen // 3], 16) for i in range(0, hlen, hlen // 3))


# Convert RGB to a 128 by 128 image
def rgb_to_image(rgb):
    img = PIL.Image.new('RGB', (256, 256), color=rgb)
    return img


# Convert RGB to HSV
def rgb_to_hsv(rgb):
    r, g, b = rgb
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    cmax = max(r, g, b)
    cmin = min(r, g, b)
    diff = cmax - cmin
    if cmax == cmin:
        h = 0
    elif cmax == r:
        h = (60 * ((g - b) / diff) + 360) % 360
    elif cmax == g:
        h = (60 * ((b - r) / diff) + 120) % 360
    elif cmax == b:
        h = (60 * ((r - g) / diff) + 240) % 360
    if cmax == 0:
        s = 0
    else:
        s = (diff / cmax) * 100
    v = cmax * 100
    return h, s, v


class ColorTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Create a color patch from a hex string
    @app_commands.command(name='hex2color', description='Display a color patch based on a hex code')
    async def hex2color(self, interaction: discord.Interaction, hexcode: str):
        # Check if hexcode is valid
        if not re.match("^(#)?([A-Fa-f0-9]){6}$", hexcode):
            await interaction.response.send_message('That is not a valid hex code!', ephemeral=True)
            return

        # Check if hexcode has a # in front
        if hexcode[0] != '#':
            hexcode = '#' + hexcode

        # Convert hex to RGB
        rgb = hex_to_rgb(hexcode)

        # Convert RGB to HSV
        hsv = rgb_to_hsv(rgb)

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
            embed.add_field(name='RGB Color Code',
                            value=f'```R: {rgb[0]}\nG: {rgb[1]}\nB: {rgb[2]}```')
            embed.add_field(name='HSV Color Code',
                            value=f'```H: {round(hsv[0], 3)}°\nS: {round(hsv[1], 3)}%\nV: {round(hsv[2], 3)}%```')
            embed.add_field(name='Hex Color Code',
                            value=hexcode)

            embed.set_image(url='attachment://color.png')

            # Send embed
            await interaction.response.send_message(embed=embed, file=discord.File(fp=image_binary, filename='color.png'))

    # Create a color patch from RGB values
    @app_commands.command(name='rgb2color', description='Display a color patch based on RGB values')
    async def rgb2color(self, interaction: discord.Interaction, r: int, g: int, b: int):
        # Check if RGB values are valid
        if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
            await interaction.response.send_message('That is not a valid RGB code!', ephemeral=True)
            return

        # Convert RGB to hex
        hexcode = '#%02x%02x%02x' % (r, g, b)

        # Convert RGB to HSV
        hsv = rgb_to_hsv((r, g, b))

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
            embed.add_field(name='RGB Color Code', value=f'```R: {r}\nG: {g}\nB: {b}```')
            embed.add_field(name='HSV Color Code',
                            value=f'```H: {round(hsv[0], 3)}°\nS: {round(hsv[1], 3)}%\nV: {round(hsv[2], 3)}%```')
            embed.add_field(name='Hex Color Code', value=hexcode)

            embed.set_image(url='attachment://color.png')

            # Send embed
            await interaction.response.send_message(embed=embed, file=discord.File(fp=image_binary, filename='color.png'))

    # Create a color patch from HSV values
    @app_commands.command(name='hsv2color', description='Display a color patch based on HSV values')
    async def hsv2color(self, interaction: discord.Interaction, h: float, s: float, v: float):
        # Check if HSV values are valid
        if not (0 <= h <= 360 and 0 <= s <= 100 and 0 <= v <= 100):
            await interaction.response.send_message('That is not a valid HSV code!', ephemeral=True)
            return

        # Convert HSV to RGB
        c = v * s
        x = c * (1 - abs((h / 60) % 2 - 1))
        m = v - c

        if 0 <= h < 60:
            r, g, b = c, x, 0
        elif 60 <= h < 120:
            r, g, b = x, c, 0
        elif 120 <= h < 180:
            r, g, b = 0, c, x
        elif 180 <= h < 240:
            r, g, b = 0, x, c
        elif 240 <= h < 300:
            r, g, b = x, 0, c
        elif 300 <= h < 360:
            r, g, b = c, 0, x
        else:
            r, g, b = 0, 0, 0

        r, g, b = int((r + m) * 255), int((g + m) * 255), int((b + m) * 255)

        # Convert RGB to hex
        hexcode = '#%02x%02x%02x' % (r, g, b)

        # Create image
        img = rgb_to_image((r, g, b))

        with BytesIO() as image_binary:
            img.save(image_binary, 'PNG')
            image_binary.seek(0)

            # Create embed
            embed = discord.Embed(
                title=f'Generated color patch for ({h}°, {s}%, {v}%)',
                color=discord.Color.from_rgb(r, g, b),
            )
            embed.add_field(name='RGB Color Code', value=f'```R: {r}\nG: {g}\nB: {b}```')
            embed.add_field(name='HSV Color Code', value=f'```H: {round(h, 3)}°\nS: {round(s, 3)}%\nV: {round(v, 3)}%```')
            embed.add_field(name='Hex Color Code', value=hexcode)

            embed.set_image(url='attachment://color.png')

            # Send embed
            await interaction.response.send_message(embed=embed, file=discord.File(fp=image_binary, filename='color.png'))

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ColorTools(bot))
