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
from qord.models.users import User
from qord.bases import MessagesSupported
from qord.enums import ChannelType
from qord._helpers import get_optional_snowflake, parse_iso_timestamp, UNDEFINED

import typing

if typing.TYPE_CHECKING:
    from datetime import datetime
    from qord.core.client import Client
    from qord.models.guilds import Guild
    from qord.models.users import User


class GuildChannel(BaseModel):
    """The base class for channel types that are associated to a specific guild.

    For each channel types, Library provides separate subclasses that implement
    related functionality for that channel type.

    Following classes currently inherit this class:

    - :class:`TextChannel`
    - :class:`NewsChannel`
    - :class:`CategoryChannel`
    - :class:`VoiceChannel`
    - :class:`StageChannel`

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
        self.parent_id = get_optional_snowflake(data, "parent_id")

    @property
    def mention(self) -> str:
        """The string used for mentioning the channel in Discord client.

        Returns
        -------
        :class:`builtins.str`
        """
        return f"<#{self.id}>"

    async def delete(self, *, reason: str = None) -> None:
        """Deletes this channel.

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


class TextChannel(GuildChannel, MessagesSupported):
    """Represents a text messages based channel in a guild.

    This class inherits :class:`GuildChannel` and :class:`MessagesSupported`.

    Attributes
    ----------
    topic: Optional[:class:`builtins.str`]
        The topic of this channel.
    last_message_id: Optional[:class:`builtins.int`]
        The ID of last message sent in this channel. Due to Discord limitation, This
        may not point to the actual last message of the channel.
    slowmode_delay: :class:`builtins.int`
        The slowmode per user (in seconds) that is set on this channel.
    nsfw: :class:`builtins.bool`
        Whether this channel is marked as NSFW.
    default_auto_archive_duration: :class:`builtins.int`
        The default auto archiving duration (in minutes) of this channel after which
        in active threads associated to this channel are automatically archived.
    last_pin_timestamp: Optional[:class:`datetime.datetime`]
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
        "nsfw",
        "last_pin_timestamp",
    )

    def _update_with_data(self, data: typing.Dict[str, typing.Any]) -> None:
        super()._update_with_data(data)

        self.topic = data.get("topic")
        self.last_message_id = get_optional_snowflake(data, "last_message_id")
        self.slowmode_delay = data.get("rate_limit_per_user", 0)
        self.default_auto_archive_duration = data.get("default_auto_archive_duration", 60)
        self.nsfw = data.get("nsfw", False)
        last_pin_timestamp = data.get("last_pin_timestamp")
        self.last_pin_timestamp = (
            parse_iso_timestamp(last_pin_timestamp) if last_pin_timestamp is not None else None
        )

    async def _get_message_channel(self) -> typing.Any:
        return self

    async def edit(
        self,
        *,
        name: str = UNDEFINED,
        type: int = UNDEFINED,
        position: int = UNDEFINED,
        nsfw: bool = UNDEFINED,
        parent: typing.Optional[CategoryChannel] = UNDEFINED,
        topic: typing.Optional[str] = UNDEFINED,
        slowmode_delay: typing.Optional[int] = UNDEFINED,
        default_auto_archive_duration: int = UNDEFINED,
        reason: str = None,
    ) -> None:
        """Edits the channel.

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
        parent: Optional[:class:`CategoryChannel`]
            The parent category in which this channel should be moved to. ``None`` to
            remove current category of this channel.
        nsfw: :class:`builtins.bool`
            Whether this channel is marked as NSFW.
        topic: Optional[:class:`builtins.str`]
            The topic of this channel. ``None`` can be used to remove the topic.
        slowmode_delay: Optional[:class:`builtins.int`]
            The slowmode delay of this channel (in seconds). ``None`` can be used to
            disable it. Cannot be greater then 21600 seconds.
        default_auto_archive_duration: :class:`builtins.int`
            The default auto archive duration after which in active threads
            are archived automatically (in minutes). Valid values are 60, 1440, 4320 and 10080.
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

        if name is not UNDEFINED:
            json["name"] = name

        if type is not UNDEFINED:
            if not type in (ChannelType.NEWS, ChannelType.TEXT):
                raise ValueError("type parameter only supports ChannelType.NEWS and TEXT.")

            json["type"] = type

        if position is not UNDEFINED:
            json["position"] = position

        if nsfw is not UNDEFINED:
            json["nsfw"] = nsfw

        if topic is not UNDEFINED:
            json["topic"] = topic

        if slowmode_delay is not UNDEFINED:
            if slowmode_delay is None:
                slowmode_delay = 0

            json["rate_limit_per_user"] = slowmode_delay

        if default_auto_archive_duration is not UNDEFINED:
            if not default_auto_archive_duration in (60, 1440, 4320, 10080):
                raise ValueError("Invalid value given for default_auto_archive_duration " \
                                "supported values are 60, 1440, 4320 and 10080.")

            json["default_auto_archive_duration"] = default_auto_archive_duration

        if parent is not UNDEFINED:
            json["parent_id"] = parent.id if parent is not None else None

        if json:
            data = await self._rest.edit_channel(
                channel_id=self.id,
                json=json,
                reason=reason
            )
            if data:
                self._update_with_data(data)


