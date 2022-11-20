.. _getting-started:

Getting Started
===============

This short section describes the installation process and basic usage of the library.

Installation
------------

Qord is installed using Python's traditional package manager, pip::

   python -m pip install -U qord

Qord requires **Python 3.8 or higher.** The dependencies are handled by pip automatically,
See complete list of dependencies in `here <https://github.com/izxxr/qord/blob/main/requirements.txt>`_.

Usage
-----

To whet your appetite, Let's get a quickstart with an example of a simple "Ping-Pong" bot::

   import qord

   intents = qord.Intents.unprivileged()
   intents.message_content = True
   client = qord.Client(intents=intents)

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
