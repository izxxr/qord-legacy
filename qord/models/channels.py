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
from qord.models.stage_instances import StageInstance
from qord.bases import BaseMessageChannel
from qord.enums import ChannelPermissionType, ChannelType, StagePrivacyLevel
from qord.internal.helpers import get_optional_snowflake, parse_iso_timestamp
from qord.internal.undefined import UNDEFINED
from qord.internal.mixins import Comparable, CreationTime
from qord.flags.permissions import Permissions
from qord.dataclasses.permission_overwrite import PermissionOverwrite

import typing

if typing.TYPE_CHECKING:
    from datetime import datetime
    from qord.core.client import Client
    from qord.models.guilds import Guild
    from qord.models.users import User
    from qord.models.guild_members import GuildMember
    from qord.models.roles import Role


__all__ = (
    "ChannelPermission",
    "GuildChannel",
    "TextChannel",
    "NewsChannel",
    "CategoryChannel",
    "VoiceChannel",
    "StageChannel",
    "PrivateChannel",
    "DMChannel",
)


class ChannelPermission(BaseModel):
    """Represents the detail of a channel permission override for a specific target.

    This class supports comparison between other :class:`ChannelPermission` objects
    considering both having same target and same permission overrides.

    Attributes
    ----------
    target_id: :class:`builtins.int`
        The ID of target that this permission overwrite is for. This can either
        be ID of a role or member.
    type: :class:`builtins.int`
        The type of target that this permission overwrite is for.
        See :class:`ChannelPermissionType` for possible values.
    permission_overwrite: :class:`PermissionOverwrite`
        The permission overwrite for the given target.
    """

    if typing.TYPE_CHECKING:
        target_id: int
        target_type: int
        permission_overwrite: PermissionOverwrite
        channel: GuildChannel

    __slots__ = (
        "channel",
        "target_id",
        "target_type",
        "permission_overwrite",
        "_client",
        "_allow",
        "_deny",
    )

    def __init__(self, data: typing.Dict[str, typing.Any], channel: GuildChannel) -> None:
        self.channel = channel
        self._client = channel._client
        self._update_with_data(data)

    def _update_with_data(self, data: typing.Dict[str, typing.Any]) -> None:
        allow, deny = (
            Permissions(int(data["allow"])),
            Permissions(int(data["deny"])),
        )

        # Raw bitwise values (private)
        self._allow = allow.value
        self._deny = deny.value

        self.target_id = int(data["id"])
        self.target_type = data["type"]
        self.permission_overwrite = PermissionOverwrite.from_permissions(allow, deny)

    def __eq__(self, other: typing.Any) -> bool:
        if isinstance(other, self.__class__):
            return (
                self.permission_overwrite == other.permission_overwrite and
                self.target_id == other.target_id
            )

        return False

    @property
    def target(self) -> typing.Optional[typing.Union[Role, GuildMember]]:
        """The target that the permission is for.

        .. note::
            This property is resolved from relevant channel's guild cache.
            If the client is missing :attr:`Intents.members` and the permission
            override is for a guild member, This would potentially return ``None``.
            In which case, you should consider fetching the member directly using
            the given :attr:`.target_id`

        Returns
        -------
        Optional[:class:`Role`, :class:`GuildMember`]
            The resolved target, or ``None`` if couldn't be resolved.
        """
        cache = self.channel.guild.cache
        target_type = self.target_type

        if target_type == ChannelPermissionType.ROLE:
            return cache.get_role(self.target_id)

        elif target_type == ChannelPermissionType.MEMBER:
            return cache.get_member(self.target_id)


