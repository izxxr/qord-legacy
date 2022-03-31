"""
Basic Usage
~~~~~~~~~~~

This example showcases the basic usage of the library by implementing a simple
ping-pong bot that responds to messages.

This example considers that you already have a bot user configured with message
content privileged intent enabled. If not, consider doing that first.

NOTE: Typehints are not required, they are only specified for convenience and may be omitted.
"""

import qord

# Intents.unprivileged() creates Intents instance with all unprivileged intents enabled
# Intents in short words, allow you to subscribe or unsubscribe to certain gateway events
# Filtering unnecessary intents is out of scope of this simple example.
intents = qord.Intents.unprivileged()

# We need message content intent enabled in order to respond to
# message content. It is a privileged intent and requires explicit
# enabling from Developers portal application page.
#
# WARNING: If not explicitly enabled, An error will be raised upon starting
# the client.
intents.message_content = True

# Instansiating our Client instance
client = qord.Client(intents=intents)

# event() decorator registers an event listener for the given event. In this case, READY.
# READY event is fired whenever client connects and becomes ready.
# We are registering this event listener as a notification of client
# becoming ready by printing to console.
@client.event(qord.GatewayEvent.READY)
async def on_ready(event: qord.events.Ready):
    print(f"Connected as {client.user.proper_name}")

# MESSAGE_CREATE event is fired whenever we have a new message
# sent by someone in a channel. This is for our commands handling.
@client.event(qord.GatewayEvent.MESSAGE_CREATE)
async def on_message_create(event: qord.events.MessageCreate):
    message = event.message

    if message.author.bot or not message.content:
        # We don't want to handle messages that are sent
        # by a bot or don't have any content, so return
        # This clause already handles the case of responding
        # to our own message and causing an infinite loop, if
        # you remove this if statement consider adding one to
        # ignore messages from ourselves and potentially running
        # into an infinite loop.
        return

    # Commands handling
    if message.content == "?ping":
        await message.channel.send(f"{message.author.proper_name} used `?ping`: Pong :ping_pong:")

# Start our client
# This method blocks until the client is not stopped.
# For that reason, All events listeners and other pre-processing must be done
# before this method's call.
client.start("BOT_TOKEN_HERE")