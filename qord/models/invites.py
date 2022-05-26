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
from qord.models.scheduled_events import ScheduledEvent
from qord.flags.applications import ApplicationFlags
from qord.internal.undefined import UNDEFINED
from qord.internal.helpers import (
    create_cdn_url,
    parse_iso_timestamp,
    BASIC_STATIC_EXTS,
    BASIC_EXTS,
)

import typing

if typing.TYPE_CHECKING:
    from qord.core.client import Client
    from qord.models.guilds import Guild
    from qord.models.channels import GuildChannel
    from datetime import datetime


__all__ = (
    "PartialInviteGuild",
    "PartialInviteChannel",
    "PartialInviteApplication",
    "Invite",
)


class PartialInviteGuild(BaseModel):
    """Represents a guild with a partial data returned in an :class:`Invite`.

    This is given in an :class:`Invite` when the full :class:`Guild` object
    is not resolveable through cache. This is generally the case for invites
    fetched over HTTP API.

    This class holds enough information to fetch the complete guild manually.

    Attributes
    ----------
    id: :class:`builtins.int`
        The ID of guild.
    name: :class:`builtins.str`
        The name of guild.
    banner: Optional[:class:`builtins.str`]
        The banner hash of guild if any.
    splash: Optional[:class:`builtins.str`]
        The splash hash of guild if any.
    icon: Optional[:class:`builtins.str`]
        The icon hash of guild if any.
    description: Optional[:class:`builtins.str`]
        The description of guild if any.
    features: List[:class:`builtins.str`]
        The list of strings representing the features that the
        guild currently has.
    verification_level: :class:`builtins.int`
        The verification level of guild. See :class:`VerificationLevel`
        enumeration for all possible values of this attribute.
    vanity_invite_code: Optional[:class:`builtins.str`]
        The vanity invite code for this guild if any set.
        To get complete URL, see :attr:`.vanity_invite_url`
    nsfw_level: :class:`builtins.int`
        The NSFW level of guild. See :class:`NSFWLevel`
        enumeration for all possible values of this attribute.
    premium_subscription_count: :class:`builtins.int`
        The number of nitro boosts this guild has.
    """
    if typing.TYPE_CHECKING:
        id: int
        name: str
        banner: typing.Optional[str]
        splash: typing.Optional[str]
        icon: typing.Optional[str]
        description: typing.Optional[str]
        features: typing.List[str]
        verification_level: int
        nsfw_level: int
        vanity_invite_code: typing.Optional[str]
        premium_subscription_count: int

    __slots__ = (
        "_client",
        "id",
        "name",
        "banner",
        "splash",
        "icon",
        "description",
        "features",
        "verification_level",
        "nsfw_level",
        "vanity_invite_code",
        "premium_subscription_count"
    )

    def __init__(self, data: typing.Dict[str, typing.Any], client: Client) -> None:
        self._client = client
        self._update_with_data(data)

    def _update_with_data(self, data: typing.Dict[str, typing.Any]) -> None:
        self.id = int(data["id"])
        self.name = data["name"]
        self.banner = data.get("banner")
        self.splash = data.get("splash")
        self.icon = data.get("icon")
        self.description = data.get("description")
        self.features = data.get("features", [])
        self.verification_level = data.get("verification_level", 0)
        self.nsfw_level = data.get("nsfw_level", 0)
        self.vanity_invite_code = data.get("vanity_url_code")
        self.premium_subscription_count = data.get("premium_subscription_count", 0)

    @property
    def vanity_invite_url(self) -> typing.Optional[str]:
        """The vanity invite URL for the guild. If guild has no
        vanity invite set, ``None`` is returned.

        Returns
        -------
        :class:`builtins.str`
        """
        if self.vanity_invite_code is None:
            return None

        return f"https://discord.gg/{self.vanity_invite_code}"

    def is_icon_animated(self) -> bool:
        """Indicates whether the guild has animated icon.

        Having no custom icon set will also return ``False``.

        Returns
        -------
        :class:`builtins.bool`
        """
        if self.icon is None:
            return False

        return self.icon.startswith("a_")

    def icon_url(self, extension: str = UNDEFINED, size: int = UNDEFINED) -> typing.Optional[str]:
        """Returns the icon URL for this guild.

        If guild has no custom icon set, ``None`` is returned.

        The ``extension`` parameter only supports following extensions
        in the case of guild icons:

        - :attr:`ImageExtension.GIF`
        - :attr:`ImageExtension.PNG`
        - :attr:`ImageExtension.JPG`
        - :attr:`ImageExtension.JPEG`
        - :attr:`ImageExtension.WEBP`

        Parameters
        ----------
        extension: :class:`builtins.str`
            The extension to use in the URL. If not supplied, An ideal
            extension will be picked depending on whether guild has static
            or animated icon.
        size: :class:`builtins.int`
            The size to append to URL. Can be any power of 2 between
            64 and 4096.

        Raises
        ------
        ValueError
            Invalid extension or size was passed.
        """
        if self.icon is None:
            return None
        if extension is UNDEFINED:
            extension = "gif" if self.is_icon_animated() else "png"

        return create_cdn_url(
            f"/icons/{self.id}/{self.icon}",
            extension=extension,
            size=size,
            valid_exts=BASIC_EXTS,
        )

    def banner_url(self, extension: str = UNDEFINED, size: int = UNDEFINED) -> typing.Optional[str]:
        """Returns the banner URL for this guild.

        If guild has no custom banner set, ``None`` is returned.

        The ``extension`` parameter only supports following extensions
        in the case of guild banners:

        - :attr:`ImageExtension.PNG`
        - :attr:`ImageExtension.JPG`
        - :attr:`ImageExtension.JPEG`
        - :attr:`ImageExtension.WEBP`

        Parameters
        ----------
        extension: :class:`builtins.str`
            The extension to use in the URL. Defaults to :attr:`~ImageExtension.PNG`.
        size: :class:`builtins.int`
            The size to append to URL. Can be any power of 2 between
            64 and 4096.

        Raises
        ------
        ValueError
            Invalid extension or size was passed.
        """
        if self.banner is None:
            return
        if extension is UNDEFINED:
            extension = "png"

        return create_cdn_url(
            f"/banners/{self.id}/{self.banner}",
            extension=extension,
            size=size,
            valid_exts=BASIC_STATIC_EXTS,
        )

    def splash_url(self, extension: str = UNDEFINED, size: int = UNDEFINED) -> typing.Optional[str]:
        """Returns the splash URL for this guild.

        If guild has no custom splash set, ``None`` is returned.

        The ``extension`` parameter only supports following extensions
        in the case of guild splashes:

        - :attr:`ImageExtension.PNG`
        - :attr:`ImageExtension.JPG`
        - :attr:`ImageExtension.JPEG`
        - :attr:`ImageExtension.WEBP`

        Parameters
        ----------
        extension: :class:`builtins.str`
            The extension to use in the URL. Defaults to :attr:`~ImageExtension.PNG`.
        size: :class:`builtins.int`
            The size to append to URL. Can be any power of 2 between
            64 and 4096.

        Raises
        ------
        ValueError
            Invalid extension or size was passed.
        """
        if self.splash is None:
            return
        if extension is UNDEFINED:
            extension = "png"

        return create_cdn_url(
            f"/splashes/{self.id}/{self.splash}",
            extension=extension,
            size=size,
            valid_exts=BASIC_STATIC_EXTS,
        )


