import discord
from discord import app_commands
from discord.ext import commands

class ModTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Create a color patch from a hex string
    @app_commands.command(name='strike', description='Give a user a strike')
    async def strike(self, interaction: discord.Interaction, user: discord.Member, reason: str):
        # Check if user has permission to use this command
        if not interaction.user.guild_permissions.kick_members:
            await interaction.response.send_message('You do not have permission to use this command!', ephemeral=True)
            return

        # Check which strike the user is on
        strike_count = 0
        for role in user.roles:
            if role.name == '1st Strike':
                strike_count = 1
            elif role.name == '2nd Strike':
                strike_count = 2
            elif role.name == '3rd Strike':
                strike_count = 3
        
        # Give the user a strike, add the role, remove the previous role, and send a message
        if strike_count == 0:
            await user.add_roles(discord.utils.get(interaction.guild.roles, name='1st Strike'))
            await user.remove_roles(discord.utils.get(interaction.guild.roles, name='Verified'))
            
            # Create embed
            embed = discord.Embed(
                title=f'Uh-oh!',
                color=discord.Color.red(),
                description=f"{user.mention} has been given a strike..."
            )
            embed.add_field(name='', value="*If you're seeing this, you did something deemed bad enough to warrant the usage of RickyJr's secret strike system.*", inline=False)
            embed.add_field(name='__Reason__', value=reason, inline=False)
            embed.add_field(name='__What does this mean?__', value=f"- You are now on much thinner ice.\n- You have lost access to certain channels such as quotes and memes\n- You can no longer speak in announcements\n- You can no longer create channels, emojis, or stickers", inline=False)
            embed.add_field(name="**__Any attempt to argue or complain about this strike will result in a 7 day mute.__**", value="", inline=False)
            embed.set_footer(text=f"{user.nick} (AKA {user.name}) now has 1 strike")

            # Send message
            await interaction.response.send_message(embed=embed, ephemeral=False)

        elif strike_count == 1:
            await user.add_roles(discord.utils.get(interaction.guild.roles, name='2nd Strike'))
            await user.remove_roles(discord.utils.get(interaction.guild.roles, name='1st Strike'))

            # Create embed
            embed = discord.Embed(
                title=f'Uh-oh!',
                color=discord.Color.red(),
                description=f"{user.mention} has been given a strike..."
            )
            embed.add_field(name='', value="*If you're seeing this, you did something deemed bad enough to warrant the usage of RickyJr's secret strike system.*", inline=False)
            embed.add_field(name='__Reason__', value=reason, inline=False)
            embed.add_field(name='__What does this mean?__', value=f"- You have lost access to the Minecraft server and will be banned from it if you attempt to join\n- You can no longer talk in any non-academic channels except for general\n- Your name is now permanently red", inline=False)
            embed.add_field(name="**__Any attempt to argue or complain about this strike will result in a permanent ban.__**", value="", inline=False)
            embed.set_footer(text=f"{user.nick} (AKA {user.name}) now has 2 strikes")

            # Send message
            await interaction.response.send_message(embed=embed, ephemeral=False)

        elif strike_count == 2:
            await user.add_roles(discord.utils.get(interaction.guild.roles, name='3rd Strike'))
            await user.remove_roles(discord.utils.get(interaction.guild.roles, name='2nd Strike'))

            # Create embed
            embed = discord.Embed(
                title=f'Uh-oh!',
                color=discord.Color.red(),
                description=f"{user.mention} has been locked out of all non-academic channels..."
            )
            embed.add_field(name='__Reason__', value=reason, inline=False)

            # Send message
            await interaction.response.send_message(embed=embed, ephemeral=False)

        else:
            await interaction.response.send_message("User already has 3 strikes! Maybe it's time for a ban...", ephemeral=True)
            return
        

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ModTools(bot))
