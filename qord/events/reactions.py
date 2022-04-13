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
    from qord.models.guild_members import GuildMember
    from qord.models.users import User
    from qord.models.emojis import PartialEmoji
    from qord.models.messages import Message, Reaction


__all__ = (
    "ReactionAdd",
    "ReactionRemove",
    "ReactionClear",
    "ReactionClearEmoji",
)


@dataclass
class ReactionAdd(BaseEvent, event_name=GatewayEvent.REACTION_ADD):
    """Structure for :attr:`~qord.GatewayEvent.REACTION_ADD` event.

    This event is called whenever a reaction is added on a message.

    This requires :attr:`Intents.guild_message_reactions` or
    :attr:`Intents.direct_message_reactions` to be enabled for
    guilds and direct messages respectively.
    """
    shard: Shard

    message: Message
    """The message on which reaction was added."""

    reaction: Reaction
    """The added reaction."""

    user: typing.Union[User, GuildMember]
    """The user who added the reaction."""


@dataclass
class ReactionRemove(BaseEvent, event_name=GatewayEvent.REACTION_REMOVE):
    """Structure for :attr:`~qord.GatewayEvent.REACTION_REMOVE` event.

    This event is called whenever a reaction is removed from a message.

    This requires :attr:`Intents.guild_message_reactions` or
    :attr:`Intents.direct_message_reactions` to be enabled for
    guilds and direct messages respectively.
    """
    shard: Shard

    message: Message
    """The message from which the reaction was removed."""

    reaction: Reaction
    """The removed reaction."""

    user: typing.Union[User, GuildMember]
    """The user who removed their reaction.

    Unlike the :class:`events.ReactionAdd` event, This attribute can be
    a :class:`GuildMember` object only when :attr:`~Intents.members` intents
    are enabled as Discord does not tend to send the member data in this event.
    """


@dataclass
class ReactionClear(BaseEvent, event_name=GatewayEvent.REACTION_CLEAR):
    """Structure for :attr:`~qord.GatewayEvent.REACTION_CLEAR` event.

    This event is called whenever all reactions are cleared from
    a message at once.

    This requires :attr:`Intents.guild_message_reactions` or
    :attr:`Intents.direct_message_reactions` to be enabled for
    guilds and direct messages respectively.
    """
    shard: Shard

    message: Message
    """The message from which the reactions were cleared."""

    reactions: typing.List[Reaction]
    """The list of cleared reactions."""


@dataclass
class ReactionClearEmoji(BaseEvent, event_name=GatewayEvent.REACTION_CLEAR_EMOJI):
    """Structure for :attr:`~qord.GatewayEvent.REACTION_CLEAR_EMOJI` event.

    This event is called whenever all reactions for a specific emoji are
    cleared from a message at once.

    This requires :attr:`Intents.guild_message_reactions` or
    :attr:`Intents.direct_message_reactions` to be enabled for
    guilds and direct messages respectively.
    """
    shard: Shard

    message: Message
    """The message from which the reactions were cleared."""

    emoji: PartialEmoji
    """The emoji whose reactions were cleared."""

    reaction: Reaction
    """The reaction that was cleared."""

