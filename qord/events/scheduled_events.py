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
    from qord.models.scheduled_events import ScheduledEvent
    from qord.models.guilds import Guild
    from qord.models.guild_members import GuildMember


__all__ = (
    "ScheduledEventCreate",
    "ScheduledEventUpdate",
    "ScheduledEventDelete",
    "ScheduledEventUserAdd",
    "ScheduledEventUserRemove",
)


@dataclass
class ScheduledEventCreate(BaseEvent, event_name=GatewayEvent.SCHEDULED_EVENT_CREATE):
    """Structure for :attr:`~qord.GatewayEvent.SCHEDULED_EVENT_CREATE` event.

    This event is called whenever a new scheduled event is created in a guild.

    Requires the :attr:`~qord.Intents.scheduled_events` intents to be enabled.
    This intent is enabled by default.
    """
    shard: Shard

    guild: Guild
    """The guild in which event was created."""

    scheduled_event: ScheduledEvent
    """The created scheduled event."""


@dataclass
class ScheduledEventUpdate(BaseEvent, event_name=GatewayEvent.SCHEDULED_EVENT_UPDATE):
    """Structure for :attr:`~qord.GatewayEvent.SCHEDULED_EVENT_UPDATE` event.

    This event is called whenever a scheduled event is updated in a guild.

    Requires the :attr:`~qord.Intents.scheduled_events` intents to be enabled.
    This intent is enabled by default.
    """
    shard: Shard

    guild: Guild
    """The guild in which event was created."""

    before: ScheduledEvent
    """The scheduled event before the update."""

    after: ScheduledEvent
    """The scheduled event after the update."""


@dataclass
class ScheduledEventDelete(BaseEvent, event_name=GatewayEvent.SCHEDULED_EVENT_DELETE):
    """Structure for :attr:`~qord.GatewayEvent.SCHEDULED_EVENT_DELETE` event.

    This event is called whenever a scheduled event is deleted in a guild.

    Requires the :attr:`~qord.Intents.scheduled_events` intents to be enabled.
    This intent is enabled by default.
    """
    shard: Shard

    guild: Guild
    """The guild from which the event was deleted."""

    scheduled_event: ScheduledEvent
    """The deleted scheduled event."""


@dataclass
class ScheduledEventUserAdd(BaseEvent, event_name=GatewayEvent.SCHEDULED_EVENT_USER_ADD):
    """Structure for :attr:`~qord.GatewayEvent.SCHEDULED_EVENT_USER_ADD` event.

    This event is called whenever a user subscribes to a scheduled event.

    Requires the :attr:`~qord.Intents.scheduled_events` intents to be enabled.
    This intent is enabled by default.
    """
    shard: Shard

    guild: Guild
    """The guild that the event belongs to."""

    scheduled_event: ScheduledEvent
    """The scheduled event on which user subscribed."""

    user_id: int
    """The ID of user who subscribed."""

    user: typing.Optional[GuildMember]
    """The user who subscribed.

    **This can be ``None``!** When :attr:`~qord.Intents.members` are not enabled or member
    isn't cached by any chance, This attribute can be ``None``. You should consider fetching
    the member via :meth:`Guild.fetch_member` with the given :attr:`.user_id`.
    """


@dataclass
class ScheduledEventUserRemove(BaseEvent, event_name=GatewayEvent.SCHEDULED_EVENT_USER_REMOVE):
    """Structure for :attr:`~qord.GatewayEvent.SCHEDULED_EVENT_USER_REMOVE` event.

    This event is called whenever a user unsubscribes to a scheduled event.

    Requires the :attr:`~qord.Intents.scheduled_events` intents to be enabled.
    This intent is enabled by default.
    """
    shard: Shard

    guild: Guild
    """The guild that the event belongs to."""

    scheduled_event: ScheduledEvent
    """The scheduled event on which user unsubscribed."""

    user_id: int
    """The ID of user who unsubscribed."""

    user: typing.Optional[GuildMember]
    """The user who unsubscribed.

    **This can be ``None``!** When :attr:`~qord.Intents.members` are not enabled or member
    isn't cached by any chance, This attribute can be ``None``. You should consider fetching
    the member via :meth:`Guild.fetch_member` with the given :attr:`.user_id`.
    """
