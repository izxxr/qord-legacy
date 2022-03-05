# Qord
Python library for Discord API based around asyncio.

**Features:**

- Object oriented, user friendly interface with no dirty payloads.
- Properly typed according to [PEP-484](https://www.python.org/dev/peps/pep-0484/)
- Easy to customise and manage.
- Supports automatic gateway sharding.
- Supports custom implementation of caching. 

## Alpha phase
Qord is currently under it's development (alpha) stage. This means that some features may be missing or potentially incomplete and furthermore, broken.

Qord currently supports the basic functionalities required to build a bot however many essential features are yet to be implemented. For this reason, Qord isn't yet a library to choose for making full fledged bots. The library would be in a decently stable and production ready state when it reaches the 1.0 version (The first stable version).

## Installation
Qord is installed using Python's traditional package manager, pip.
```bash
pip install -U qord
```
> ℹ️ On Windows and Mac, you might need to prefix the above command with `python -m` for it work.

Qord requires **Python 3.8 or higher.** The dependencies are handled by pip automatically, See complete list of dependencies in [here](https://github.com/nerdguyahmad/qord/blob/main/requirements.txt).

## Usage
To whet your appetite, Let's get a quickstart with an example of a simple "Ping-Pong" bot.
```py
import qord

client = qord.Client()

@client.event(qord.GatewayEvent.READY)
async def on_ready(event):
  print("Bot is ready.")
  print(f"Shards: {client.shards_count}")
  print(f"User: {client.user.proper_name}")
  print(f"Guilds: {len(client.cache.guilds())}")

@client.event(qord.GatewayEvent.MESSAGE_CREATE)
async def on_message_create(event):
  message = event.message
	
  if message.author.bot:
    # Don't respond to bot messages.
    return
	
  if message.content == "!ping":
    await message.channel.send("Pong!")

client.start("BOT_TOKEN")
```

## Contributing
Qord is under heavy development. You can help us in reaching 100% coverage of Discord API by reporting bugs, suggesting features or even directly contributing to the code base, See [Contribution Guidelines](https://github.com/nerdguyahmad/qord/blob/main/CONTRIBUTING.MD).

----

<br>
<div align="center">
  <a href="https://qord.rtfd.io">Documentation</a> • <a href="https://discord.gg/nE9cGtzayA">Discord Server</a> • <a href="https://pypi.org/project/qord">PyPi</a> 
  • <a href="https://github.com/nerdguyahmad/qord">GitHub</a> • <a href="https://github.com/nerdguyahmad/qord/issues">Issues Tracker</a>
  <br><br>
  <sup>Copyright (C) nerdguyahmad and contributors 2022, Under the MIT license.</sup>
</p>
