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


@dataclass(frozen=True)
class GatewayDispatch(BaseEvent):
    r"""Structure of a :attr:`~qord.GatewayEvent.GATEWAY_DISPATCH` event.

    This event is called whenever gateway sends an event dispatch.

    This event purely exists for debugging and experimental purposes and should
    not generally be used. This event will also call for dispatch events that
    are not supported by the library.

    This event is only called when ``debug_events`` parameter is enabled in
    :class:`Client`.
    """
    event_name = GatewayEvent.GATEWAY_DISPATCH
    shard: Shard

    title: str
    r"""The title/name of event.

    This name isn't same as how library defines the events name. See Discord
    documentation for all events names.

    https://discord.dev/topics/gateway#commands-and-events
    """

    data: typing.Optional[typing.Dict[str, typing.Any]] = None
    r"""The raw event data.

    This is mostly raw JSON payload however for some events, This can be ``None``.
    """

@dataclass(frozen=True)
class ShardReady(BaseEvent):
    r"""Structure of a :attr:`~qord.GatewayEvent.SHARD_READY` event.

    This event is called whenever a shard successfully establishes
    a connection with Discord gateway and lazy loads cache for all guilds
    associated to that shard.
    """
    event_name = GatewayEvent.SHARD_READY
    shard: Shard

@dataclass(frozen=True)
class Ready(BaseEvent):
    r"""Structure of a :attr:`~qord.GatewayEvent.READY` event.

    This event is called when all shards associated to the client
    have completely prepared their guilds cache and client is in ready state.

    This event is not shard specific as such :attr:`.shard` is always ``None``.
    """
    event_name = GatewayEvent.READY
    shard = None

@dataclass(frozen=True)
class Resumed(BaseEvent):
    r"""Structure of a :attr:`~qord.GatewayEvent.RESUMED` event.

    This event is called whenver a shard is resumed i.e successfully re-establishes
    a previously disconnected session.
    """
    event_name = GatewayEvent.RESUMED

    shard: Shard
    """The shard that was resumed."""
