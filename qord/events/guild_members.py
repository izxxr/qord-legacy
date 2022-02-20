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
    from qord.models.guild_members import GuildMember

@dataclass(frozen=True)
class GuildMemberAdd(BaseEvent):
    r"""Structure for :attr:`~qord.GatewayEvent.GUILD_MEMBER_ADD` event.

    This event is called whenever a new member joins the guild. This event
    requires the privileged intent, :attr:`~Intents.members` to be enabled.
    """
    event_name = GatewayEvent.GUILD_MEMBER_ADD
    shard: Shard

    member: GuildMember
    r"""The member that joined the :attr:`.guild`."""

    guild: Guild
    r"""The guild that was joined by the member."""

@dataclass(frozen=True)
class GuildMemberUpdate(BaseEvent):
    r"""Structure for :attr:`~qord.GatewayEvent.GUILD_MEMBER_UPDATE` event.

    This event is called whenever a guild member is updated. This event
    requires the privileged intent, :attr:`~Intents.members` to be enabled.
    """
    event_name = GatewayEvent.GUILD_MEMBER_UPDATE
    shard: Shard

    before: GuildMember
    r"""The member before the update."""

    after: GuildMember
    r"""The member after the update."""

    guild: Guild
    r"""The associated guild."""

@dataclass(frozen=True)
class GuildMemberRemove(BaseEvent):
    r"""Structure for :attr:`~qord.GatewayEvent.GUILD_MEMBER_REMOVE` event.

    This event is called whenever a member is removed from the guild. The
    removal may be in form of leaving, getting kicked or banned etc. This event
    requires the privileged intent, :attr:`~Intents.members` to be enabled.
    """
    event_name = GatewayEvent.GUILD_MEMBER_REMOVE
    shard: Shard

    member: GuildMember
    r"""The member that had left the :attr:`.guild`."""

    guild: Guild
    r"""The guild that was left by the member."""
