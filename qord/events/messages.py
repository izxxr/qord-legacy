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
    from qord.models.messages import Message, MessageableT

@dataclass(frozen=True)
class MessageCreate(BaseEvent):
    """Structure for :attr:`~qord.GatewayEvent.MESSAGE_CREATE` event.

    This event is called whenever a new message is sent in a guild or
    private channel.
    """
    event_name = GatewayEvent.MESSAGE_CREATE
    shard: Shard

    message: Message
    """The message that was sent."""

@dataclass(frozen=True)
class MessageDelete(BaseEvent):
    """Structure for :attr:`~qord.GatewayEvent.MESSAGE_DELETE` event.

    This event is called whenever a message is deleted.
    """
    event_name = GatewayEvent.MESSAGE_DELETE
    shard: Shard

    message: Message
    """The message that was deleted."""

@dataclass(frozen=True)
class MessageUpdate(BaseEvent):
    """Structure for :attr:`~qord.GatewayEvent.MESSAGE_UPDATE` event.

    This event is called whenever a message is updated aka edited.
    """
    event_name = GatewayEvent.MESSAGE_UPDATE
    shard: Shard

    before: Message
    """The message that was edited, before the edit happened."""

    after: Message
    """The message that was edited, after the edit happened."""


@dataclass(frozen=True)
class MessageBulkDelete(BaseEvent):
    """Structure for :attr:`~qord.GatewayEvent.MESSAGE_BULK_DELETE` event.

    This event is called whenever multiple messages are deleted at the same
    time in a channel.
    """
    event_name = GatewayEvent.MESSAGE_BULK_DELETE
    shard: Shard

    messages: typing.List[Message]
    """The list of messages that were deleted.

    This list only includes messages that could be resolved from
    the bot's cache and may not include all messages that were deleted.
    You should use :attr:`.message_ids` to get the IDs of all the messages
    deleted however do note that you cannot fetch those messages as
    they have been deleted.
    """

    channel: MessageableT
    """The channel in which messages were bulk deleted."""

    guild: typing.Optional[Guild]
    """The relevant guild if any, ``None`` if the bulk delete happened in DMs."""

    message_ids: typing.List[int]
    """The list of IDs of messages that were deleted."""
