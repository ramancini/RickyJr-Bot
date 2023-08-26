import discord
from discord import app_commands
from discord.ext import commands
from discord import ui
import botDataFns

settings_file = botDataFns.SettingsFile()


async def role_check(interaction: discord.Interaction) -> bool:
    """
    Check if user has admin role

    :param interaction: Discord interaction to check
    :return: True if user has admin role, false if user does not have admin role or no admin role set
    """
    admin_role = settings_file.server_admin_role_get(interaction.guild_id)
    owner_id = interaction.guild.owner_id
    if admin_role is None:
        if interaction.user.id == owner_id:
            return True
        else:
            await interaction.response.send_message("You do not have permission to do this.", ephemeral=True)
            return False
    else:
        if interaction.user.get_role(admin_role) is None:
            await interaction.response.send_message("You do not have permission to do this.", ephemeral=True)
            return False
        else:
            return True


class AdminRole(commands.GroupCog, group_name='adminrole', group_description='Commands to set the role which can run bot admin commands'):
    """
    Group for automatically applied user role app commands
    """

    def __init__(self, bot):
        self.bot = bot

    # set
    @app_commands.command(name='set', description='Set the role which can run admin commands')
    @app_commands.check(role_check)
    async def set(self, interaction: discord.Interaction, role: discord.Role):
        """
        Set the role which can run admin commands

        :param interaction: The Discord interaction
        :param role: Role to set the admin role to
        """
        settings_file.server_admin_role_set(interaction.guild_id, role.id)
        await interaction.response.send_message(f'Set the admin role to {role.mention}')

    # get
    @app_commands.command(name='get', description='See which role can run admin commands')
    @app_commands.check(role_check)
    async def get(self, interaction: discord.Interaction):
        """
        Send a response to interaction with the currently set role which can run admin commands

        :param interaction: Discord interaction
        """
        role_id = settings_file.server_admin_role_get(interaction.guild_id)

        if role_id is None:
            await interaction.response.send_message('There is no currently set admin role. Set one with `/adminrole set`')
        else:
            role = interaction.guild.get_role(role_id)
            await interaction.response.send_message(f'Current admin role is {role.mention}')


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(AdminRole(bot))
