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

from qord.core.rest import RestClient

import logging
import typing

if typing.TYPE_CHECKING:
    from aiohttp import ClientSession

__all__ = (
    "Client",
)

_LOGGER = logging.getLogger(__name__)

class Client:
    r"""A client that interacts with Discord API.

    This is the core class of this library and the main starter point for
    every bot. All parameters passed during initializing are optional and keyword only.

    This is a basic example using this class to build a "Ping Pong" bot::

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

    Parameters
    ----------
    session: :class:`aiohttp.ClientSession`
        The client session used for making HTTPs requests. If omitted, Library
        will initalize a session internally.
    session_owner: :class:`builtins.bool`
        Whether the :attr:`.session` is owned by the user, If set to ``True``,
        The session will not be closed upon bot's close. Defaults to ``False``.
    max_retries: :class:`builtins.int`
        The maximum number of re-tries for an unexpectedly failed HTTP request before
        raising :class:`HTTPException`. This integer cannot be less than 0 and greater
        than 5.
    """

    def __init__(self,
        *,
        session: ClientSession,
        session_owner: bool = False,
        max_retries: int = 5,
    ) -> None:

        self._rest = RestClient(
            session=session,
            session_owner=session_owner,
            max_retries=max_retries,
        )

    @property
    def session(self) -> typing.Optional[ClientSession]:
        return self._rest.session

    @property
    def session_owner(self) -> bool:
        return self._rest.session_owner

    @property
    def max_retries(self) -> int:
        return self._rest.max_retries