class PartialInviteChannel(BaseModel):
    """Represents a channel with partial data returned in an :class:`Invite`.

    This is given in an :class:`Invite` when the full :class:`GuildChannel`
    object is not resolveable through cache. This is generally the case for
    invites fetched over HTTP API.

    This class holds enough information to fetch the complete channel manually.

    Attributes
    ----------
    id: :class:`builtins.int`
        The ID of channel.
    name: :class:`builtins.str`
        The name of channel.
    type: :class:`builtins.int`
        The type of channel.
    """
    if typing.TYPE_CHECKING:
        id: int
        name: str
        type: int

    __slots__ = (
        "_client",
        "id",
        "name",
        "type",
    )

    def __init__(self, data: typing.Dict[str, typing.Any], client: Client) -> None:
        self._client = client
        self._update_with_data(data)

    def _update_with_data(self, data: typing.Dict[str, typing.Any]) -> None:
        self.id = int(data["id"])
        self.name = data["name"]
        self.type = data["type"]


class PartialInviteApplication(BaseModel):
    """Represents an application with partial data returned in an :class:`Invite`.

    This class mainly represents an embedded application from an invite.

    Attributes
    ----------
    id: :class:`builtins.str`
        The snowflake ID of application
    name: :class:`builtins.str`
        The name of application.
    icon: Optional[:class:`builtins.str`]
        The icon of application.
    flags: :class:`ApplicationFlags`
        The flags of this application.
    description: Optional[:class:`builtins.str`]
        The description of application.
    rpc_origins: List[:class:`builtins.str`]
        A list of RPC origin URLs for the application.
    verify_key: :class:`builtins.str`
        The hex encoded key used by application for verification in interactions
        and the GameSDKs.
    terms_of_service_url: Optional[:class:`builtins.str`]
        The application's terms of service URL, if any.
    privacy_policy_url: Optional[:class:`builtins.str`]
        The application's privacy policy URL, if any.
    """
    if typing.TYPE_CHECKING:
        id: int
        name: str
        icon: typing.Optional[str]
        flags: ApplicationFlags
        description: typing.Optional[str]
        rpc_origins: typing.List[str]
        verify_key: typing.Optional[str]
        terms_of_service_url: typing.Optional[str]
        privacy_policy_url: typing.Optional[str]

    __slots__ = (
        "_client",
        "id",
        "name",
        "icon",
        "flags",
        "description",
        "rpc_origins",
        "verify_key",
        "terms_of_service_url",
        "privacy_policy_url",
    )

    def __init__(self, data: typing.Dict[str, typing.Any], client: Client) -> None:
        self._client = client
        self._update_with_data(data)

    def _update_with_data(self, data: typing.Dict[str, typing.Any]) -> None:
        self.id = int(data["id"])
        self.name = data["name"]
        self.icon = data.get("icon")
        self.flags = ApplicationFlags(data.get("flags", 0))
        self.description = data.get("description")
        self.rpc_origins = data.get("rpc_origins", [])
        self.verify_key = data.get("verify_key")
        self.terms_of_service_url = data.get("terms_of_service_url")
        self.privacy_policy_url = data.get("privacy_policy_url")

    def icon_url(self, extension: str = UNDEFINED, size: int = UNDEFINED) -> typing.Optional[str]:
        """Returns the icon's URL for this application.

        If application has no icon set, This method would return ``None``.

        The ``extension`` parameter only supports following extensions
        in the case of application icons:

        - :attr:`ImageExtension.PNG`
        - :attr:`ImageExtension.JPG`
        - :attr:`ImageExtension.JPEG`
        - :attr:`ImageExtension.WEBP`

        Parameters
        ----------
        extension: :class:`builtins.str`
            The extension to use in the URL. If not supplied, Defaults
            to :attr:`~ImageExtension.PNG`.
        size: :class:`builtins.int`
            The size to append to URL. Can be any power of 2 between
            64 and 4096.

        Raises
        ------
        ValueError
            Invalid extension or size was passed.
        """
        icon = self.icon

        if icon is None:
            return None

        if extension is UNDEFINED:
            extension = "png"

        return create_cdn_url(
            f"/app-icons/{self.id}/{icon}",
            extension=extension,
            size=size,
            valid_exts=BASIC_STATIC_EXTS,
        )


