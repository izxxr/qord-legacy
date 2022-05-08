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
from qord.core.cache_impl import DefaultClientCache, DefaultGuildCache
from qord.flags.intents import Intents
from qord.flags.applications import ApplicationFlags
from qord.models.users import User
from qord.models.guilds import Guild
from qord.models.channels import _is_guild_channel, _guild_channel_factory, _private_channel_factory
from qord.models.applications import Application
from qord.exceptions import ClientSetupRequired
from qord.events.base import BaseEvent

import asyncio
import inspect
import logging
import traceback
import typing

if typing.TYPE_CHECKING:
    from aiohttp import ClientSession
    from qord.models.users import ClientUser
    from qord.models.channels import GuildChannel, PrivateChannel
    from qord.core.cache import ClientCache, GuildCache

    BE = typing.TypeVar("BE", bound="BaseEvent")
    EventListener = typing.Callable[[BE], typing.Any]


__all__ = (
    "Client",
)

_LOGGER = logging.getLogger(__name__)


class Client:
    """A client that interacts with Discord API.

    This is the core class of this library and the main starter point for
    every bot. All parameters passed during initializing are optional and keyword only.

    This is a basic example using this class to build a "Ping Pong" bot::

        import qord

        client = qord.Client()

        @client.event(qord.GatewayEvent.MESSAGE_CREATE)
        async def on_message_create(event):
            message = event.message

            if message.author.bot:
                # Don't respond to bots.
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
    cache: :class:`ClientCache`
        The cache handler to use for the client. If not provided, Defaults to
        :class:`DefaultClientCache`.
    """
    if typing.TYPE_CHECKING:
        _event_listeners: typing.Dict[str, typing.List[EventListener]]
        _event_futures: typing.Dict[str, typing.List[typing.Tuple[typing.Callable[[BaseEvent], bool], asyncio.Future[BaseEvent]]]]

    def __init__(self,
        *,
        session: typing.Optional[ClientSession] = None,
        shards_count: typing.Optional[int] = None,
        intents: typing.Optional[Intents] = None,
        cache: typing.Optional[ClientCache] = None,
        session_owner: bool = False,
        max_retries: int = 5,
        debug_events: bool = False,
        connect_timeout: float = 5.0,
        ready_timeout: float = 2.0,
    ) -> None:

        if shards_count is not None and shards_count < 1:
            raise ValueError("Parameter shards_count must be an integer greater then or equal to 1.")
        if cache is not None and not isinstance(cache, ClientCache):
            raise TypeError("Parameter cache must be an instance of ClientCache. Not %r" % cache.__class__)

        self._rest: RestClient = RestClient(
            session=session,
            session_owner=session_owner,
            max_retries=max_retries,
        )
        self._cache: ClientCache = cache or DefaultClientCache()
        self._dispatch: DispatchHandler = DispatchHandler(
            client=self,
            ready_timeout=ready_timeout,
            debug_events=debug_events,
        )
        self._event_listeners = {}
        self._event_futures = {}
        self._setup = False
        self._closed = True
        self._shards_fut = None
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
        self._application_id: typing.Optional[int] = None
        self._application_flags: typing.Optional[int] = None

        # Using inspect.getmembers() on the client instance ends
        # up calling the properties and possibly any other dynamic
        # attributes of the client instance. Since we don't want
        # that, here's a hacky approach for avoiding this unfortunate
        # behaviour that uses getmembers() on parent class rather than
        # the instance. See https://bugs.python.org/issue38337

        for name, member in inspect.getmembers(self.__class__):
            if hasattr(member, "__listener_event__"):
                try:
                    bound_method = getattr(self, name)
                except AttributeError:
                    # Not there somehow
                    continue
                else:
                    self.register_event_listener(member.__listener_event__, bound_method)

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
        """The list of shards associated to the client.

        Returns
        -------
        List[:class:`Shard`]
        """
        return list(self._shards.values())

    @property
    def latency(self) -> float:
        """The websocket latency of the client.

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
        """The maximum number of shards the client is allowed to start concurrently
        when :meth:`.launch` is called. This is set during :meth:`.setup`.

        This is retrieved from Discord and cannot be set by the user.

        Returns
        -------
        Optional[:class:`builtins.int`]
        """
        return self._max_concurrency

    @property
    def user(self) -> typing.Optional[ClientUser]:
        """Returns the user associated to the client.

        This is only available after initial connection has been
        made with the Discord gateway. This is not dependant on the
        members/users cache and is always available.

        Returns
        -------
        typing.Optional[:class:`ClientUser`]
        """
        return self._user

    @property
    def application_id(self) -> typing.Optional[int]:
        """The application ID of connected client.

        This is only available after initial connection has been
        made with the Discord gateway.

        Returns
        -------
        typing.Optional[:class:`int`]
        """
        return self._application_id

    @property
    def application_flags(self) -> typing.Optional[ApplicationFlags]:
        """The application flags of connected client.

        This is only available after initial connection has been
        made with the Discord gateway.

        Returns
        -------
        typing.Optional[:class:`ApplicationFlags`]
        """
        flags = self._application_flags
        if flags is None:
            return None
        return ApplicationFlags(flags)

    @property
    def cache(self) -> ClientCache:
        """Returns the cache handler associated to this client.

        Returns
        -------
        :class:`ClientCache`
        """
        return self._cache

    def get_guild_cache(self, guild: Guild) -> GuildCache:
        """Returns the cache handler for the provided guild.

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

    def get_event_listeners(self, event_name: str, /) -> typing.List[EventListener]:
        """Gets the list of all events listener for the provided event.

        Parameters
        ----------
        event_name: :class:`builtins.str`
            The name of event to get listeners for.

        Returns
        -------
        The list of event listeners.
        """
        return self._event_listeners.get(event_name, [])

    def clear_event_listeners(self, event_name: str, /) -> typing.List[EventListener]:
        """Clears all events listener for the provided event.

        Parameters
        ----------
        event_name: :class:`builtins.str`
            The name of event to clear listeners for.

        Returns
        -------
        The list of removed event listeners.
        """
        return self._event_listeners.pop(event_name, [])

    def walk_event_listeners(self) -> typing.List[typing.Tuple[str, typing.List[EventListener]]]:
        """Returns a list of tuples with first element being event name and second
        element being the list of event listeners for that event.

        Example::

            for name, listeners in client.walk_event_listeners():
                print(name, listeners)
        """
        return list(self._event_listeners.items())

    def register_event_listener(self, event_name: str, callback: EventListener, /) -> None:
        """Registers an event listener for provided event.

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

    async def wait_for_event(
        self,
        event_name: str,
        *,
        check: typing.Optional[typing.Callable[[BE], bool]] = None,
        timeout: typing.Optional[float] = None,
    ) -> BE:
        """Waits for an event to invoke.

        If no ``check`` is passed, the first event that invokes after
        calling this method is returned otherwise the ``check`` function
        is called every time the event happens until the check isn't met.

        This method is useful when awaiting user input such as a message
        or reaction.

        Example::

            def check(event):
                return event.message.content.isdigit()

            await channel.send("Say a number within 60 seconds!")
            try:
                event = await client.wait_for_event(
                    qord.GatewayEvent.MESSAGE_CREATE,
                    check=check,
                    timeout=60.0
                )
            except asyncio.TimeoutError:
                await channel.send("You didn't respond in time...")
            else:
                await channel.send(f"You said a number: {event.message.content}")

        Parameters
        ----------
        event_name: :class:`builtins.str`
            The name of event to wait for.
        check: Callable[[:class:`BaseEvent`], :class:`builtins.bool`]
            A function to check against before returning the result.
            This function takes a single :class:`BaseEvent` instance.
        timeout: Optional[:class:`builtins.float`]
            The number of seconds after which :class:`asyncio.TimeoutError`
            is raised if the event has not occured. ``None`` (default) indicates
            no timeout.

        Returns
        -------
        :class:`BaseEvent`
            The event that met the check.

        Raises
        ------
        asyncio.TimeoutError
            Timed out waiting for the event to invoke.
        """

        if check is None:
            check = lambda e: True

        try:
            futures = self._event_futures[event_name]
        except KeyError:
            self._event_futures[event_name] = futures = []

        future = asyncio.Future()
        tup = (check, future)
        futures.append(tup)

        try:
            result = await asyncio.wait_for(future, timeout=timeout)
        except asyncio.TimeoutError:
            # Make sure to properly remove the stored future
            try:
                futures.remove(tup)
            except ValueError:
                pass
            raise
        else:
            return result

    def invoke_event(self, event: BaseEvent, /) -> None:
        """Invokes an event by calling all of it's listeners.

        This method is exposed to documentation to allow users
        to dispatch custom events. For more information about this
        topic, See :doc:`events`.

        Parameters
        ----------
        event: :class:`BaseEvent`
            The event to invoke.
        """
        try:
            event_name = event.__event_name__
        except AttributeError:
            raise TypeError("Parameter 'event' must be an instance of events.BaseEvent") from None

        loop = asyncio.get_running_loop()

        listeners = self._event_listeners.get(event_name, [])
        for listener in listeners:
            loop.create_task(self._wrapped_callable(listener, event))

        futures = self._event_futures.get(event_name, [])
        for tup in futures:
            check, future = tup
            if check(event):
                if not future.done():
                    future.set_result(event)
                try:
                    futures.remove(tup)
                except ValueError:
                    pass

    def event(self, event_name: str, /) -> typing.Callable[[EventListener], EventListener]:
        """A decorator that registers an event listener for provided event.

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
        def wrap(func: EventListener):
            self.register_event_listener(event_name, func)
            return func

        return wrap

    def is_setup(self) -> bool:
        """
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
        """Setups the client with the provided authorization token.

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
        """Launches the bot.

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
            's' if self._max_concurrency > 1 else '', # type: ignore
        )
        self._shards_fut = future = asyncio.Future()

        while shards:
            # The _max_concurrency attribute is never None here.
            # Starting '_max_concurrency' number of shards every
            # 5 seconds.

            waiters = []

            for _ in range(self._max_concurrency): # type: ignore
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

    async def close(self, *, clear_setup: bool = True) -> None:
        """Gracefully closes the client.

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
        self._cache.clear()
        await self._rest.close()

        if clear_setup:
            self._reset_setup()

        self._closed = True

    def start(self, token: str, /) -> None:
        """Setups the client with provided token and then starts it.

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
        """Indicates whether the client is ready.

        This returns ``True`` only when all shards are ready.

        Returns
        -------
        :class:`builtins.bool`
        """
        return self._dispatch._shards_ready.is_set()

    async def wait_until_ready(self) -> None:
        """A coroutine that blocks until all shards are ready."""
        await self._dispatch._shards_ready.wait()

    def get_shard(self, shard_id: int, /) -> typing.Optional[Shard]:
        """Resolves a :class:`Shard` by it's ID.

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

    async def fetch_current_application(self) -> Application:
        """Fetches the current bot's application.

        This requires the client to be setup with a proper bot
        token via :meth:`.setup`.

        .. tip::

            If you just need the application ID and flags, see
            the :attr:`.application_id` and :attr:`.application_flags`
            properties.

        Returns
        -------
        :class:`Application`
            The application for current bot.
        """
        data = await self._rest.get_current_application()
        return Application(data, client=self)

    async def fetch_user(self, user_id: int, /) -> User:
        """Fetches a :class:`User` by it's ID via REST API.

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
        """Fetches a :class:`Guild` by it's ID via REST API.

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
        """Leaves a guild by it's ID.

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

    async def fetch_channel(self, channel_id: int, /) -> typing.Union[GuildChannel, PrivateChannel]:
        """Fetches a channel through it's ID.

        .. note::
            Due to an implementation limitation, When fetching channels related
            to a specific guild, The relevant guild is needed to be cached by
            the client otherwise a :class:`RuntimeError` is raised. This
            is not the case for channel types that are not assoicated to guilds.

        Parameters
        ----------
        channel_id: :class:`builtins.int`
            The ID of channel to fetch.

        Returns
        -------
        Union[:class:`GuildChannel`, :class:`PrivateChannel`]
            The fetched channel.

        Raises
        ------
        RuntimeError
            The guild of channel is not cached.
        HTTPNotFound
            The channel does not exist.
        HTTPException
            The fetching failed.
        """
        data = await self._rest.get_channel(channel_id)
        channel_type = int(data["type"])

        if _is_guild_channel(channel_type):
            # The guild_id field is always present for channels sent over REST.
            guild = self._cache.get_guild(int(data["guild_id"]))

            if guild is None:
                raise RuntimeError("The channel's guild is not cached.")

            cls = _guild_channel_factory(channel_type)
            return cls(data, guild=guild)
        else:
            cls = _private_channel_factory(channel_type)
            return cls(data, client=self)

