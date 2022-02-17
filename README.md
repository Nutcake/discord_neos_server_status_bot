# discord_neos_server_status_bot
A simple Discord bot to display a playercount for a NeosVR server (or any server, really).

# Setup

This project requires poetry for dependency management, see installation guide [here](https://python-poetry.org/docs/).

```bash
$ git clone https://github.com/Nutcake/discord_neos_server_status_bot
$ cd discord_neos_server_status_bot
$ poetry install
```

# Config
Discord bots needs a valid bot-token, see https://discord.com/developers to create an application and bot.

Set the `token`-field in the config.ini file to contain your token and change the default host and port if needed.

# Running
Start the bot using poetry:

`poetry run python src/main.py`

# Usage
With the bot running you can send a HTTP-POST request containing a positive integer to the specified host:port combination to update the displayed playercount.

## Node Setup
Put this Node-Setup anywhere in your world and adjust the address to point to the IP and port where the bot is running.  
![node-setup](https://user-images.githubusercontent.com/10452593/154491422-f5eebd88-f400-4bfc-9ca6-2159dea04f73.jpg)
Note: It is probably a good idea to run this server on the same host as the actual Neos instance and to keep the selected port closed to the public for security reasons.
