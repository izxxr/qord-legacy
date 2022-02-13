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

from qord.models.users import ClientUser
from qord.models.guilds import Guild
from qord import events

import asyncio
import inspect
import logging
import typing

if typing.TYPE_CHECKING:
    from qord.core.client import Client
    from qord.core.shard import Shard


def event_dispatch_handler(name: str):
    def _wrap(func: typing.Callable[[DispatchHandler, Shard, typing.Any], typing.Any]):
        func.__handler_event__ = name
        return func

    return _wrap


class DispatchHandler:
    r"""Internal class that handles gateway events dispatches."""

    def __init__(self, client: Client, ready_timeout: float = 2.0) -> None:
        self.client = client
        self.ready_timeout = ready_timeout
        self.cache = client._cache
        self.invoke = client.invoke_event
        self._guild_create_waiter = None
        self._update_handlers()

    def _update_handlers(self):
        self._handlers = {}
        members = inspect.getmembers(self)

        for _, member in members:
            try:
                self._handlers[member.__handler_event__] = member
            except AttributeError:
                pass

    async def handle(self, shard: Shard, title: str, data: typing.Any) -> None:
        event = events.GatewayDispatch(shard=shard, title=title, data=data)
        self.invoke(event.event_name, event)

        try:
            handler = self._handlers[title]
        except KeyError:
            return
        else:
            await handler(shard, data)

    async def _prepare_shard_ready(self, event: events.ShardReady):
        # Wait for guilds cache to fill before invoking
        # ready event by setting a timeout on the GUILD_CREATE events.

        timeout = self.ready_timeout

        while True:
            self._guild_create_waiter = asyncio.Future()

            try:
                await asyncio.wait_for(self._guild_create_waiter, timeout=timeout)
            except asyncio.TimeoutError:
                break

        self._guild_create_waiter = None
        self.invoke(event.event_name, event)

    @event_dispatch_handler("READY")
    async def on_ready(self, shard: Shard, data: typing.Any) -> None:
        user = ClientUser(data["user"], client=self.client)
        self.cache.add_user(user)
        self.client._user = user

        shard._log(logging.INFO, "Lazy loading cache for ~%s guilds in background." % len(data["guilds"]))
        event = events.ShardReady(shard=shard)
        asyncio.create_task(self._prepare_shard_ready(event))

    @event_dispatch_handler("GUILD_CREATE")
    async def on_guild_create(self, shard: Shard, data: typing.Any) -> None:
        guild = Guild(data, client=self.client, enable_cache=True)

        if not guild.unavailable:
            self.cache.add_guild(guild)

        waiter = self._guild_create_waiter

        if waiter and not waiter.done():
            # Notify the waiters for ready event.
            waiter.set_result(guild)