class NewsChannel(TextChannel):
    """Represents a news channel that holds other guild channels.

    This class inherits :class:`TextChannel` so all attributes of
    :class:`TextChannel` and :class:`GuildChannel` classes are valid here too.

    Currently this class has no extra functionality compared to :class:`TextChannel`.
    """

    __slots__ = ()

class CategoryChannel(GuildChannel):
    """Represents a category channel that holds other guild channels.

    This class inherits the :attr:`GuildChannel` class.
    """

    __slots__ = ()

    @property
    def channels(self) -> typing.List[GuildChannel]:
        """The list of channels associated to this category.

        Returns
        -------
        List[:class:`GuildChannel`]
        """
        channels = self.guild.cache.channels()
        return [channel for channel in channels if channel.parent_id == self.id]

    async def edit(
        self,
        *,
        name: str = UNDEFINED,
        position: int = UNDEFINED,
        reason: str = None,
    ) -> None:
        """Edits the channel.

        This operation requires the :attr:`~Permissions.manage_channels` permission
        for the client user in the parent guild.

        When the request is successful, This channel is updated in place with
        the returned data.

        Parameters
        ----------
        name: :class:`builtins.str`
            The name of this channel.
        position: :class:`builtins.int`
            The position of this channel in channels list.
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

        if name is not UNDEFINED:
            json["name"] = name

        if position is not UNDEFINED:
            json["position"] = position

        if json:
            data = await self._rest.edit_channel(
                channel_id=self.id,
                json=json,
                reason=reason
            )
            if data:
                self._update_with_data(data)


class VoiceChannel(GuildChannel):
    """Represents a voice channel in a guild.

    This class inherits the :class:`GuildChannel` class.

    Attributes
    ----------
    bitrate: :class:`builtins.int`
        The bitrate of this channel, in bits.
    user_limit: :class:`builtins.int`
        The number of users that can connect to this channel at a time. The
        value of ``0`` indicates that there is no limit set.
    rtc_region: Optional[:class:`builtins.str`]
        The string representation of RTC region of the voice channel. This
        is only available when a region is explicitly set. ``None`` indicates
        that region is chosen automatically.
    video_quality_mode: :class:`builtins.int`
        The video quality mode of this channel. See :class:`VideoQualityMode` for
        more information.
    """
    if typing.TYPE_CHECKING:
        bitrate: int
        user_limit: int
        video_quality_mode: int
        rtc_region: typing.Optional[str]

    __slots__ = (
        "bitrate",
        "rtc_region",
        "user_limit",
        "video_quality_mode",
    )

    def _update_with_data(self, data: typing.Dict[str, typing.Any]) -> None:
        super()._update_with_data(data)

        self.bitrate = data.get("bitrate") # type: ignore
        self.rtc_region = data.get("rtc_region")
        self.user_limit = data.get("user_limit", 0)
        self.video_quality_mode = data.get("video_quality_mode", 1)

    async def edit(
        self,
        *,
        name: str = UNDEFINED,
        position: int = UNDEFINED,
        bitrate: int = UNDEFINED,
        parent: typing.Optional[CategoryChannel] = UNDEFINED,
        rtc_region: typing.Optional[str] = UNDEFINED,
        user_limit: typing.Optional[int] = UNDEFINED,
        video_quality_mode: int = UNDEFINED,
        reason: str = None,
    ) -> None:
        """Edits the channel.

        This operation requires the :attr:`~Permissions.manage_channels` permission
        for the client user in the parent guild.

        When the request is successful, This channel is updated in place with
        the returned data.

        Parameters
        ----------
        name: :class:`builtins.str`
            The name of this channel.
        position: :class:`builtins.int`
            The position of this channel in channels list.
        parent: Optional[:class:`CategoryChannel`]
            The parent category in which this channel should be moved to. ``None`` to
            remove current category of this channel.
        bitrate: :class:`builtins.int`
            The bitrate of this channel in bits. This value can be in range of 8000
            and 96000 (128000 for VIP servers).
        rtc_region: Optional[:class:`builtins.str`]
            The RTC region of this voice channel. ``None`` can be used to
            set this to automatic selection of regions.
        user_limit: Optional[:class:`builtins.int`]
            The number of users that can connect to the channel at a time.
            ``None`` or ``0`` will remove the explicit limit allowing unlimited
            number of users.
        video_quality_mode: :class:`builtins.int`
            The video quality mode of the voice channel. See :class:`VideoQualityMode`
            for valid values.
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

        if name is not UNDEFINED:
            json["name"] = name

        if position is not UNDEFINED:
            json["position"] = position

        if rtc_region is not UNDEFINED:
            json["rtc_region"] = rtc_region

        if bitrate is not UNDEFINED:
            if bitrate < 8000 or bitrate > 128000:
                raise ValueError("Parameter 'bitrate' must be in range of 8000 and 128000")

            json["bitrate"] = bitrate

        if user_limit is not UNDEFINED:
            if user_limit is None:
                user_limit = 0

            json["user_limit"] = user_limit

        if video_quality_mode is not UNDEFINED:
            json["video_quality_mode"] = video_quality_mode

        if parent is not UNDEFINED:
            json["parent_id"] = parent.id if parent is not None else None

        if json:
            data = await self._rest.edit_channel(
                channel_id=self.id,
                json=json,
                reason=reason
            )
            if data:
                self._update_with_data(data)


