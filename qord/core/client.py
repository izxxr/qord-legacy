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
import asyncio

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
        raising :class:`HTTPException`. This integer cannot be less than 5. ``None``
        or ``0`` means no retries should be done.
    """
    if typing.TYPE_CHECKING:
        _rest: RestClient
        _event_listeners: typing.Dict[str, typing.List[typing.Callable[..., typing.Any]]]

    def __init__(self,
        *,
        session: ClientSession = None,
        session_owner: bool = False,
        max_retries: int = 5,
    ) -> None:

        self._rest: RestClient = RestClient(
            session=session,
            session_owner=session_owner,
            max_retries=max_retries,
        )
        self._event_listeners = {}

    @property
    def session(self) -> typing.Optional[ClientSession]:
        return self._rest.session

    @property
    def session_owner(self) -> bool:
        return self._rest.session_owner

    @property
    def max_retries(self) -> int:
        return self._rest.max_retries

    def get_event_listeners(self, event_name: str, /) -> typing.List[typing.Callable[..., typing.Any]]:
        r"""Gets the list of all events listener for the provided event.

        Parameters
        ----------
        event_name: :class:`builtins.str`
            The name of event to get listeners for.

        Returns
        -------
        The list of event listeners.
        """
        return self._event_listeners.get(event_name, [])

    def clear_event_listeners(self, event_name: str, /) -> typing.List[typing.Callable[..., typing.Any]]:
        r"""Clears all events listener for the provided event.

        Parameters
        ----------
        event_name: :class:`builtins.str`
            The name of event to clear listeners for.

        Returns
        -------
        The list of removed event listeners.
        """
        return self._event_listeners.pop(event_name, [])

    def walk_event_listeners(self) -> typing.List[typing.Tuple[str, typing.List[typing.Callable[..., typing.Any]]]]:
        r"""Returns a list of tuples with first element being event name and second
        element being the list of event listeners for that event.

        Example::

            for name, listeners in client.walk_event_listeners():
                print(name, listeners)
        """
        return list(self._event_listeners.items())

    def register_event_listener(self, event_name: str, callback: typing.Callable[..., typing.Any], /) -> None:
        r"""Registers an event listener for provided event.

        Parameters
        ----------
        event_name: :class:`builtins.str`
            The name of event to register listener for.
        callback:
            The callback listener. This must be a coroutine.
        """
        if not asyncio.iscoroutinefunction(callback):
            raise TypeError("Parameter 'callback' must be a coroutine.")

        try:
            self._event_listeners[event_name].append(callback)
        except KeyError:
            self._event_listeners[event_name] = [callback]

    def invoke_event(self, event_name: str, *args, /) -> None:
        r"""Invokes an event by calling all of it's listeners.

        Parameters
        ----------
        event_name: :class:`builtins.str`
            The name of event to invoke.
        *args: :class:`BaseEvent`
            The arguments to pass to listeners.
        """
        listeners = self._event_listeners.get(event_name)

        if not listeners:
            return

        loop = asyncio.get_running_loop()

        for listener in listeners:
            loop.create_task(*args)

    def event(self, event_name: str):
        r"""A decorator that registers an event listener for provided event.

        The decorated function must be a coroutine. Example::

            @client.event(qord.GatewayEvents.MESSAGE_CREATE)
            async def on_message_create(event):
                ...

        Parameters
        ----------
        event_name: :class:`builtins.str`
            The name of event to register listener for.
        """
        def wrap(func):
            self.register_event_listener(event_name, func)
            return func

        return wrap
