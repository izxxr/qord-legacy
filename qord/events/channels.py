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

from qord.events.base import BaseEvent
from qord.enums import GatewayEvent

import typing
from dataclasses import dataclass

if typing.TYPE_CHECKING:
    from datetime import datetime
    from qord.core.shard import Shard
    from qord.models.channels import GuildChannel
    from qord.models.guilds import Guild
    from qord.models.guild_members import GuildMember
    from qord.models.users import User
    from qord.models.messages import MessageableT

@dataclass(frozen=True)
class ChannelCreate(BaseEvent):
    """Structure for :attr:`~qord.GatewayEvent.CHANNEL_CREATE` event.

    This event is called whenever a new channel is created in a guild.
    """
    event_name = GatewayEvent.CHANNEL_CREATE
    shard: Shard

    channel: GuildChannel
    """The channel that was created."""

    guild: Guild
    """The guild where the event happened."""

@dataclass(frozen=True)
class ChannelUpdate(BaseEvent):
    """Structure for :attr:`~qord.GatewayEvent.CHANNEL_UPDATE` event.

    This event is called whenever one or more properties of a guild channel
    are updated.
    """
    event_name = GatewayEvent.CHANNEL_UPDATE
    shard: Shard

    before: GuildChannel
    """The channel before the update."""

    after: GuildChannel
    """The channel after the update."""

    guild: Guild
    """The guild that the updated channel belonged to."""

@dataclass(frozen=True)
class ChannelPinsUpdate(BaseEvent):
    """Structure for :attr:`~qord.GatewayEvent.CHANNEL_PINS_UPDATE` event.

    This event is called whenever a message is pinned or unpinned in a channel.
    This event is not called if a pinned message is deleted.
    """
    event_name = GatewayEvent.CHANNEL_PINS_UPDATE
    shard: Shard

    channel: MessageableT
    """The channel whose pins were updated."""

    guild: typing.Optional[Guild]
    """The guild where the event happened; If applicable otherwise ``None``."""

@dataclass(frozen=True)
class ChannelDelete(BaseEvent):
    """Structure for :attr:`~qord.GatewayEvent.CHANNEL_DELETE` event.

    This event is called whenever a channel is deleted in a guild.
    """
    event_name = GatewayEvent.CHANNEL_DELETE
    shard: Shard

    channel: GuildChannel
    """The channel that was deleted."""

    guild: Guild
    """The guild that the delete channel belonged to."""

@dataclass(frozen=True)
class TypingStart(BaseEvent):
    """Structure for :attr:`~qord.GatewayEvent.TYPING_START` event.

    This event is called whenever a user starts typing in a channel.
    """
    event_name = GatewayEvent.TYPING_START
    shard: Shard

    channel: MessageableT
    """The channel in which typing started in."""

    started_at: datetime
    """The time when the typing started."""

    user: typing.Union[User, GuildMember]
    """The user or member that started typing.

    If the event happened in a guild, This is :class:`GuildMember` otherwise
    it is a :class:`User`.
    """

    guild: typing.Optional[Guild]
    """The guild in which typing started in if any."""
