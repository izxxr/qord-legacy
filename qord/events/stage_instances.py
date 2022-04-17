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
    from qord.models.stage_instances import StageInstance
    from qord.models.guilds import Guild


__all__ = (
    "StageInstanceCreate",
    "StageInstanceUpdate",
    "StageInstanceDelete",
)


@dataclass
class StageInstanceCreate(BaseEvent, event_name=GatewayEvent.STAGE_INSTANCE_CREATE):
    """Structure for :attr:`~qord.GatewayEvent.STAGE_INSTANCE_CREATE` event.

    This event is called whenever a new stage instance is created in a guild.

    Requires the :attr:`~qord.Intents.guilds` intents to be enabled.
    This intent is enabled by default.
    """
    shard: Shard

    guild: Guild
    """The guild in which stage instance was created."""

    stage_instance: StageInstance
    """The created stage instance."""


@dataclass
class StageInstanceUpdate(BaseEvent, event_name=GatewayEvent.STAGE_INSTANCE_UPDATE):
    """Structure for :attr:`~qord.GatewayEvent.STAGE_INSTANCE_UPDATE` event.

    This event is called whenever a stage instance is updated in a guild.

    Requires the :attr:`~qord.Intents.guilds` intents to be enabled.
    This intent is enabled by default.
    """
    shard: Shard

    guild: Guild
    """The guild in which stage instance was created."""

    before: StageInstance
    """The stage instance before the update."""

    after: StageInstance
    """The stage instance after the update."""


@dataclass
class StageInstanceDelete(BaseEvent, event_name=GatewayEvent.STAGE_INSTANCE_DELETE):
    """Structure for :attr:`~qord.GatewayEvent.STAGE_INSTANCE_DELETE` event.

    This event is called whenever a stage instance is deleted in a guild.

    Requires the :attr:`~qord.Intents.guilds` intents to be enabled.
    This intent is enabled by default.
    """
    shard: Shard

    guild: Guild
    """The guild from which the stage instance was deleted."""

    stage_instance: StageInstance
    """The deleted stage instance."""