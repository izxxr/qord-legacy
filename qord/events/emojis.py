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
    from qord.models.emojis import Emoji
    from qord.models.guilds import Guild


__all__ = (
    "EmojisUpdate",
)


@dataclass
class EmojisUpdate(BaseEvent, event_name=GatewayEvent.EMOJIS_UPDATE):
    shard: Shard

    guild: Guild
    """The guild whose emojis were updated."""

    before: typing.List[Emoji]
    """The list of emojis before the update."""

    after: typing.List[Emoji]
    """The list of emojis after the update."""
