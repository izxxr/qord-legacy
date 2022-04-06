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
    from qord.core.shard import Shard
    from qord.models.guilds import Guild


__all__ = (
    "GuildAvailable",
    "GuildUnavailable",
    "GuildJoin",
    "GuildUpdate",
    "GuildLeave",
)


@dataclass(frozen=True)
class GuildAvailable(BaseEvent, event_name=GatewayEvent.GUILD_AVAILABLE):
    """Structure for :attr:`~qord.GatewayEvent.GUILD_AVAILABLE` event.

    This event is called whenever a guild becomes available to the client. When
    initially connecting, This event may call several times for lazy loading of
    client guilds.

    This event requires the :attr:`~qord.Intents.guilds` to be enabled. This
    intent is enabled by default.
    """
    shard: Shard

    guild: Guild
    """The guild that became available."""

@dataclass(frozen=True)
class GuildUnavailable(BaseEvent, event_name=GatewayEvent.GUILD_UNAVAILABLE):
    """Structure for :attr:`~qord.GatewayEvent.GUILD_UNAVAILABLE` event.

    This event is called whenever a guild becomes unavailable to the client
    most likely due to an outage.

    This event requires the :attr:`~qord.Intents.guilds` to be enabled. This
    intent is enabled by default.
    """
    shard: Shard

    guild: Guild
    """The guild that became unavailable."""

@dataclass(frozen=True)
class GuildJoin(BaseEvent, event_name=GatewayEvent.GUILD_JOIN):
    """Structure for :attr:`~qord.GatewayEvent.GUILD_JOIN` event.

    This event is called whenever the client user or bot joins a new
    guild.

    This event requires the :attr:`~qord.Intents.guilds` to be enabled. This
    intent is enabled by default.
    """
    shard: Shard

    guild: Guild
    """The joined guild."""

@dataclass(frozen=True)
class GuildLeave(BaseEvent, event_name=GatewayEvent.GUILD_LEAVE):
    """Structure for :attr:`~qord.GatewayEvent.GUILD_LEAVE` event.

    This event is called whenever the client user or bot is removed
    (kicked, banned or simply left) from a guild.

    This event requires the :attr:`~qord.Intents.guilds` to be enabled. This
    intent is enabled by default.
    """
    shard: Shard

    guild: Guild
    """The left guild."""

@dataclass(frozen=True)
class GuildUpdate(BaseEvent, event_name=GatewayEvent.GUILD_UPDATE):
    """Structure for :attr:`~qord.GatewayEvent.GUILD_UPDATE` event.

    This event is called whenever one or more properties of a guild are updated.

    This event requires the :attr:`~qord.Intents.guilds` to be enabled. This
    intent is enabled by default.
    """
    shard: Shard

    before: Guild
    """The copy of guild before the update."""

    after: Guild
    """The guild after the update."""
