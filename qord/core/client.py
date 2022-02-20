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

from qord.core.dispatch import DispatchHandler
from qord.core.rest import RestClient
from qord.core.shard import Shard
from qord.core.cache_impl import DefaultCache, DefaultGuildCache
from qord.exceptions import ClientSetupRequired
from qord.flags.intents import Intents
from qord.models.users import User
from qord.models.guilds import Guild

import asyncio
import logging
import traceback
import typing

if typing.TYPE_CHECKING:
    from aiohttp import ClientSession
    from qord.models.users import ClientUser
    from qord.core.cache import Cache, GuildCache


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

        @client.event(qord.GatewayEvent.MESSAGE_CREATE)
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
    ready_timeout: :class:`builtins.float`
        The number of seconds to wait for lazy loading guilds cache initially before
        dispatching the ready event. Defaults to ``2``. Note that setting a very small
        timeout would cause ready event to fire with incomplete cache or setting
        too large value will increase the startup time.
    debug_events: :class:`builtins.bool`
        Whether to enable debug events. Defaults to ``False``.
    intents: :class:`Intents`
        The intents for this client. By default, Only unprivileged intents are
        enabled using :meth:`Intents.unprivileged` method.
    cache: :class:`Cache`
        The cache handler to use for the client. If not provided, Defaults to
        :class:`DefaultCache`.
    """
    if typing.TYPE_CHECKING:
        _event_listeners: typing.Dict[str, typing.List[typing.Callable[..., typing.Any]]]

    def __init__(self,
        *,
        session: ClientSession = None,
        session_owner: bool = False,
        max_retries: int = 5,
        shards_count: int = None,
        debug_events: bool = False,
        connect_timeout: float = 5.0,
        ready_timeout: float = 2.0,
        intents: Intents = None,
        cache: Cache = None,
    ) -> None:

        if shards_count is not None and shards_count < 1:
            raise ValueError("Parameter shards_count must be an integer greater then or equal to 1.")
        if cache is not None and not isinstance(cache, Cache):
            raise TypeError("Parameter cache must be an instance of Cache. Not %r" % cache.__class__)

        self._rest: RestClient = RestClient(
            session=session,
            session_owner=session_owner,
            max_retries=max_retries,
        )
        self._cache: Cache = cache or DefaultCache()
        self._dispatch: DispatchHandler = DispatchHandler(
            client=self,
            ready_timeout=ready_timeout,
            debug_events=debug_events,
        )
        self._event_listeners = {}
        self._setup = False
        self._closed = True
        self._cache.clear()

        self.connect_timeout = connect_timeout
        self.intents = intents or Intents.unprivileged()

        # Following are set during setup()
        self._shards_count: typing.Optional[int] = shards_count
        self._max_concurrency: typing.Optional[int] = None
        self._gateway_url: typing.Optional[str] = None
        self._shards: typing.Dict[int, Shard] = {}

        # Following are set after initial connection
        self._user: typing.Optional[ClientUser] = None

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
    def ready_timeout(self) -> float:
        return self._dispatch.ready_timeout

    @property
    def shards(self) -> typing.List[Shard]:
        r"""The list of shards associated to the client.

        Returns
        -------
        List[:class:`Shard`]
        """
        return list(self._shards.values())

    @property
    def latency(self) -> float:
        r"""The websocket latency of the client.

        If the client is running multiple shards, This returns the average of
        latencies of all shards. See :attr:`Shard.latency` for more info.

        Returns
        -------
        :class:`builtins.float`
        """
        latencies = [shard.latency for shard in self._shards.values()]
        return sum(latencies) / len(self._shards)

    @property
    def max_concurrency(self) -> typing.Optional[int]:
        r"""The maximum number of shards the client is allowed to start concurrently
        when :meth:`.launch` is called. This is set during :meth:`.setup`.

        This is retrieved from Discord and cannot be set by the user.

        Returns
        -------
        Optional[:class:`builtins.int`]
        """
        return self._max_concurrency

    @property
    def user(self) -> typing.Optional[ClientUser]:
        r"""Returns the user associated to the client.

        This is only available after initial connection has been
        made with the Discord gateway. This is not dependant on the
        members/users cache and is always available.

        Returns
        -------
        typing.Optional[:class:`ClientUser`]
        """
        return self._user

    @property
    def cache(self) -> Cache:
        r"""Returns the cache handler associated to this client.

        Returns
        -------
        :class:`Cache`
        """
        return self._cache

    def get_guild_cache(self, guild: Guild) -> GuildCache:
        r"""Returns the cache handler for the provided guild.

        This method is not meant to be called by the user. It is called by the
        library. By default, this returns the :class:`DefaultGuildCache`. However,
        When implementing custom handlers, You may return instance of custom subclasses
        of :class:`GuildCache`.

        Example::

            class MyGuildCache(qord.GuildCache):
                # implement abstract methods here.
                ...

            class Client(qord.Client):
                def get_guild_cache(self, guild):
                    return MyGuildCache(guild=guild)

        The returned value must be an instance of :class:`GuildCache` otherwise
        :exc:`TypeError` would be raised upon guild creations.

        Returns
        -------
        :class:`GuildCache`
        """
        return DefaultGuildCache(guild=guild)

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

    async def _wrapped_callable(self, _callable: typing.Callable[..., typing.Any], *args) -> None:
        try:
            await _callable(*args)
        except Exception:
            traceback.print_exc()

    def invoke_event(self, event_name: str, /, *args) -> None:
        r"""Invokes an event by calling all of it's listeners.

        Parameters
        ----------
        event_name: :class:`builtins.str`
            The name of event to invoke.
        *args:
            The arguments to pass to listeners.
        """
        listeners = self._event_listeners.get(event_name)

        if not listeners:
            return

        loop = asyncio.get_running_loop()

        for listener in listeners:
            loop.create_task(self._wrapped_callable(listener, *args))

    def event(self, event_name: str):
        r"""A decorator that registers an event listener for provided event.

        The decorated function must be a coroutine. Example::

            @client.event(qord.GatewayEvent.MESSAGE_CREATE)
            async def on_message_create(event):
                ...

        Parameters
        ----------
        event_name: :class:`builtins.str`
            The name of event to register listener for. See :class:`GatewayEvent` for
            names of various gateway events.
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
        return self._setup

    def _notify_shards_launch(self) -> None:
        self._dispatch._shards_connected.set()

    def _reset_setup(self) -> None:
        self._rest.token = None
        self._max_concurrency = None
        self._shards.clear()
        self._setup = False

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
        if self.is_setup():
            raise RuntimeError("Client is already setup.")

        self._rest.token = token

        gateway = await self._rest.get_bot_gateway()

        self._gateway_url = gateway["url"] + "?v=9&encoding=json&compress=zlib-stream"
        self._max_concurrency = gateway["session_start_limit"]["max_concurrency"]

        if self._shards_count is None:
            self._shards_count = gateway["shards"]

        # spawn the shards
        self._shards = {
            shard_id: Shard(id=shard_id, client=self)
            for shard_id in range(self._shards_count) # type: ignore
        }
        self._setup = True

    async def launch(self) -> None:
        r"""Launches the bot.

        This method should be called *after* :meth:`.setup`.

        Raises
        ------
        :class:`ClientSetupRequired`
            The client is not setup yet. See :meth:`.setup` for more info.
        """
        if not self.is_setup():
            raise ClientSetupRequired("Client is not setup yet. Call Client.setup() first.")
        if not self._closed:
            raise RuntimeError("Already running, Close the client first.")

        loop = asyncio.get_running_loop()

        shards = self.shards

        _LOGGER.info(
            "Launching %s shards (%s shard%s concurrently per 5 seconds)",
            self._shards_count,
            self._max_concurrency,
            's' if self._max_concurrency > 1 else '',
        )
        future = asyncio.Future()

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
                        shard._wrapped_launch(self._gateway_url, future), # type: ignore
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
                    _LOGGER.error("Timed out waiting for a shard to start.")

                    # Check if we have an error
                    if future.done():
                        raise future.result()

            if shards:
                await asyncio.sleep(5)

        # block until one of the shards crash
        self._closed = False
        self._notify_shards_launch()
        exc = await asyncio.wait_for(future, timeout=None)
        raise exc

    async def close(self, clear_setup: bool = True) -> None:
        r"""Gracefully closes the client.

        The entire closing process includes:

        - Gracefully closing all the spawned shards.
        - Closing the HTTP session.
        - Clearing the client setup.

        Parameters
        ----------
        clear_setup: :class:`builtins.bool`
            Whether to clear the client setup. Defaults to ``True``.

            If set to ``False``, Client setup will not be closed and there
            will be no need of calling :meth:`.setup` again.
        """
        if self._closed:
            return

        _LOGGER.info("Gracefully closing %s shards.", self._shards_count)

        for shard in self._shards.values():
            await shard._close(code=1000, _clean=True)

        dispatch_handler = self._dispatch
        dispatch_handler._shards_connected.clear()
        dispatch_handler._shards_ready.clear()
        await self._rest.close()

        if clear_setup:
            self._reset_setup()

        self._closed = True

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
            loop.stop()
            loop.close()

    def is_ready(self) -> bool:
        r"""Indicates whether the client is ready.

        This returns ``True`` only when all shards are ready.

        Returns
        -------
        :class:`builtins.bool`
        """
        return self._dispatch._shards_ready.is_set()

    async def wait_until_ready(self) -> None:
        r"""A coroutine that blocks until all shards are ready."""
        await self._dispatch._shards_ready.wait()

    def get_shard(self, shard_id: int, /) -> typing.Optional[Shard]:
        r"""Resolves a :class:`Shard` by it's ID.

        Parameters
        ----------
        shard_id: :class:`builtins.int`
            The ID of shard to get. See :attr:`Shard.id` documentation for more
            information about shard ID.

        Returns
        -------
        typing.Optional[:class:`Shard`]
            The resolved shard for the provided ID. If no shard exists
            with the provided ID, None is returned.
        """
        return self._shards.get(shard_id)

    # API calls

    async def fetch_user(self, user_id: int, /) -> User:
        r"""Fetches a :class:`User` by it's ID via REST API.

        Parameters
        ----------
        user_id: :class:`builtins.int`
            The ID of user to fetch.

        Returns
        -------
        :class:`User`
            The requested user.

        Raises
        ------
        HTTPNotFound
            The user of provided ID does not exist.
        HTTPException
            HTTP request failed.
        """
        data = await self._rest.get_user(user_id)
        return User(data, client=self)

    async def fetch_guild(self, guild_id: int, /, *, with_counts: bool = False) -> Guild:
        r"""Fetches a :class:`Guild` by it's ID via REST API.

        Parameters
        ----------
        guild_id: :class:`builtins.int`
            The ID of guild to fetch.
        with_counts: :class:`builtins.bool`
            Whether to also include :attr:`~Guild.approximate_member_count` and
            :attr:`~Guild.approximate_presence_count` in the returned guild.

        Returns
        -------
        :class:`Guild`
            The requested guild.

        Raises
        ------
        HTTPNotFound
            The guild of provided ID does not exist.
        HTTPException
            HTTP request failed.
        """
        data = await self._rest.get_guild(guild_id, with_counts=with_counts)
        return Guild(data, client=self, enable_cache=False)

    async def leave_guild(self, guild_id: int, /) -> None:
        r"""Leaves a guild by it's ID.

        Parameters
        ----------
        guild_id: :class:`builtins.int`
            The ID of guild to leave.

        Raises
        ------
        HTTPNotFound
            The guild of provided ID does not exist or user is already
            not part of such guild.
        HTTPException
            HTTP request failed.
        """
        await self._rest.leave_guild(guild_id)
