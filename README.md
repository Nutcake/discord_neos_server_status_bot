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
Start the bot with the following command:
`poetry run python src/main.py`

# Usage
With the bot running you can send UDP packets containing positive integers to the specified host:port combination to update the displayed playercount.
