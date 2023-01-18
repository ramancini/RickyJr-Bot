# RickyJr Bot
RickyJr is an Imaging Science discord bot, designed to do a variety of simple Imaging Science tasks. 

It is currently in development. Contributions are more than welcome!

## Features

A list of all commands and features will be able to be found on the GitHub wiki in the future.

## Important Information

### Required Intents

- [ ] Presence Intent
- [ ] Server Members Intent
- [ ] Message Content Intent

### Required Scopes

- [ ] bot
- [ ] applications.commands

### Required Permissions

*It is recommended that you give RickyJr Administrator permissions to be safe, but if you are wary of giving the bot administrator permissions, here is a list of the required permissions that need to be enabled in your bot's settings:*

- [ ] Send Messages
- [ ] Send Messages in Threads
- [ ] Manage Messages
- [ ] Embed Links
- [ ] Attach Files
- [ ] Use External Emojis
- [ ] Add Reactions
- [ ] Use Slash Commands

## Guide for Setting Up the Bot
### Creating the bot
*Made using python 3.9.13*

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications) and create a new application.
2. After entering a name for your application, click on the "Bot" tab.
3. Click on "Add Bot" and confirm.
4. Click on "Reset Token" and **make sure to copy the token**.
5. Go to the "Privileged Gateway Intents" tab and enable "Presence Intent", "Server Members Intent", and "Message Content Intent".
6. Go to the "OAuth2" tab and select the following scopes:
    * bot
    * applications.commands
7. Under "Bot Permissions", select the following permissions:
    * Send Messages
    * Send Messages in Threads
    * Manage Messages
    * Embed Links
    * Attach Files
    * Use External Emojis
    * Add Reactions
    * Use Slash Commands
8. Copy the link and open it in a new tab. Select the server you want to add the bot to and click "Authorize".

### Running the bot

1. Clone the repository with the following command:
    ```bash
    git clone https://github.com/ramancini/RickyJr-Bot.git
    ```
2. Create a file called `.env` in the directory labeled `data` in the repository.
3. Add the following lines to the `.env` file:
    ```bash
    TOKEN=<your bot token>
    GUILD_ID=<your discord server id>
    DEV_ID=<your discord user id>
    APPLICATION_ID=<your discord application id>
    ```

*This bot was set up using Pebblehost as a host.*

## Acknowledgements

- ### Robert Mancini (*Creator*)
    - Email: [bam3869@rit.edu](mailto:bam3869@rit.edu)
        - *You can also contact me at: [ramancini04@gmail.com](mailto:ramancini04@gmail.com)*
    - GitHub profile: [ramancini](https://github.com/ramancini)
    - Discord: `King_Nerp#9999`

## License

Copyright (c) 2022 - Robert Mancini

> This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.  
> 
> This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for more details.
> 
> You should have received a copy of the GNU Affero General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.