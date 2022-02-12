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
from qord.flags.system_channel import SystemChannelFlags
from qord._helpers import get_optional_snowflake, create_cdn_url, compute_shard_id

from datetime import datetime
import typing

if typing.TYPE_CHECKING:
    from qord.core.shard import Shard
    from qord.core.client import Client

class Guild(BaseModel):
    r"""Representation of a Discord guild entity often referred as "Server" in the UI.

    Attributes
    ----------
    id: :class:`builtins.int`
        The snowflake ID of this guild.
    name: :class:`builtins.str`
        The name of this guild.
    afk_timeout: :class:`builtins.int`
        The AFK timeout after which AFK members are moved to designated AFK
        voice channel. ``0`` means no timeout.
    premium_subscription_count: :class:`builtins.int`
        The number of nitro boosts this guild has.
    preferred_locale: :class:`builtins.str`
        The chosen language for this guild.
    widget_enabled: :class:`builtins.bool`
        Whether guild has widget enabled.
    large: :class:`builtins.bool`
        Whether guild is marked as large.
    unavailable: :class:`builtins.bool`
        Whether guild is unavailable due to an outage, This is almost never ``True``.
    premium_progress_bar_enabled: :class:`builtins.bool`
        Whether guild has premium progress bar or server boosts progress
        bar enabled.
    features: :class:`builtins.str`
        The list of string representations of features of this guild. Complete
        list of valid features with meanings can be found here:

        https://discord.com/developers/docs/resources/guild#guild-object-guild-features
    system_channel_flags: :class:`SystemChannelFlags`
        The system channel flags for this guild.
    member_count: typing.Optional[:class:`builtins.int`]
        The member count of this guild.
    max_presences: typing.Optional[:class:`builtins.int`]
        The maximum number of presences for this guild, This is generally ``None``
        except for guilds marked as large.
    max_members: typing.Optional[:class:`builtins.int`]
        The maximum number of members for this guild.
    max_video_channel_users: typing.Optional[:class:`builtins.int`]
        The maximum number of video channel users for this guild.
    approximate_member_count: typing.Optional[:class:`builtins.int`]
        The approximated member count for this guild.
    approximate_presence_count: typing.Optional[:class:`builtins.int`]
        The approximated presences count for this guild.
    vanity_invite_code: typing.Optional[:class:`builtins.str`]
        The vanity invite code for this guild. To get complete URL, see
        :attr:`.vanity_invite_url`
    description: typing.Optional[:class:`builtins.str`]
        The description of this guild, if any.
    joined_at: typing.Optional[:class:`datetime.datetime`]
        The datetime representation of time when the bot had joined this guild.
    icon: typing.Optional[:class:`builtins.str`]
        The icon hash of this guild. If guild has no icon set, This is ``None``.
        See :meth:`.icon_url` to retrieve the URL to this.
    banner: typing.Optional[:class:`builtins.str`]
        The banner hash of this guild. If guild has no banner set, This is ``None``.
        See :meth:`.banner_url` to retrieve the URL to this.
    splash: typing.Optional[:class:`builtins.str`]
        The splash hash of this guild. If guild has no splash set, This is ``None``.
        See :meth:`.splash_url` to retrieve the URL to this.
    discovery_splash: typing.Optional[:class:`builtins.str`]
        The discovery splash hash of this guild. If guild has no discovery splash set,
        This is ``None``. See :meth:`.discovery_splash_url` to retrieve the URL to this.
    owner_id: typing.Optional[:class:`builtins.int`]
        The ID of owner of this guild.
    afk_channel_id: typing.Optional[:class:`builtins.int`]
        The ID of designated AFK voice channel of this guild or ``None`` if no
        channel is set.
    widget_channel_id: typing.Optional[:class:`builtins.int`]
        The ID of channel designated to be shown on guild's widget or ``None`` if no
        channel is set.
    application_id: typing.Optional[:class:`builtins.int`]
        The ID of application or bot that created this guild or ``None`` if guild is not
        created by an application or bot.
    system_channel_id: typing.Optional[:class:`builtins.int`]
        The ID of channel designated for the system messages or ``None`` if no
        channel is set.
    rules_channel_id: typing.Optional[:class:`builtins.int`]
        The ID of channel marked as rules channel in community guilds or ``None`` if no
        channel is set.
    public_updates_channel_id: typing.Optional[:class:`builtins.int`]
        The ID of channel designated for moderator updates community guilds or
        ``None`` if no channel is set.
    verification_level: :class:`builtins.int`
        The verification level value of this guild. See :class:`VerificationLevel`
        for more information about this.
    notification_level: :class:`builtins.int`
        The message notification level value of this guild. See :class:`NotificationLevel`
        for more information about this.
    explicit_content_filter: :class:`builtins.int`
        The explicit content filter level value of this guild. See :class:`ExplicitContentFilter`
        for more information about this.
    mfa_level: :class:`builtins.int`
        The 2FA requirement value of this guild. See :class:`MFALevel` for more information
        about this.
    premium_tier: :class:`builtins.int`
        The premium tier or server boosts level value of this guild. See
        :class:`PremiumTier` for more information about this.
    nsfw_level: :class:`builtins.int`
        The NSFW level value of this guild.  See :class:`NSFWLevel` for more information
        about this.
    """
    if typing.TYPE_CHECKING:
        # These are here to avoid cluttering in main code.
        id: int
        name: str
        afk_timeout: int
        premium_subscription_count: int
        preferred_locale: str
        widget_enabled: bool
        large: bool
        unavailable: bool
        premium_progress_bar_enabled: bool
        features: typing.List[str]
        system_channel_flags: SystemChannelFlags
        verification_level: int
        nsfw_level: int
        explicit_content_filter: int
        mfa_level: int
        notification_level: int
        premium_tier: int
        member_count: typing.Optional[int]
        max_presences: typing.Optional[int]
        max_members: typing.Optional[int]
        max_video_channel_users: typing.Optional[int]
        approximate_member_count: typing.Optional[int]
        approximate_presence_count: typing.Optional[int]
        vanity_invite_code: typing.Optional[str]
        description: typing.Optional[str]
        joined_at: typing.Optional[datetime]
        icon: typing.Optional[str]
        splash: typing.Optional[str]
        discovery_splash: typing.Optional[str]
        banner: typing.Optional[str]
        owner_id: typing.Optional[int]
        afk_channel_id: typing.Optional[int]
        application_id: typing.Optional[int]
        public_updates_channel_id: typing.Optional[int]
        rules_channel_id: typing.Optional[int]
        widget_channel_id: typing.Optional[int]
        system_channel_id: typing.Optional[int]

    __slots__ = ("_client", "_rest", "id", "name", "afk_timeout", "premium_subscription_count",
                "preferred_locale", "widget_enabled", "large", "unavailable", "system_channel_flags",
                "premium_progress_bar_enabled", "features", "verification_level", "notification_level",
                "mfa_level", "premium_tier", "nsfw_level", "member_count", "max_presences", "max_members",
                "max_video_channel_users", "approximate_member_count", "approximate_presence_count",
                "vanity_invite_code", "description", "joined_at", "icon", "splash", "discovery_splash",
                "banner", "owner_id", "afk_channel_id", "widget_channel_id", "application_id", "system_channel_id",
                "rules_channel_id", "public_updates_channel_id", "explicit_content_filter",)

    def __init__(self, data: typing.Dict[str, typing.Any], client: Client) -> None:
        self._client = client
        self._rest = client._rest
        self._update_with_data(data)

    def _update_with_data(self, data: typing.Dict[str, typing.Any]) -> None:
        # I'm documenting these attributes here for future reference when we
        # eventually implement these features.
        #
        # - permissions
        # - roles
        # - emojis
        # - voice_states
        # - members
        # - channels
        # - threads
        # - presences
        # - welcome_screen
        # - stage_instances
        # - stickers
        # - guild_scheduled_events

        # General / non-optional attributes
        self.id = int(data["id"])
        self.name = data["name"]
        self.afk_timeout = data.get("afk_timeout", 0)
        self.premium_subscription_count = data.get("premium_subscription_count", 0)
        self.preferred_locale = data.get("preferred_locale", "en-US")
        self.widget_enabled = data.get("widget_enabled", False)
        self.large = data.get("large", False)
        self.unavailable = data.get("unavailable", False)
        self.premium_progress_bar_enabled = data.get("premium_progress_bar_enabled", False)
        self.features = data.get("features", [])
        self.system_channel_flags = SystemChannelFlags(data.get("system_channel_flags", 0))

        # Enums
        self.verification_level = data.get("verification_level", 0)
        self.notification_level = data.get("default_message_notifications", 0)
        self.explicit_content_filter = data.get("explicit_content_filter", 0)
        self.mfa_level = data.get("mfa_level", 0)
        self.premium_tier = data.get("premium_tier", 0)
        self.nsfw_level = data.get("nsfw_level", 0)

        # Nullable attributes
        self.member_count = data.get("member_count")
        self.max_presences = data.get("max_presences")
        self.max_members = data.get("max_presences")
        self.max_video_channel_users = data.get("max_video_channel_users")
        self.approximate_member_count = data.get("approximate_member_count")
        self.approximate_presence_count = data.get("approximate_presence_count")
        self.vanity_invite_code = data.get("vanity_url_code")
        self.description = data.get("description")
        joined_at = data.get("joined_at")
        self.joined_at = datetime.fromisoformat(joined_at) if joined_at is not None else None

        # CDN resources
        self.icon = data.get("icon") or data.get("icon_hash")
        self.splash = data.get("splash")
        self.discovery_splash = data.get("discovery_splash")
        self.banner = data.get("banner")

        # Snowflakes
        self.owner_id = get_optional_snowflake(data, "owner_id")
        self.afk_channel_id = get_optional_snowflake(data, "afk_channel_id")
        self.widget_channel_id = get_optional_snowflake(data, "widget_channel_id")
        self.application_id = get_optional_snowflake(data, "application_id")
        self.system_channel_id = get_optional_snowflake(data, "system_channel_id")
        self.rules_channel_id = get_optional_snowflake(data, "rules_channel_id")
        self.public_updates_channel_id = get_optional_snowflake(data, "public_updates_channel_id")

    @property
    def vanity_invite_url(self) -> typing.Optional[str]:
        r"""The vanity invite URL for the guild. If guild has no
        vanity invite set, ``None`` is returned.

        Returns
        -------
        :class:`builtins.str`
        """
        if self.vanity_invite_code is None:
            return None

        return f"https://discord.gg/{self.vanity_invite_code}"

    @property
    def shard_id(self) -> int:
        r"""The *computed* shard ID for this guild.

        Note that the value returned by this property is just computed
        using the guild ID and total shards count of the bound client and
        the actual shard with that ID may not exist in the client's cache.
        This is usually the case for guilds that are not cached by the client.

        Returns
        -------
        :class:`int`
        """
        shards_count = self._client.shards_count
        assert shards_count is not None, "No shards count is available yet."
        return compute_shard_id(guild_id=self.id, shards_count=shards_count)

    @property
    def shard(self) -> typing.Optional[Shard]:
        r"""The shard associated to this guild.

        This can be ``None`` in some cases, See :attr:`.shard_id` documentation
        for more information. This is equivalent to calling :meth:`Client.get_shard`
        using the :attr:`.shard_id`.

        Returns
        -------
        Optional[:class:`Shard`]
        """
        return self._client.get_shard(self.shard_id)

    def icon_url(self, extension: str = None, size: int = None) -> typing.Optional[str]:
        r"""Returns the icon URL for this guild.

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

        extension = "gif" if self.is_icon_animated() else "png"
        return create_cdn_url(f"/icons/{self.id}/{self.icon}", extension=extension, size=size)

    def banner_url(self, extension: str = None, size: int = None) -> typing.Optional[str]:
        r"""Returns the banner URL for this guild.

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

        return create_cdn_url(
            f"/banners/{self.id}/{self.banner}",
            extension=extension or "png",
            size=size,
            valid_exts=["jpg", "jpeg", "png", "webp"] # Doesn't support GIF.
        )

    def splash_url(self, extension: str = None, size: int = None) -> typing.Optional[str]:
        r"""Returns the splash URL for this guild.

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

        return create_cdn_url(
            f"/splashes/{self.id}/{self.splash}",
            extension=extension or "png",
            size=size,
            valid_exts=["jpg", "jpeg", "png", "webp"] # Doesn't support GIF.
        )

    def discovery_splash_url(self, extension: str = None, size: int = None) -> typing.Optional[str]:
        r"""Returns the discovery splash URL for this guild.

        If guild has no custom discovery splash set, ``None`` is returned.

        The ``extension`` parameter only supports following extensions
        in the case of guild discovery splashes:

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
        if self.discovery_splash is None:
            return

        return create_cdn_url(
            f"/splashes/{self.id}/{self.discovery_splash}",
            extension=extension or "png",
            size=size,
            valid_exts=["jpg", "jpeg", "png", "webp"] # Doesn't support GIF.
        )

    def is_icon_animated(self) -> bool:
        r"""Indicates whether the guild has animated icon.

        Having no custom icon set will also return ``False``.

        Returns
        -------
        :class:`builtins.bool`
        """
        if self.icon is None:
            return False

        return self.icon.startswith("a_")

    # API calls

    async def leave(self) -> None:
        r"""Leaves the guild.

        Raises
        ------
        HTTPNotFound
            The bot is already not part of this guild.
        HTTPException
            HTTP request failed.
        """
        await self._rest.leave_guild(guild_id=self.id)
