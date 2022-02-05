# MIT License

# Copyright (c) 2022 Izhar Ahmad

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import annotations

import typing

__all__ = (
    "Client",
)


class Client:
    r"""A client that interacts with Discord API.

    This is the core class of this library and the main starter point for
    every bot. All parameters passed during initializing are optional and keyword only.

    Common functionality of the class is summarised below:

    - The class should be initialized once only.
    - Events listeners are registered using :meth:`.event` decorator.
    - :meth:`.start` is used to setup the client and launch it. It must be called after \
        all the events listeners are registered as it is a blocking function.

    This is a basic example that describes above points::

        import qord

        client = qord.Client()

        @client.event(qord.GatewayEvents.MESSAGE_CREATE)
        async def on_message_create(event):
            message = event.message

            if message.author.is_me():
                # Don't respond to ourselves.
                return

            if message.content == "!ping":
                await message.channel.send_message("🏓 Pong!")

        if __name__ == "__main__":
            client.start(BOT_TOKEN)
    """

    def __init__(self) -> None:
        pass
