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
from qord._helpers import get_optional_snowflake, parse_iso_timestamp

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

    def is_higher_than(self, other: GuildChannel) -> bool:
        r"""Compares this channel with another channel of the same guild
        and checks whether this channel is higher than the other in the
        channels list.

        Parameters
        ----------
        other: :class:`GuildChannel`
            The channel to check against.

        Raises
        -------
        RuntimeError
            The provided channel is not associated to the guild
            that this channel is associated to.
        """
        if not isinstance(other, GuildChannel):
            raise TypeError("Parameter other must be an instance of GuildChannel.")
        if self.guild.id != other.guild.id:
            raise RuntimeError("Cannot compare against channels of different guild.")

        if self.position == other.position:
            return self.id > other.id

        return self.position > other.position

    def is_lower_than(self, other: GuildChannel) -> bool:
        r"""Compares this channel with another channel of the same guild
        and checks whether this channel is lower than the other in the
        channels list.

        Parameters
        ----------
        other: :class:`GuildChannel`
            The channel to check against.

        Raises
        -------
        RuntimeError
            The provided channel is not associated to the guild
            that this channel is associated to.
        """
        return (not self.is_higher_than(other))


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


def _guild_channel_factory(type: int) -> typing.Type[GuildChannel]:
    if type in (ChannelType.NEWS, ChannelType.TEXT):
        return TextChannel

    return GuildChannel