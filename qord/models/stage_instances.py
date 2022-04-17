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

from qord.models.base import BaseModel
from qord.internal.mixins import Comparable, CreationTime
from qord.internal.undefined import UNDEFINED
from qord.internal.helpers import get_optional_snowflake

import typing

if typing.TYPE_CHECKING:
    from qord.models.guilds import Guild
    from qord.models.channels import StageChannel
    from qord.models.scheduled_events import ScheduledEvent


__all__ = (
    "StageInstance",
)


class StageInstance(BaseModel, Comparable, CreationTime):
    """Represents a live stage instace from a :class:`StageChannel`.

    |supports-comparison|

    Attributes
    ----------
    guild: :class:`Guild`
        The guild that the stage instance is live in.
    id: :class:`builtins.int`
        The ID of stage instance.
    channel_id: :class:`builtins.int`
        The ID of channel that the stage instance is live in.
    privacy_level: :class:`builtins.int`
        The privacy level of the stage instance, see :class:`StagePrivacyLevel` for
        all possible values for this attribute.
    topic: :class:`builtins.str`
        The topic of stage instance.
    scheduled_event_id: Optional[:class:`builtins.int`]
        The scheduled event's ID that is associated to the stage instance, if any.
    """

    if typing.TYPE_CHECKING:
        id: int
        channel_id: int
        guild_id: int
        privacy_level: int
        topic: str
        scheduled_event_id: typing.Optional[int]

    __slots__ = (
        "_client",
        "guild",
        "id",
        "channel_id",
        "guild_id",
        "topic",
        "privacy_level",
        "scheduled_event_id",
    )

    def __init__(self, data: typing.Dict[str, typing.Any], guild: Guild) -> None:
        self.guild = guild
        self._client = guild._client
        self._update_with_data(data)

    def _update_with_data(self, data: typing.Dict[str, typing.Any]) -> None:
        self.id = int(data["id"])
        self.channel_id = int(data["channel_id"])
        self.guild_id = data.get("guild_id", self.guild.id)
        self.topic = data.get("topic", "")
        self.privacy_level = data.get("privacy_level", 2)
        self.scheduled_event_id = get_optional_snowflake(data, "guild_scheduled_event_id")

    @property
    def channel(self) -> typing.Optional[StageChannel]:
        """Returns the stage channel associated to this stage instance.

        Returns
        -------
        Optional[:class:`StageChannel`]
        """
        # This shall always return StageChannel
        return self.guild._cache.get_channel(self.channel_id)  # type: ignore

    @property
    def scheduled_event(self) -> typing.Optional[ScheduledEvent]:
        """Returns the scheduled event associated to the stage instance, if any.

        Returns
        -------
        Optional[:class:`ScheduledEvent`]
        """
        event_id = self.scheduled_event_id

        if event_id is None:
            return None

        return self.guild._cache.get_scheduled_event(event_id)

    async def delete(self, *, reason: typing.Optional[str] = None) -> None:
        """Deletes the stage instance.

        This operation requires the bot to be stage moderator, i.e has following
        permissions in the stage channel:

        - :attr:`~Permissions.manage_channels`
        - :attr:`~Permissions.move_members`
        - :attr:`~Permissions.mute_members`

        Parameters
        ----------
        reason: :class:`builtins.str`
            The reason for doing this action.

        Raises
        ------
        HTTPForbidden
            You are not allowed to do this.
        HTTPException
            The operation failed.
        """
        await self._client._rest.delete_stage_instance(
            channel_id=self.channel_id,
            reason=reason,
        )

    async def edit(
        self,
        topic: str = UNDEFINED,
        privacy_level: int = UNDEFINED,
        reason: typing.Optional[str] = None,
    ) -> None:
        """Edits the stage instance.

        This operation requires the bot to be stage moderator, i.e has following
        permissions in the stage channel:

        - :attr:`~Permissions.manage_channels`
        - :attr:`~Permissions.move_members`
        - :attr:`~Permissions.mute_members`

        Parameters
        ----------
        topic: :class:`builtins.str`
            The topic of this tage instance.
        privacy_level: :class:`builtins.int`
            The privacy level of stage instance, see :class:`StagePrivacyLevel` for
            all possible values.
        reason: :class:`builtins.str`
            The reason for doing this action.

        Raises
        ------
        HTTPForbidden
            You are not allowed to do this.
        HTTPException
            The operation failed.
        """
        json = {}

        if topic is not UNDEFINED:
            json["topic"] = topic

        if privacy_level is not UNDEFINED:
            json["privacy_level"] = privacy_level

        if json:
            data = await self._client._rest.edit_stage_instance(
                channel_id=self.channel_id,
                json=json,
                reason=reason,
            )
            self._update_with_data(data)
