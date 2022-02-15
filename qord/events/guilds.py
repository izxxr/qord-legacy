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

@dataclass(frozen=True)
class GuildAvailable(BaseEvent):
    r"""Structure for :attr:`~qord.GatewayEvent.GUILD_AVAILABLE` event.

    This event is called whenever a guild becomes available to the client. When
    initially connecting, This event may call several times for lazy loading of
    client guilds. Requires the :attr:`~qord.Intents.guilds` to be enabled.
    """
    event_name = GatewayEvent.GUILD_AVAILABLE
    shard: Shard

    guild: Guild
    r"""The guild that became available."""

@dataclass(frozen=True)
class GuildUnavailable(BaseEvent):
    r"""Structure for :attr:`~qord.GatewayEvent.GUILD_UNAVAILABLE` event.

    This event is called whenever a guild becomes unavailable to the client
    most likely due to an outage.
    """
    event_name = GatewayEvent.GUILD_UNAVAILABLE
    shard: Shard

    guild: Guild
    r"""The guild that became unavailable."""

@dataclass(frozen=True)
class GuildJoin(BaseEvent):
    r"""Structure for :attr:`~qord.GatewayEvent.GUILD_JOIN` event.

    This event is called whenever the client user or bot joins a new
    guild. Requires the :attr:`~qord.Intents.guilds` to be enabled.
    """
    event_name = GatewayEvent.GUILD_JOIN
    shard: Shard

    guild: Guild
    r"""The joined guild."""

@dataclass(frozen=True)
class GuildLeave(BaseEvent):
    r"""Structure for :attr:`~qord.GatewayEvent.GUILD_LEAVE` event.

    This event is called whenever the client user or bot is removed
    (kicked, banned or simply left) from a guild. Requires the
    :attr:`~qord.Intents.guilds` to be enabled.
    """
    event_name = GatewayEvent.GUILD_LEAVE
    shard: Shard

    guild: Guild
    r"""The left guild."""

@dataclass(frozen=True)
class GuildUpdate(BaseEvent):
    r"""Structure for :attr:`~qord.GatewayEvent.GUILD_UPDATE` event.

    This event is called whenever one or more properties of a guild are updated.
    Requires the :attr:`~qord.Intents.guilds` to be enabled.
    """
    event_name = GatewayEvent.GUILD_UPDATE
    shard: Shard

    before: Guild
    r"""The copy of guild before the update."""

    after: Guild
    r"""The guild after the update."""
