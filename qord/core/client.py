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
from qord.core.shard import Shard
from qord.exceptions import ClientSetupRequired

import asyncio
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
    shards_count: :class:`builtins.int`
        The number of shards to spawn for this client. It is recommended to omit this
        parameter and let the library fetch the ideal shards count automatically for you.
    connect_timeout: :class:`builtins.float`
        The number of seconds to wait for a shard to connect before timing out.
        Defaults to ``5``. Greater the integer, The longer it will wait and if
        a shard raises an error, It will take longer to raise it.
    heartbeat_ack_timeout: :class:`builtins.float`
        The number of seconds to wait for a heartbeat ack before attempting to
        reconnect the shard. This must be greater then 5. When omitted, Defaults to
        the :attr:`Shard.heartbeat_interval`.
    """
    if typing.TYPE_CHECKING:
        _rest: RestClient
        _shards_count: typing.Optional[int]
        _shards: typing.List[Shard]
        _max_concurrency: typing.Optional[int]
        _gateway_url: typing.Optional[str]
        _event_listeners: typing.Dict[str, typing.List[typing.Callable[..., typing.Any]]]

    def __init__(self,
        *,
        session: ClientSession = None,
        session_owner: bool = False,
        max_retries: int = 5,
        shards_count: int = None,
        connect_timeout: float = 5.0,
        heartbeat_ack_timeout: float = None,
    ) -> None:

        if shards_count is not None and shards_count < 1:
            raise ValueError("shards_count must be an integer greater then or equal to 1.")
        if heartbeat_ack_timeout is not None and heartbeat_ack_timeout < 5:
            raise ValueError("heartbeat_ack_timeout must be an integer greater then 5.")

        self._rest: RestClient = RestClient(
            session=session,
            session_owner=session_owner,
            max_retries=max_retries,
        )
        self._event_listeners = {}

        self.connect_timeout = connect_timeout
        self.heartbeat_ack_timeout = heartbeat_ack_timeout

        # Following are set during setup()
        self._shards_count = shards_count
        self._max_concurrency = None
        self._gateway_url = None
        self._shards = []

    @property
    def session(self) -> typing.Optional[ClientSession]:
        return self._rest.session

    @property
    def session_owner(self) -> bool:
        return self._rest.session_owner

    @property
    def max_retries(self) -> int:
        return self._rest.max_retries

    @property
    def shards_count(self) -> typing.Optional[int]:
        return self._shards_count

    @property
    def max_concurrency(self) -> typing.Optional[int]:
        r"""
        Returns
        -------
        Optional[:class:`builtins.int`]
            The maximum number of shards the client is allowed to start concurrently when
            :meth:`.launch` is called. This is set during :meth:`.setup`.

            This is retrieved from Discord and cannot be set by the user.
        """
        return self._max_concurrency

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

    def invoke_event(self, event_name: str, /, *args) -> None:
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
            loop.create_task(listener(*args))

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

    def is_setup(self) -> bool:
        r"""
        Returns
        -------
        :class:`builtins.bool`
            Indicates whether the client is setup.
        """
        return self._rest.token is not None

    async def setup(self, token: str, /) -> None:
        r"""Setups the client with the provided authorization token.

        This must be called before :meth:`.launch`. This setup fetches the
        shards count and spawns that many shards accordingly.

        Parameters
        ----------
        token: :class:`builtins.str`
            The token to setup the client with.

        Raises
        ------
        RuntimeError
            The client is already setup.
        HTTPException
            Setup failed. Most probably the provided token is invalid. Consider
            checking for HTTP status code using ``status`` attribute on
            :attr:`HTTPException.response` object.
        """
        if self._rest.token is not None:
            raise RuntimeError("Client is already setup.")

        self._rest.token = token

        try:
            gateway = await self._rest.get_bot_gateway()
        except Exception:
            # failed to fetch the gateway. This most likely
            # means that specified token is invalid so we want to
            # ensure that token unsets properly.
            self._rest.token = None
            raise

        self._gateway_url = gateway["url"] + "?v=9&encoding=json&compress=zlib-stream"
        self._max_concurrency = gateway["session_start_limit"]["max_concurrency"]

        if self._shards_count is None:
            self._shards_count = gateway["shards"]

        # spawn the shards
        self._shards = [
            Shard(id=shard_id, client=self)
            for shard_id in range(self._shards_count) # type: ignore
        ]

    async def launch(self) -> None:
        r"""Launches the bot.

        This method should be called *after* :meth:`.setup`.

        Raises
        ------
        :class:`ClientSetupRequired`
            The client is not setup yet. See :meth:`.setup` for more info.
        """
        if self._rest.token is None:
            raise ClientSetupRequired("Client is not setup yet. Call Client.setup() first.")

        loop = asyncio.get_running_loop()

        shards = self._shards.copy()

        _LOGGER.info(
            "Launching %s shards (%s shard%s concurrently per 5 seconds)",
            self._shards_count,
            self._max_concurrency,
            's' if self._max_concurrency > 1 else '',
        )
        exc_queue = asyncio.Queue()

        while shards:
            # The _max_concurrency attribute is never None here.
            # Starting '_max_concurrency' number of shards every
            # 5 seconds.

            waiters = []

            for i in range(self._max_concurrency): # type: ignore
                try:
                    shard = shards[0]
                except IndexError:
                    # no more shards
                    break
                else:
                    shard._worker_task = loop.create_task(
                        shard._wrapped_launch(self._gateway_url, exc_queue), # type: ignore
                        name=f"shard-worker:{shard._id}"
                    )
                    shards.remove(shard)
                    waiters.append(shard._identified.wait())

            # Ensure that all shards properly identify before delaying.
            for waiter in waiters:
                try:
                    await asyncio.wait_for(waiter, timeout=self.connect_timeout)
                except asyncio.TimeoutError:
                    # Timed out waiting for a shard to start.
                    _LOGGER.error("Timed out waiting for a shard to start. Crashing.")

                    # Check if we have an error in the queue
                    try:
                        exc = exc_queue.get_nowait()
                    except asyncio.QueueEmpty as exc:
                        raise TimeoutError("Timed out waiting for a shard to connect.") from exc
                    else:
                        raise exc

            await asyncio.sleep(5)

        # block until one of the shards crash
        exc = await exc_queue.get()
        raise exc

    async def close(self, clear_setup: bool = True) -> None:
        r"""Gracefully closes the client.

        The entire closing process includes:

        - Gracefully closing all the spawned shards.
        - Closing the HTTP session.
        - Resetting the client setup.

        Parameters
        ----------
        clear_setup: :class:`builtins.bool`
            Whether to clear the client setup. Defaults to ``True``.

            If set to ``False``, Client setup will not be closed and there
            will be no need of calling :meth:`.setup` again.
        """
        for shard in self._shards:
            await shard._close(code=1000, _clean=True)

        await self._rest.close()

        if clear_setup:
            self._rest.token = None
            self._max_concurrency = None
            self._shards.clear()

    def start(self, token: str) -> None:
        r"""Setups the client with provided token and then starts it.

        Unlike :meth:`.launch`, This method is not a coroutine and aims to
        abstract away the asyncio event loop handling from the user. For a
        granular control over the event loop, Consider using :meth:`.setup` and
        :meth:`.launch`

        Parameters
        ----------
        token: :class:`builtins.str`
            The token to setup the client with.

        Raises
        ------
        HTTPException
            Startup failed. Most probably the provided token is invalid. Consider
            checking for HTTP status code using ``status`` attribute on
            :attr:`HTTPException.response` object.
        """
        async def launcher():
            await self.setup(token)
            await self.launch()

        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()

        try:
            loop.run_until_complete(launcher())
        except KeyboardInterrupt:
            loop.run_until_complete(self.close())
        finally:
            loop.close()