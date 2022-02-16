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
    from qord.models.roles import Role
    from qord.models.guilds import Guild

@dataclass(frozen=True)
class RoleCreate(BaseEvent):
    r"""Structure for :attr:`~qord.GatewayEvent.ROLE_CREATE` event.

    This event is called whenever a role is created in a guild.
    """
    event_name = GatewayEvent.ROLE_CREATE
    shard: Shard

    role: Role
    r"""The role that was created."""

    guild: Guild
    r"""The guild that the created role belonged to."""

@dataclass(frozen=True)
class RoleUpdate(BaseEvent):
    r"""Structure for :attr:`~qord.GatewayEvent.ROLE_UPDATE` event.

    This event is called whenever one or more properties of a guild role
    are updated.
    """
    event_name = GatewayEvent.ROLE_UPDATE
    shard: Shard

    before: Role
    r"""The role before the update."""

    after: Role
    r"""The role after the update."""

    guild: Guild
    r"""The guild that the updated role belonged to."""

@dataclass(frozen=True)
class RoleDelete(BaseEvent):
    r"""Structure for :attr:`~qord.GatewayEvent.ROLE_DELETE` event.

    This event is called whenever a role is deleted in a guild.
    """
    event_name = GatewayEvent.ROLE_DELETE
    shard: Shard

    role: Role
    r"""The deleted role."""

    guild: Guild
    r"""The guild that the updated role belonged to."""