class Invite(BaseModel):
    r"""Represents an invite.

    Some attibutes of this class are only available in some special
    cases. Other than those cases, the value of such attributes is None.

    The attributes that show this behaviour are:

    - :attr:`.approximate_member_count`
    - :attr:`.approximate_presence_count`
    - :attr:`.expires_at`
    - :attr:`.uses`
    - :attr:`.max_uses`
    - :attr:`.max_age`
    - :attr:`.temporary`
    - :attr:`.created_at`

    See the documentation of these attributes for more information on when
    they are present.

    Attributes
    ----------
    code: :class:`builtins.str`
        The unique code of this invite.
    target_type: Optional[:class:`builtins.int`]
        The type of target that this invite points to. If the invite
        does not point to a specific target, then this is ``None``.
        See :class:`InviteTargetType` for all possible values.
    approximate_member_count: Optional[:class:`builtins.int`]
        The approximate members count of guild that the invite belongs to.
        Only available when invite is retrieved through :meth:`Client.fetch_invite`
        with ``with_counts`` parameter set to ``True``.
    approximate_presence_count: Optional[:class:`builtins.int`]
        The approximate online members count of guild that the invite belongs to.
        Only available when invite is retrieved through :meth:`Client.fetch_invite`
        with ``with_counts`` parameter set to ``True``.
    expires_at: Optional[:class:`datetime.datetime`]
        The time when the invite expires.
        Only available when invite is retrieved through :meth:`Client.fetch_invite`
        with ``with_expiration`` parameter set to ``True``.
    inviter: Optional[:class:`User`]
        The user who created the invite.
    target_user: Optional[:class:`User`]
        The target user that the invite points to. This is only available when
        invite is pointing to a stream in a voice channel.
    target_application: Optional[:class:`PartialInviteApplication`]
        The target embedded application that the invite points to. This is only
        available when invite is pointing to an embedded application in a voice channel.
    uses: Optional[:class:`builtins.int`]
        The number of time this invite has been used.
        This attribute is only available in :attr:`~GatewayEvent.INVITE_CREATE` event
        or when invite is fetched through :meth:`Guild.fetch_invites` or :meth:`GuildChannel.fetch_invites`.
    max_uses: Optional[:class:`builtins.int`]
        The number of time this invite can been used. The value of 0 indicates unlimited uses.
        This attribute is only available in :attr:`~GatewayEvent.INVITE_CREATE` event
        or when invite is fetched through :meth:`Guild.fetch_invites` or :meth:`GuildChannel.fetch_invites`.
    max_age: Optional[:class:`builtins.int`]
        Duration in seconds after which the invite expires. The value of 0 indicates unlimited age.
        This attribute is only available in :attr:`~GatewayEvent.INVITE_CREATE` event
        or when invite is fetched through :meth:`Guild.fetch_invites` or :meth:`GuildChannel.fetch_invites`.
    temporary: Optional[:class:`builtins.bool`]
        Whether the invite grants temporary membership.
        This attribute is only available in :attr:`~GatewayEvent.INVITE_CREATE` event
        or when invite is fetched through :meth:`Guild.fetch_invites` or :meth:`GuildChannel.fetch_invites`.
    created_at: Optional[:class:`datetime.datetime`]
        The time when the invite was created.
        This attribute is only available in :attr:`~GatewayEvent.INVITE_CREATE` event
        or when invite is fetched through :meth:`Guild.fetch_invites` or :meth:`GuildChannel.fetch_invites`.
    scheduled_event: Optional[:class:`ScheduledEvent`]
        The scheduled event attached to this invite. Only present when ``scheduled_event_id``
        is given in :meth:`Client.fetch_invite`.
    """

    if typing.TYPE_CHECKING:
        code: str
        target_type: typing.Optional[int]
        approximate_member_count: typing.Optional[int]
        approximate_presence_count: typing.Optional[int]
        uses: typing.Optional[int]
        max_uses: typing.Optional[int]
        max_age: typing.Optional[int]
        temporary: typing.Optional[bool]
        created_at: typing.Optional[datetime]
        expires_at: typing.Optional[datetime]
        inviter: typing.Optional[User]
        target_user: typing.Optional[User]
        target_application: typing.Optional[PartialInviteApplication]
        guild: typing.Optional[typing.Union[Guild, PartialInviteGuild]]
        channel: typing.Union[GuildChannel, PartialInviteChannel]
        scheduled_event: typing.Optional[ScheduledEvent]

    __slots__ = (
        "_client",
        "_cache",
        "code",
        "target_type",
        "approximate_presence_count",
        "approximate_member_count",
        "expires_at",
        "inviter",
        "target_user",
        "target_application",
        "uses",
        "max_uses",
        "max_age",
        "temporary",
        "created_at",
        "guild",
        "channel",
        "scheduled_event",
    )

    def __init__(
        self,
        data: typing.Dict[str, typing.Any],
        client: Client,
        guild: Guild = UNDEFINED,
        channel: GuildChannel = UNDEFINED,
    ) -> None:
        self._client = client
        self._cache = client._cache
        self.guild = guild
        self.channel = channel
        self._update_with_data(data)

    def _update_with_data(self, data: typing.Dict[str, typing.Any]) -> None:
        self.code = data["code"]
        self.target_type = data.get("target_type")
        self.approximate_presence_count = data.get("approximate_presence_count")
        self.approximate_member_count = data.get("approximate_member_count")
        self.uses = data.get("uses")
        self.max_uses = data.get("uses")
        self.max_age = data.get("max_age")
        self.temporary = data.get("temporary")

        expires_at = data.get("expires_at")
        created_at = data.get("created_at")
        inviter = data.get("inviter")
        target_user = data.get("target_user")
        target_application = data.get("target_application")

        self.expires_at = parse_iso_timestamp(expires_at) if expires_at else None
        self.created_at = parse_iso_timestamp(created_at) if created_at else None
        self.inviter = User(inviter, client=self._client) if inviter else None
        self.target_user = User(target_user, client=self._client) if target_user else None
        self.target_application = PartialInviteApplication(target_application, client=self._client) if target_application else None

        if self.guild is UNDEFINED:
            guild_data = data.get("guild")
            if guild_data:
                self.guild = PartialInviteGuild(guild_data, client=self._client)
            else:
                self.guild = None

        if self.channel is UNDEFINED:
            self.channel = PartialInviteChannel(data["channel"], client=self._client)

        self.scheduled_event = None

        event = data.get("guild_scheduled_event")
        if event:
            from qord.models.guilds import Guild  # Circular import
            guild = self.guild
            if guild and isinstance(guild, Guild):
                self.scheduled_event = ScheduledEvent(event, guild=guild, client=self._client)
            else:
                self.scheduled_event = ScheduledEvent(event, client=self._client)

    def __repr__(self) -> str:
        return f"<Invite code={self.code}>"

    @property
    def url(self) -> str:
        """The URL of this invite.

        Returns
        -------
        :class:`builtins.str`
        """
        ret = f"https://discord.gg/{self.code}"
        event = self.scheduled_event
        if event is not None:
            return ret + f"?event={event.id}"
        return ret

    async def delete(self) -> None:
        """Deletes or revokes the invite.

        This requires :attr:`~Permissions.manage_channels` in the invite's
        channel or :attr:`~Permissions.manage_guilds` permission to delete
        any invite across the guild.

        Raises
        ------
        HTTPForbidden
            You are not allowed to do this.
        HTTPException
            The action failed.
        """
        await self._client._rest.delete_invite(invite_code=self.code)