class StageChannel(VoiceChannel):
    """Represents a stage channel in a guild.

    This class is a subclass of :class:`VoiceChannel` as such all attributes
    of :class:`VoiceChannel` and :class:`GuildChannel` are valid in this class too.

    Currently this class has no extra functionality compared to :class:`VoiceChannel`,
    More functionality will be included when stage instances are supported
    by the library.
    """

    __slots__ = ()

class PrivateChannel(BaseModel):
    """Base class for channel types that are private and not associated to a guild.

    Currently only one channel type is available for private channels that is
    :class:`DMChannel`.

    Attributes
    ----------
    id: :class:`builtins.int`
        The ID of this channel.
    type: :class:`builtins.int`
        The type of this channel. See :class:`ChannelType` for valid values.
    """
    if typing.TYPE_CHECKING:
        id: int
        type: int

    __slots__ = ("id", "type", "_client", "_cache", "_rest")

    def __init__(self, data: typing.Dict[str, typing.Any], client: Client) -> None:
        self._client = client
        self._rest = client._rest
        self._cache = client._cache
        self._update_with_data(data)

    def _update_with_data(self, data: typing.Dict[str, typing.Any]) -> None:
        self.id = int(data["id"])
        self.type = int(data["type"])

class DMChannel(PrivateChannel, MessagesSupported):
    """Represents a direct message channel between two users.

    This class inherits :class:`PrivateChannel`.

    Attributes
    ----------
    recipient: :class:`User`
        The user that this direct message is with.
    last_message_id: Optional[:class:`builtins.int`]
        The ID of last message associated to this channel. May not be accurate.
    last_pin_timestamp: Optional[:class:`datetime`]
        The time when last pin in the channel was created.
    """
    if typing.TYPE_CHECKING:
        last_message_id: typing.Optional[int]
        last_pin_timestamp: typing.Optional[datetime]
        recipient: User

    __slots__ = (
        "last_message_id",
        "last_pin_timestamp",
        "recipient"
    )

    def _update_with_data(self, data: typing.Dict[str, typing.Any]) -> None:
        super()._update_with_data(data)

        recipient_data = data["recipients"][0]
        recipient = self._cache.get_user(int(recipient_data["id"]))

        if recipient is None:
            recipient = User(recipient_data, client=self._client)

        pin_ts = data.get("last_pin_timestamp")

        self.last_pin_timestamp = parse_iso_timestamp(pin_ts) if pin_ts is not None else None
        self.recipient = recipient
        self.last_message_id = get_optional_snowflake(data, "last_message_id")

    async def _get_message_channel(self) -> typing.Any:
        return self


def _is_guild_channel(type: int) -> bool:
    return type in (
        ChannelType.TEXT,
        ChannelType.NEWS,
        ChannelType.CATEGORY,
        ChannelType.VOICE,
        ChannelType.STAGE,
        ChannelType.STORE,
    )

def _guild_channel_factory(type: int) -> typing.Type[GuildChannel]:
    if type is ChannelType.TEXT:
        return TextChannel
    if type is ChannelType.NEWS:
        return NewsChannel
    if type is ChannelType.CATEGORY:
        return CategoryChannel
    if type is ChannelType.VOICE:
        return VoiceChannel
    if type is ChannelType.STAGE:
        return StageChannel

    return GuildChannel

def _private_channel_factory(type: int) -> typing.Type[PrivateChannel]:
    if type is ChannelType.DM:
        return DMChannel

    return PrivateChannel