class GuildChannel(BaseModel, Comparable, CreationTime):
    """The base class for channel types that are associated to a specific guild.

    For each channel types, Library provides separate subclasses that implement
    related functionality for that channel type.

    Following classes currently inherit this class:

    - :class:`TextChannel`
    - :class:`NewsChannel`
    - :class:`CategoryChannel`
    - :class:`VoiceChannel`
    - :class:`StageChannel`

    |supports-comparison|

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
        parent_id: typing.Optional[int]
        _permissions: typing.Dict[int, ChannelPermission]

    __slots__ = (
        "_client",
        "_rest",
        "guild",
        "id",
        "type",
        "name",
        "position",
        "parent_id",
        "_permissions",
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
        self._permissions = {
            int(po["id"]): ChannelPermission(po, channel=self)
            for po in data.get("permission_overwrites", [])
        }

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, name={self.name!r}, position={self.position}, type={self.type})"

    @property
    def mention(self) -> str:
        """The string used for mentioning the channel in Discord client.

        Returns
        -------
        :class:`builtins.str`
        """
        return f"<#{self.id}>"

    @property
    def permissions(self) -> typing.List[ChannelPermission]:
        """The list of permission overwrites set on this channel.

        Returns
        -------
        List[:class:`ChannelPermission`]
        """
        return list(self._permissions.values())

    @property
    def url(self) -> str:
        """The URL for this channel.

        Returns
        -------
        :class:`builtins.str`
        """
        return f"https://discord.com/channels/{self.guild.id}/{self.id}"

    def permission_overwrite_for(self, target: typing.Union[GuildMember, User, Role]) -> typing.Optional[PermissionOverwrite]:
        """Gets the permission overwrite for the given target.

        Parameters
        ----------
        target: Union[:class:`Role`, :class:`User`, :class:`GuildMember`]
            The target to get the overwrite for.

        Returns
        -------
        Optional[:class:`PermissionOverwrite`]
            The permission overwrite, if any. If no overwrite is explicitly
            configured, None is returned.
        """
        permission = self._permissions.get(target.id)

        if permission is not None:
            return permission.permission_overwrite

    def _get_permission(self, target: typing.Any) -> typing.Optional[ChannelPermission]:
        # This method is for internal usage in permissions_in() methods
        return self._permissions.get(target.id)

    async def delete(self, *, reason: typing.Optional[str] = None) -> None:
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

    async def _edit_permission_overwrites_payload(
        self,
        permission_overwrites: typing.Dict[typing.Union[GuildMember, User, Role], PermissionOverwrite]
    ) -> typing.List[typing.Dict[str, typing.Any]]:

        # Circular imports
        from qord.models.guild_members import GuildMember
        from qord.models.roles import Role

        ret = []

        for obj, overwrite in permission_overwrites.items():
            if isinstance(obj, (GuildMember, User)):
                target_type = ChannelPermissionType.MEMBER
            elif isinstance(obj, Role):
                target_type = ChannelPermissionType.ROLE
            else:
                raise TypeError(f"Expected key of permission_overwrites dictionary to be an instance of GuildMember or Role, got {obj.__class__}")

            allow, deny = overwrite.permissions()
            ret.append({
                "id": obj.id,
                "type": target_type,
                "allow": allow.value,
                "deny": deny.value,
            })

        return ret

    async def set_permission_overwrite(
        self,
        target: typing.Union[GuildMember, User, Role],
        overwrite: PermissionOverwrite,
        reason: typing.Optional[str] = None,
    ) -> None:
        """Sets a permission overwrite for the given target on the channel.

        This requires :attr:`~Permissions.manage_channels` permission for the
        given channel and only those permissions that the bot has can be overriden
        in the overwrite.

        Parameters
        ----------
        target: Union[:class:`GuildMember`, :class:`User`, :class:`Role`]
            The role or member for which the permission overwrite is being set.
        overwrite: :class:`PermissionOverwrite`
            The new permission overwrite to set.
        reason: :class:`builtins.str`
            The audit log reason for this operation.

        Raises
        ------
        HTTPForbidden
            You are not allowed to do this or you are trying to override
            permissions that are not on the bot.
        HTTPException
            The operation failed.
        """
        # Circular imports
        from qord.models.guild_members import GuildMember
        from qord.models.roles import Role

        if isinstance(target, (GuildMember, User)):
            target_type = ChannelPermissionType.MEMBER
        elif isinstance(target, Role):
            target_type = ChannelPermissionType.ROLE
        else:
            raise TypeError(f"Expected key of permission_overwrites dictionary to be an instance of GuildMember or Role, got {target.__class__}")

        allow, deny = overwrite.permissions()
        json = {
            "type": target_type,
            "allow": allow.value,
            "deny": deny.value,
        }

        await self._rest.set_permission_overwrite(
            channel_id=self.id,
            overwrite_id=target.id,
            json=json,
            reason=reason
        )

    async def remove_permission_overwrite(
        self,
        target: typing.Union[GuildMember, User, Role],
        reason: typing.Optional[str] = None,
    ) -> None:
        """Removes the permission overwrite for the given targets.

        This requires :attr:`~Permissions.manage_channels` permission
        in the given channel.

        Parameters
        ----------
        target: Union[:class:`GuildMember`, :class:`User`, :class:`Role`]
            The role or member for which the permission overwrite
            is being removed.
        reason: :class:`builtins.str`
            The audit log reason for this operation.

        Raises
        ------
        HTTPForbidden
            You are not allowed to do this.
        HTTPNotFound
            Permission overwrite does not exist for this user.
        HTTPException
            The operation failed.
        """
        await self._rest.remove_permission_overwrite(
            channel_id=self.id,
            overwrite_id=target.id,
            reason=reason
        )

    # TODO: Refactor this to take common parameters like name and permission_overwrites
    async def edit(self, **kwargs) -> None:
        raise NotImplementedError("edit() must be implemented by subclasses.")


class TextChannel(GuildChannel, BaseMessageChannel):
    """Represents a text messages based channel in a guild.

    This class inherits :class:`GuildChannel` and :class:`BaseMessageChannel`.

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
        permission_overwrites: typing.Dict[typing.Union[GuildMember, User, Role], PermissionOverwrite] = UNDEFINED,
        reason: typing.Optional[str] = None,
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
        permission_overwrites: Dict[Union[:class:`GuildMember`, :class:`User`, :class:`Role`], :class:`PermissionOverwrite`]
            The permission overwrites of this channel. This is a dictionary with key being the
            target whose permission overwrite is being edited and value is the new
            permission overwrite.
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
                                "supported values are 60, 1440, 4320 and 10080.") # type: ignore

            json["default_auto_archive_duration"] = default_auto_archive_duration

        if parent is not UNDEFINED:
            json["parent_id"] = parent.id if parent is not None else None

        if permission_overwrites is not UNDEFINED:
            json["permission_overwrites"] = self._edit_permission_overwrites_payload(permission_overwrites)

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
        permission_overwrites: typing.Dict[typing.Union[GuildMember, User, Role], PermissionOverwrite] = UNDEFINED,
        reason: typing.Optional[str] = None,
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
        permission_overwrites: Dict[Union[:class:`GuildMember`, :class:`User`, :class:`Role`], :class:`PermissionOverwrite`]
            The permission overwrites of this channel. This is a dictionary with key being the
            target whose permission overwrite is being edited and value is the new
            permission overwrite.
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

        if permission_overwrites is not UNDEFINED:
            json["permission_overwrites"] = self._edit_permission_overwrites_payload(permission_overwrites)

        if json:
            data = await self._rest.edit_channel(
                channel_id=self.id,
                json=json,
                reason=reason
            )
            if data:
                self._update_with_data(data)


