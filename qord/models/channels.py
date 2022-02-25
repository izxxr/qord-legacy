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
from qord.enums import ChannelType
from qord._helpers import get_optional_snowflake, parse_iso_timestamp, EMPTY

import abc
import typing

if typing.TYPE_CHECKING:
    from datetime import datetime
    from qord.models.guilds import Guild


class GuildChannel(BaseModel, abc.ABC):
    r"""The base class for channel types that are associated to a specific guild.

    Following classes currently inherit this class:

    - :class:`TextChannel`

    Attributes
    ----------
    guild: :class:`Guild`
        The guild associated to this channel.
    id: :class:`builtins.int`
        The ID of this channel.
    type: :class:`builtins.int`
        The type of this channel. See :class:`ChannelType` for more information.
    name: :class:`builtins.str`
        The name of this channel.
    position: :class:`builtins.int`
        The position of this channel in channels list.
    nsfw: :class:`builtins.bool`
        Whether this channel is marked as NSFW.
    parent_id: :class:`builtins.int`
        The ID of category that this channel is associated to.
    """

    if typing.TYPE_CHECKING:
        guild: Guild
        id: int
        type: int
        name: str
        position: int
        nsfw: bool
        parent_id: typing.Optional[int]

    __slots__ = (
        "_client",
        "_rest",
        "guild",
        "id",
        "type",
        "name",
        "position",
        "nsfw",
        "parent_id"
    )

    def __init__(self, data: typing.Dict[str, typing.Any], guild: Guild) -> None:
        self.guild = guild
        self._client = guild._client
        self._rest = guild._rest
        self._update_with_data(data)

    def _update_with_data(self, data: typing.Dict[str, typing.Any]) -> None:
        self.id = int(data["id"])
        self.type = int(data["type"])
        self.name = data["name"]
        self.position = data.get("position", 1)
        self.nsfw = data.get("nsfw", False)
        self.parent_id = get_optional_snowflake(data, "parent_id")

    @property
    def mention(self) -> str:
        r"""The string used for mentioning the channel in Discord client.

        Returns
        -------
        :class:`builtins.str`
        """
        return f"<#{self.id}>"

    async def delete(self, *, reason: str = None) -> None:
        r"""Deletes this channel.

        Requires the :attr:`~Permissions.manage_channels` on the bot
        in the parent :attr:`~GuildChannel.guild` for performing this action.

        Parameters
        ----------
        reason: :class:`builtins.str`
            The reason for performing this action.

        Raises
        ------
        HTTPForbidden
            Missing permissions.
        HTTPException
            Failed to perform this action.
        """
        await self._rest.delete_channel(channel_id=self.id, reason=reason)

    async def edit(self, **kwargs) -> None:
        raise NotImplementedError("edit() must be implemented by subclasses.")

class TextChannel(GuildChannel):
    r"""Represents a text messages based channel in a guild.

    This class inherits :class:`GuildChannel`.

    Attributes
    ----------
    topic: typing.Optional[:class:`builtins.str`]
        The topic of this channel.
    last_message_id: typing.Optional[:class:`builtins.int`]
        The ID of last message sent in this channel. Due to Discord limitation, This
        may not point to the actual last message of the channel.
    slowmode_delay: :class:`builtins.int`
        The slowmode per user (in seconds) that is set on this channel.
    default_auto_archive_duration: :class:`builtins.int`
        The default auto archiving duration (in minutes) of this channel after which
        in active threads associated to this channel are automatically archived.
    last_pin_timestamp: typing.Optional[:class:`datetime.datetime`]
        The time when last pin in this channel was created.
    """

    if typing.TYPE_CHECKING:
        topic: typing.Optional[str]
        last_message_id: typing.Optional[int]
        last_pin_timestamp: typing.Optional[datetime]
        slowmode_delay: int
        default_auto_archive_duration: int

    __slots__ = (
        "topic",
        "slowmode_delay",
        "last_message_id",
        "default_auto_archive_duration",
        "last_pin_timestamp",
    )

    def _update_with_data(self, data: typing.Dict[str, typing.Any]) -> None:
        super()._update_with_data(data)

        self.topic = data.get("topic")
        self.last_message_id = get_optional_snowflake(data, "last_message_id")
        self.slowmode_delay = data.get("rate_limit_per_user", 0)
        self.default_auto_archive_duration = data.get("default_auto_archive_duration", 60)
        last_pin_timestamp = data.get("last_pin_timestamp")
        self.last_pin_timestamp = (
            parse_iso_timestamp(last_pin_timestamp) if last_pin_timestamp is not None else None
        )

    def is_news(self) -> bool:
        r"""Checks whether the channel is a news channel.

        Returns
        -------
        :class:`builtins.bool`
        """
        return self.type is ChannelType.NEWS

    async def edit(
        self,
        *,
        name: str = EMPTY,
        type: int = EMPTY,
        position: int = EMPTY,
        topic: typing.Optional[str] = EMPTY,
        slowmode_delay: typing.Optional[int] = EMPTY,
        default_auto_archive_duration: typing.Optional[int] = EMPTY,
        reason: str = None,
    ) -> None:
        r"""Edits the channel.

        This operation requires the :attr:`~Permissions.manage_channels` permission
        for the client user in the parent guild.

        When the request is successful, This channel is updated in place with
        the returned data.

        Parameters
        ----------
        name: :class:`builtins.str`
            The name of this channel.
        type: :class:`builtins.int`
            The type of this channel. In this case, Only :attr:`~ChannelType.NEWS`
            and :attr:`~ChannelType.TEXT` are supported.
        position: :class:`builtins.int`
            The position of this channel in channels list.
        topic: :class:`builtins.str`
            The topic of this channel. ``None`` can be used to remove the topic.
        slowmode_delay: :class:`builtins.int`
            The slowmode delay of this channel (in seconds). ``None`` can be used to
            disable it. Cannot be greater then 21600 seconds.
        default_auto_archive_duration: :class:`builtins.int`
            The default auto archive duration after which in active threads
            are archived automatically (in minutes). Can be ``None`` to reset
            the default.
            Valid values are 60, 1440, 4320 and 10080.
        reason: :class:`builtins.str`
            The reason for performing this action that shows up on guild's audit log.

        Raises
        ------
        ValueError
            Invalid values supplied in some arguments.
        HTTPForbidden
            Missing permissions.
        HTTPException
            Failed to perform this action.
        """
        json = {}

        if name is not EMPTY:
            json["name"] = name

        if type is not EMPTY:
            if not type in (ChannelType.NEWS, ChannelType.TEXT):
                raise ValueError("type parameter only supports ChannelType.NEWS and TEXT.")

            json["type"] = type

        if position is not EMPTY:
            json["position"] = position

        if topic is not EMPTY:
            json["topic"] = topic

        if slowmode_delay is not EMPTY:
            if slowmode_delay is None:
                slowmode_delay = 0

            json["rate_limit_per_user"] = slowmode_delay

        if default_auto_archive_duration is not EMPTY:
            if not default_auto_archive_duration in (60, 1440, 4320, 10080):
                raise ValueError("Invalid value given for default_auto_archive_duration " \
                                "supported values are 60, 1440, 4320 and 10080.")

            json["default_auto_archive_duration"] = default_auto_archive_duration

        if json:
            data = await self._rest.edit_channel(
                channel_id=self.id,
                json=json,
                reason=reason
            )
            if data:
                self._update_with_data(data)

def _channel_factory(type: int) -> typing.Type[GuildChannel]:
    if type in (ChannelType.NEWS, ChannelType.TEXT):
        return TextChannel

    return GuildChannel