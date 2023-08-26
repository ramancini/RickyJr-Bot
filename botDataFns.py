import os
import json
from dotenv import load_dotenv
import collections

load_dotenv(dotenv_path='data/.env')
DEV_ID = os.getenv('DEV_ID')
GUILD_ID = os.getenv('GUILD_ID')


class SettingsFile:
    """
    An object which makes reading and working with the settings file for the bot easier
    """

    def __init__(self):
        # Prevent "re-loading"
        self.file_loaded = False

        # Default settings file path
        self.file_name = 'data/settings.json'

        # Set default settings
        self.default_prefix = '!'
        self.default_admin_role = None
        self.default_auto_role_id = None

        # Load preexisting data (if it exists, otherwise create it)
        self.data = self.load()

    def load(self) -> collections.defaultdict:
        """
        Load the settings.json file

        :return: A dictionary with settings for each unique discord server
        """
        global GUILD_ID

        # Set default json values
        default_dictionary = {
            'prefix': self.default_prefix,
            'admin_role': self.default_admin_role,
            'auto_role_id': self.default_auto_role_id,
        }

        # Check if the file exists / create settings.json
        if not os.path.exists(self.file_name):
            data = collections.defaultdict(lambda: default_dictionary)
            data[GUILD_ID].update()

            # Create the default file in directory
            with open(self.file_name, 'w') as f:
                json.dump(data, f)
        else:
            file = open(self.file_name)
            data = collections.defaultdict(lambda: default_dictionary, json.load(file))

        # File loaded, prevent "re-loading"
        self.file_loaded = True

        return data

    def save(self):
        """
        Save data to the settings file
        """
        with open(self.file_name, 'w') as f:
            json.dump(self.data, f)

    def server_prefix_get(self, guild_id) -> str:
        """
        Return the prefix that a bot uses for calling commands for a given discord server

        :param guild_id: The ID of the server whose prefix is being changed
        :return:         The prefix for calling bot commands
        """
        if not self.file_loaded:
            self.load()

        return self.data[str(guild_id)]['prefix']

    def server_prefix_set(self, guild_id, prefix):
        """
        Changes the prefix that the bot uses for calling commands for a given discord server

        :param guild_id: The ID of the server whose prefix is being changed
        :param prefix:   The prefix for calling bot commands
        """
        if not self.file_loaded:
            self.load()

        self.data[str(guild_id)]['prefix'] = prefix
        self.save()

    def server_admin_role_get(self, guild_id) -> int:
        """
        Changes the role in a given server which will have the ability to use the "administrator commands" in the discord bot

        :param guild_id: The ID of the server whose admin role is being changed
        :return: The ID of the role which will be able to use bot admin commands
        """
        if not self.file_loaded:
            self.load()

        return self.data[str(guild_id)]['admin_role_id']

    def server_admin_role_set(self, guild_id, admin_role_id):
        """
        Changes the role in a given server which will have the ability to use the "administrator commands" in the discord bot

        :param guild_id: The ID of the server whose admin role is being changed
        :param admin_role_id: The ID of the role which will be able to use bot admin commands
        """
        if not self.file_loaded:
            self.load()

        self.data[str(guild_id)]['admin_role_id'] = admin_role_id
        self.save()

    def server_auto_role_get(self, guild_id) -> int:
        """
        Set the role automatically assigned to new members that join a given server

        :param guild_id: The ID of the server whose admin role is being changed
        :return: The ID of the role that is automatically assigned to new members
        """
        if not self.file_loaded:
            self.load()

        return self.data[str(guild_id)]["auto_role_id"]

    def server_auto_role_set(self, guild_id, auto_role_id):
        """
        Set the role automatically assigned to new members that join a given server

        :param guild_id: The ID of the server whose admin role is being changed
        :param auto_role_id: The ID of the role that is automatically assigned to new members
        """
        if not self.file_loaded:
            self.load()

        self.data[str(guild_id)]["auto_role_id"] = auto_role_id
        self.save()
