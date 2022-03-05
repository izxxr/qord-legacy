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
from qord.models.roles import Role
from qord.models.guild_members import GuildMember
from qord.models.channels import _guild_channel_factory
from qord.models.messages import Message
from qord._helpers import parse_iso_timestamp
from qord import events

from datetime import datetime
import asyncio
import copy
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

    def __init__(self, client: Client, ready_timeout: float = 2.0, debug_events: bool = False) -> None:
        self.client = client
        self.ready_timeout = ready_timeout
        self.debug_events = debug_events
        self.cache = client._cache
        self._invoke = client.invoke_event
        self._shards_connected = asyncio.Event()
        self._shards_ready = asyncio.Event()
        self._guild_create_waiter = None
        self._ready_task = None
        self._update_handlers()

    def _update_handlers(self):
        self._handlers = {}
        members = inspect.getmembers(self)

        for _, member in members:
            try:
                self._handlers[member.__handler_event__] = member
            except AttributeError:
                pass

    def invoke(self, event: events.BaseEvent) -> None:
        self._invoke(event.event_name, event)

    async def handle(self, shard: Shard, title: str, data: typing.Any) -> None:
        if self.debug_events:
            event = events.GatewayDispatch(shard=shard, title=title, data=data)
            self.invoke(event)

        try:
            handler = self._handlers[title]
        except KeyError:
            return
        else:
            await handler(shard, data)

    async def _prepare_ready(self, shard: typing.Optional[Shard] = None):
        # Setting a timeout for GUILD_CREATE to allow the given shards
        # to lazy load the guilds before dispatching ready event.
        timeout = self.ready_timeout

        if shard is None:
            # shard being None means we are waiting for all shards to lazy load the
            # guilds so wait for all the shards to connect first.
            await self._shards_connected.wait()

        while True:
            self._guild_create_waiter = asyncio.Future()
            try:
                await asyncio.wait_for(self._guild_create_waiter, timeout=timeout)
            except asyncio.TimeoutError:
                break

        # Do some cleanup and invoke the ready event
        self._guild_create_waiter = None
        event = events.Ready() if shard is None else events.ShardReady(shard=shard)
        self.invoke(event)

        if shard is None:
            self._shards_ready.set()
            self._ready_task = None

    @event_dispatch_handler("READY")
    async def on_ready(self, shard: Shard, data: typing.Any) -> None:
        user = ClientUser(data["user"], client=self.client)
        self.cache.add_user(user)
        self.client._user = user

        shard._log(logging.INFO, "Lazy loading cache for ~%s guilds in background." % len(data["guilds"]))

        # Wait for current shard to backfill guilds.
        coro = self._prepare_ready(shard)
        asyncio.create_task(coro)

        if self._ready_task is None:
            # Wait for all shards to backfill guilds in background.
            coro = self._prepare_ready()
            self._ready_task = asyncio.create_task(coro)

    @event_dispatch_handler("RESUMED")
    async def on_resumed(self, shard: Shard, data: typing.Any) -> None:
        event = events.Resumed(shard=shard)
        self.invoke(event)

    @event_dispatch_handler("USER_UPDATE")
    async def on_user_update(self, shard: Shard, data: typing.Dict[str, typing.Any]) -> None:
        user_id = int(data["id"])
        user = self.cache.get_user(user_id)

        if user is None:
            shard._log(logging.DEBUG, "USER_UPDATE: Unknown user with ID %s", user_id)
            return

        before = copy.copy(user)
        user._update_with_data(data)

        event = events.UserUpdate(shard=shard, before=before, after=user)
        self.invoke(event)

    @event_dispatch_handler("GUILD_CREATE")
    async def on_guild_create(self, shard: Shard, data: typing.Dict[str, typing.Any]) -> None:
        unavailable = data.get("unavailable")

        if unavailable is True:
            # TODO: Not sure about what to do about joining an unavailable
            # guild but for now, Do nothing
            return

        guild = Guild(data, client=self.client, enable_cache=True)
        self.cache.add_guild(guild)

        # Notify waiters for dispatching ready event
        waiter = self._guild_create_waiter

        if waiter and not waiter.done():
            waiter.set_result(guild)

        # unavailable being False means that an unavailable guild
        # either because of outage or from READY event has became available.
        # And unavailable not being included in payload
        # means that bot has joined a new guild.
        # https://github.com/discord/discord-api-docs/issues/4518
        if unavailable is False:
            event = events.GuildAvailable(guild=guild, shard=shard)
        elif unavailable is None:
            event = events.GuildJoin(guild=guild, shard=shard)

        self.invoke(event) # type: ignore

    @event_dispatch_handler("GUILD_UPDATE")
    async def on_guild_update(self, shard: Shard, data: typing.Any) -> None:
        guild_id = int(data["id"])
        guild = self.cache.get_guild(guild_id)

        if guild is None:
            shard._log(logging.DEBUG, "GUILD_UPDATE: Unknown guild with ID %s", guild_id)
            return

        before = copy.copy(guild)
        guild._update_with_data(data)

        event = events.GuildUpdate(before=before, after=guild, shard=shard)
        self.invoke(event)

    @event_dispatch_handler("GUILD_DELETE")
    async def on_guild_delete(self, shard: Shard, data: typing.Any) -> None:
        guild_id = int(data["id"])
        guild = self.cache.get_guild(guild_id)

        if guild is None:
            shard._log(logging.DEBUG, "GUILD_DELETE: Unknown guild with ID %s", guild_id)
            return

        unavailable = data.get("unavailable")

        if unavailable is None:
            # Bot is removed from the guild.
            guild = self.cache.delete_guild(guild_id)
            if guild is None:
                # already removed?
                return
            event = events.GuildLeave(shard=shard, guild=guild)
        else:
            # Guild became unavailable due to an outage
            # TODO: Evict guild here?
            guild.unavailable = True
            event = events.GuildUnavailable(shard=shard, guild=guild)

        self.invoke(event)

    @event_dispatch_handler("GUILD_ROLE_CREATE")
    async def on_guild_role_create(self, shard: Shard, data: typing.Any) -> None:
        guild_id = int(data["guild_id"])
        guild = self.cache.get_guild(guild_id)

        if guild is None:
            shard._log(logging.DEBUG, "GUILD_ROLE_CREATE: Unknown guild with ID %s", guild_id)
            return

        role = Role(data["role"], guild=guild)
        event = events.RoleCreate(role=role, guild=guild, shard=shard)

        guild._cache.add_role(role)
        self.invoke(event)

    @event_dispatch_handler("GUILD_ROLE_UPDATE")
    async def on_guild_role_update(self, shard: Shard, data: typing.Any) -> None:
        guild_id = int(data["guild_id"])
        guild = self.cache.get_guild(guild_id)

        if guild is None:
            shard._log(logging.DEBUG, "GUILD_ROLE_UPDATE: Unknown guild with ID %s", guild_id)
            return

        raw_role = data["role"]
        role_id = int(raw_role["id"])

        role = guild._cache.get_role(role_id)

        if role is None:
            shard._log(logging.DEBUG, "GUILD_ROLE_UPDATE: Unknown role with ID %s", role_id)
            return

        before = copy.copy(role)
        role._update_with_data(raw_role)
        event = events.RoleUpdate(before=before, after=role, guild=guild, shard=shard)

        self.invoke(event)

    @event_dispatch_handler("GUILD_ROLE_DELETE")
    async def on_guild_role_delete(self, shard: Shard, data: typing.Any) -> None:
        guild_id = int(data["guild_id"])
        guild = self.cache.get_guild(guild_id)

        if guild is None:
            shard._log(logging.DEBUG, "GUILD_ROLE_DELETE: Unknown guild with ID %s", guild_id)
            return

        role_id = int(data["role_id"])
        role = guild._cache.delete_role(role_id)

        if role is None:
            shard._log(logging.DEBUG, "GUILD_ROLE_DELETE: Unknown role with ID %s", role_id)
            return

        event = events.RoleDelete(role=role, guild=guild, shard=shard)
        self.invoke(event)

    @event_dispatch_handler("GUILD_MEMBER_ADD")
    async def on_guild_member_add(self, shard: Shard, data: typing.Any) -> None:
        guild_id = int(data["guild_id"])
        guild = self.cache.get_guild(guild_id)

        if guild is None:
            shard._log(logging.DEBUG, "GUILD_MEMBER_ADD: Unknown guild with ID %s", guild_id)
            return

        member = GuildMember(data, guild=guild)

        guild._cache.add_member(member)
        self.cache.add_user(member.user)

        if guild.member_count is not None:
            guild.member_count += 1

        event = events.GuildMemberAdd(shard=shard, guild=guild, member=member)
        self.invoke(event)

    @event_dispatch_handler("GUILD_MEMBER_UPDATE")
    async def on_guild_member_update(self, shard: Shard, data: typing.Any) -> None:
        guild_id = int(data["guild_id"])
        guild = self.cache.get_guild(guild_id)

        if guild is None:
            shard._log(logging.DEBUG, "GUILD_MEMBER_UPDATE: Unknown guild with ID %s", guild_id)
            return

        user_id = int(data["user"]["id"])
        member = guild._cache.get_member(user_id)

        if member is None:
            shard._log(logging.DEBUG, "GUILD_MEMBER_UPDATE: Unknown user with ID %s", user_id)
            return

        before = copy.copy(member)
        member._update_with_data(data)

        event = events.GuildMemberUpdate(shard=shard, guild=guild, before=before, after=member)
        self.invoke(event)

    @event_dispatch_handler("GUILD_MEMBER_REMOVE")
    async def on_guild_member_remove(self, shard: Shard, data: typing.Any) -> None:
        guild_id = int(data["guild_id"])
        guild = self.cache.get_guild(guild_id)

        if guild is None:
            shard._log(logging.DEBUG, "GUILD_MEMBER_REMOVE: Unknown guild with ID %s", guild_id)
            return

        user_id = int(data["user"]["id"])
        member = guild._cache.delete_member(user_id)

        if member is None:
            shard._log(logging.DEBUG, "GUILD_MEMBER_REMOVE: Unknown user with ID %s", user_id)
            return

        self.cache.delete_user(user_id)

        if guild.member_count is not None:
            guild.member_count -= 1

        event = events.GuildMemberRemove(shard=shard, guild=guild, member=member)
        self.invoke(event)

    @event_dispatch_handler("CHANNEL_CREATE")
    async def on_channel_create(self, shard: Shard, data: typing.Dict[str, typing.Any]) -> None:
        try:
            guild_id = int(data["guild_id"])
        except KeyError:
            return

        guild = self.cache.get_guild(guild_id)

        if guild is None:
            shard._log(logging.DEBUG, "CHANNEL_CREATE: Unknown guild with ID %s", guild_id)
            return

        cls = _guild_channel_factory(data["type"])
        channel = cls(data, guild=guild)
        event = events.ChannelCreate(shard=shard, channel=channel, guild=guild)

        guild.cache.add_channel(channel)
        self.invoke(event)

    @event_dispatch_handler("CHANNEL_UPDATE")
    async def on_channel_update(self, shard: Shard, data: typing.Dict[str, typing.Any]) -> None:
        try:
            guild_id = int(data["guild_id"])
        except KeyError:
            return

        guild = self.cache.get_guild(guild_id)

        if guild is None:
            shard._log(logging.DEBUG, "CHANNEL_UPDATE: Unknown guild with ID %s", guild_id)
            return

        channel_id = int(data["id"])
        channel = guild.cache.get_channel(channel_id)

        if channel is None:
            shard._log(logging.DEBUG, "CHANNEL_UPDATE: Unknown channel with ID %s", channel_id)
            return

        before = copy.copy(channel)
        channel._update_with_data(data)

        event = events.ChannelUpdate(shard=shard, before=before, after=channel, guild=guild)
        self.invoke(event)

    @event_dispatch_handler("CHANNEL_DELETE")
    async def on_channel_delete(self, shard: Shard, data: typing.Dict[str, typing.Any]) -> None:
        try:
            guild_id = int(data["guild_id"])
        except KeyError:
            return

        guild = self.cache.get_guild(guild_id)

        if guild is None:
            shard._log(logging.DEBUG, "CHANNEL_DELETE: Unknown guild with ID %s", guild_id)
            return

        channel_id = int(data["id"])
        channel = guild.cache.delete_channel(channel_id)

        # XXX: data is a complete channel object, maybe create a new instance
        # if older isn't available?
        if channel is None:
            shard._log(logging.DEBUG, "CHANNEL_DELETE: Unknown channel with ID %s", channel_id)
            return

        event = events.ChannelDelete(shard=shard, channel=channel, guild=guild)
        self.invoke(event)

    @event_dispatch_handler("MESSAGE_CREATE")
    async def on_message_create(self, shard: Shard, data: typing.Dict[str, typing.Any]) -> None:
        channel_id = int(data["channel_id"])

        try:
            guild_id = int(data["guild_id"])
        except KeyError:
            channel = self.cache.get_private_channel(channel_id)
        else:
            guild = self.cache.get_guild(guild_id)
            if guild is None:
                shard._log(logging.DEBUG, "MESSAGE_CREATE: Unknown guild with ID %s", guild_id)
                return
            channel = guild._cache.get_channel(channel_id)

        if channel is None:
            shard._log(logging.DEBUG, "MESSAGE_CREATE: Unknown channel with ID %s", channel_id)
            return

        message = Message(data, channel=channel) # type: ignore
        event = events.MessageCreate(shard=shard, message=message)
        self.cache.add_message(message)
        self.invoke(event)

    @event_dispatch_handler("MESSAGE_DELETE")
    async def on_message_delete(self, shard: Shard, data: typing.Dict[str, typing.Any]) -> None:
        message_id = int(data["id"])
        message = self.cache.delete_message(message_id)

        if message is None:
            return

        event = events.MessageDelete(shard=shard, message=message)
        self.invoke(event)

    @event_dispatch_handler("MESSAGE_DELETE_BULK")
    async def on_message_delete_bulk(self, shard: Shard, data: typing.Dict[str, typing.Any]) -> None:
        message_ids = [int(mid) for mid in data["ids"]]
        channel_id = int(data["channel_id"])

        try:
            guild_id = int(data["guild_id"])
        except KeyError:
            guild = None
            channel = self.cache.get_private_channel(channel_id)
        else:
            guild = self.cache.get_guild(guild_id)

            if guild is None:
                shard._log(logging.DEBUG, "MESSAGE_DELETE_BULK: Unknown guild with ID %s", guild_id)
                return

            channel = guild._cache.get_channel(channel_id)

        if channel is None:
            shard._log(logging.DEBUG, "MESSAGE_DELETE_BULK: Unknown channel with ID %s", channel_id)
            return

        messages = []

        for message_id in message_ids:
            message = self.cache.delete_message(message_id)

            if message is not None:
                messages.append(message)

        # `channel` is always a messageable channel here.
        event = events.MessageBulkDelete(
            shard=shard,
            messages=messages,
            message_ids=message_ids,
            guild=guild,
            channel=channel, # type: ignore
        )
        self.invoke(event)

    @event_dispatch_handler("CHANNEL_PINS_UPDATE")
    async def on_channel_pins_update(self, shard: Shard, data: typing.Dict[str, typing.Any]):
        channel_id = int(data["channel_id"])

        try:
            guild_id = int(data["guild_id"])
        except KeyError:
            guild = None
            channel = self.cache.get_private_channel(channel_id)
        else:
            guild = self.cache.get_guild(guild_id)

            if guild is None:
                shard._log(logging.DEBUG, "CHANNEL_PINS_UPDATE: Unknown guild of ID %s", guild_id)
                return

            channel = guild._cache.get_channel(channel_id)

        if channel is None:
            shard._log(logging.DEBUG, "CHANNEL_PINS_UPDATE: Unknown channel of ID %s", channel_id)
            return

        last_pin_timestamp = data.get("last_pin_timestamp")

        if last_pin_timestamp is not None:
            try:
                # Should always be a messageable channel *
                channel.last_pin_timestamp = parse_iso_timestamp(last_pin_timestamp) # type: ignore
            except AttributeError:
                # We can't trust Discord. *
                pass

        event = events.ChannelPinsUpdate(
            shard=shard,
            guild=guild,
            channel=channel, # type: ignore
        )
        self.invoke(event)

    @event_dispatch_handler("MESSAGE_UPDATE")
    async def on_message_update(self, shard: Shard, data: typing.Dict[str, typing.Any]) -> None:
        message_id = int(data["id"])
        message = self.cache.get_message(message_id)

        if message is None:
            return

        before = copy.copy(message)
        message._update_with_data(data)

        event = events.MessageUpdate(shard=shard, before=before, after=message)
        self.invoke(event)

    @event_dispatch_handler("TYPING_START")
    async def on_typing_start(self, shard: Shard, data: typing.Dict[str, typing.Any]):
        channel_id = int(data["channel_id"])
        user_id = int(data["user_id"])

        try:
            guild_id = int(data["guild_id"])
        except KeyError:
            guild = None
            channel = self.cache.get_private_channel(channel_id)
        else:
            guild = self.cache.get_guild(guild_id)
            if guild is None:
                shard._log(logging.DEBUG, "TYPING_START: Unknown guild of ID %s", guild_id)
                return

            channel = guild._cache.get_channel(channel_id)

        if channel is None:
            shard._log(logging.DEBUG, "TYPING_START: Unknown channel of ID %s", channel_id)
            return

        if guild is None:
            user = self.cache.get_user(user_id)
        else:
            user = guild._cache.get_member(user_id)
            if user is None:
                user = GuildMember(data["member"], guild=guild)

        if user is None:
            shard._log(logging.DEBUG, "TYPING_START: Unknown user of ID", user_id)
            return

        # This is not in ISO format because Discord likes being inconsistent.
        timestamp = datetime.fromtimestamp(data["timestamp"])

        event = events.TypingStart(
            shard=shard,
            channel=channel, # type: ignore
            started_at=timestamp,
            user=user,
            guild=guild,
        )
        self.invoke(event)