class VoiceChannel(GuildChannel, BaseMessageChannel):
    """Represents a voice channel in a guild.

    This class inherits the :class:`GuildChannel` class.

    Attributes
    ----------
    nsfw: :class:`builtins.bool`
        Whether the channel is marked as NSFW.
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
        nsfw: bool
        bitrate: int
        user_limit: int
        video_quality_mode: int
        rtc_region: typing.Optional[str]

    __slots__ = (
        "bitrate",
        "rtc_region",
        "user_limit",
        "video_quality_mode",
        "nsfw",
    )

    def _update_with_data(self, data: typing.Dict[str, typing.Any]) -> None:
        super()._update_with_data(data)

        self.nsfw = data.get("nsfw", False)
        self.bitrate = data.get("bitrate") # type: ignore
        self.rtc_region = data.get("rtc_region")
        self.user_limit = data.get("user_limit", 0)
        self.video_quality_mode = data.get("video_quality_mode", 1)

    async def _get_message_channel(self) -> typing.Any:
        return self

    async def edit(
        self,
        *,
        name: str = UNDEFINED,
        position: int = UNDEFINED,
        bitrate: int = UNDEFINED,
        nsfw: bool = UNDEFINED,
        parent: typing.Optional[CategoryChannel] = UNDEFINED,
        rtc_region: typing.Optional[str] = UNDEFINED,
        user_limit: typing.Optional[int] = UNDEFINED,
        video_quality_mode: int = UNDEFINED,
        permission_overwrites: typing.Dict[typing.Union[GuildMember, User, Role], PermissionOverwrite] = UNDEFINED,
        reason: typing.Optional[str] = None,
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
        nsfw: :class:`builtins.bool`
            Whether the channel should be marked as NSFW.
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
        permission_overwrites: Dict[Union[:class:`GuildMember`, :class:`User`, :class:`Role`], :class:`PermissionOverwrite`]
            The permission overwrites of this channel. This is a dictionary with key being the
            target whose permission overwrite is being edited and value is the new
            permission overwrite.
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

        if nsfw is not UNDEFINED:
            json["nsfw"] = nsfw

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

        if permission_overwrites is not UNDEFINED:
            json["permission_overwrites"] = self._edit_permission_overwrites_payload(permission_overwrites)

        if json:
            data = await self._rest.edit_channel(
                channel_id=self.id,
                json=json,
                reason=reason
            )
            if data:
                self._update_with_data(data)


class StageChannel(GuildChannel):
    """Represents a stage channel in a guild.

    Attributes
    ----------
    bitrate: :class:`builtins.int`
        The bitrate of this channel, in bits.
    rtc_region: Optional[:class:`builtins.str`]
        The string representation of RTC region of the voice channel. This
        is only available when a region is explicitly set. ``None`` indicates
        that region is chosen automatically.
    """
    if typing.TYPE_CHECKING:
        bitrate: int
        rtc_region: typing.Optional[str]

    __slots__ = (
        "bitrate",
        "rtc_region",
    )

    def _update_with_data(self, data: typing.Dict[str, typing.Any]) -> None:
        super()._update_with_data(data)

        self.bitrate = data.get("bitrate") # type: ignore
        self.rtc_region = data.get("rtc_region")

    @property
    def stage_instance(self) -> typing.Optional[StageInstance]:
        """The stage instance belonging to this channel. If any.

        Returns
        -------
        Optional[:class:`StageInstance`]
        """
        for stage_instance in self.guild._cache.stage_instances():
            if stage_instance.channel_id == self.id:
                return stage_instance
    async def edit(
        self,
        *,
        name: str = UNDEFINED,
        position: int = UNDEFINED,
        bitrate: int = UNDEFINED,
        parent: typing.Optional[CategoryChannel] = UNDEFINED,
        rtc_region: typing.Optional[str] = UNDEFINED,
        permission_overwrites: typing.Dict[typing.Union[GuildMember, User, Role], PermissionOverwrite] = UNDEFINED,
        reason: typing.Optional[str] = None,
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
        permission_overwrites: Dict[Union[:class:`GuildMember`, :class:`User`, :class:`Role`], :class:`PermissionOverwrite`]
            The permission overwrites of this channel. This is a dictionary with key being the
            target whose permission overwrite is being edited and value is the new
            permission overwrite.
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

        if parent is not UNDEFINED:
            json["parent_id"] = parent.id if parent is not None else None

        if permission_overwrites is not UNDEFINED:
            json["permission_overwrites"] = self._edit_permission_overwrites_payload(permission_overwrites)

        if json:
            data = await self._rest.edit_channel(
                channel_id=self.id,
                json=json,
                reason=reason
            )
            if data:
                self._update_with_data(data)

    async def fetch_stage_instance(self) -> StageInstance:
        """Fetches the stage instance for this channel.

        Returns
        -------
        :class:`StageInstance`
            The stage instance for this channel.

        Raises
        ------
        HTTPNotFound
            No instance belongs to the channel.
        """
        data = await self._rest.get_stage_instance(channel_id=self.id)
        return StageInstance(data, guild=self.guild)

    async def create_stage_instance(
        self,
        *,
        topic: str,
        privacy_level: int = StagePrivacyLevel.GUILD_ONLY,
        send_start_notification: bool = UNDEFINED,
        reason: typing.Optional[str] = None,
    ) -> StageInstance:
        """Creates a stage instance in this channel.

        This operation requires the bot to be stage moderator, i.e has following
        permissions in the stage channel:

        - :attr:`~Permissions.manage_channels`
        - :attr:`~Permissions.move_members`
        - :attr:`~Permissions.mute_members`

        Additionally, when setting ``send_start_notification`` to ``True``, The
        :attr:`~Permissions.mention_everyone` permission is required.

        Parameters
        ----------
        topic: :class:`builtins.str`
            The topic of stage instance.
        privacy_level: :class:`builtins.int`
            The privacy level of stage instance. See :class:`StagePrivacyLevel` for
            all possible values. Defaults to :attr:`~StagePrivacyLevel.GUILD_ONLY`.
        send_start_notification: :class:`builtins.bool`
            Whether to send start notification to guild members. Defaults to ``False``.
        reason: :class:`builtins.str`
            The reason for doing this action.

        Returns
        -------
        :class:`StageInstance`
            The created stage instance.

        Raises
        ------
        HTTPForbidden
            You are not allowed to do this.
        HTTPException
            The operation failed.
        """
        json: typing.Dict[str, typing.Any] = {
            "channel_id": self.id,
            "topic": topic,
            "privacy_level": privacy_level,
        }

        if send_start_notification is not UNDEFINED:
            json["send_start_notification"] = send_start_notification

        data = await self._rest.create_stage_instance(json=json, reason=reason)
        return StageInstance(data, guild=self.guild)


class PrivateChannel(BaseModel, Comparable, CreationTime):
    """Base class for channel types that are private and not associated to a guild.

    Currently only one channel type is available for private channels that is
    :class:`DMChannel`.

    |supports-comparison|

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

    @property
    def url(self) -> str:
        """The URL for this channel.

        Returns
        -------
        :class:`builtins.str`
        """
        return f"https://discord.com/channels/@me/{self.id}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, type={self.type})"

    async def close(self) -> None:
        """Closes the private channel.

        This should rarely be used. The channel may be reopened using
        relevant methods like :meth:`User.create_dm` for DM channels.
        """
        await self._rest.delete_channel(channel_id=self.id)

class DMChannel(PrivateChannel, BaseMessageChannel):
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

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, recipient={self.recipient})"

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
