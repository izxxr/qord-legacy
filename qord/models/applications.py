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
from qord.flags.applications import ApplicationFlags
from qord.flags.permissions import Permissions
from qord.internal.helpers import get_optional_snowflake, create_cdn_url, BASIC_STATIC_EXTS
from qord.internal.mixins import Comparable, CreationTime
from qord.internal.undefined import UNDEFINED

import typing

if typing.TYPE_CHECKING:
    from qord.core.client import Client
    from qord.models.guilds import Guild


__all__ = (
    "ApplicationInstallParams",
    "Application",
    "Team",
    "TeamMember",
)


class ApplicationInstallParams(BaseModel):
    """Represents installation parameters of a Discord :class:`Application`.

    Attributes
    ----------
    scopes: List[:class:`builtins.str`]
        The list of `OAuth2 scopes <https://discord.com/developers/docs/topics/oauth2#shared-resources-oauth2-scopes>`_
        to allow on application during installation.
    permissions: :class:`Permissions`
        The permissions that are given to application.
    """
    if typing.TYPE_CHECKING:
        scopes: typing.List[str]
        permissions: Permissions

    def __init__(self, data: typing.Dict[str, typing.Any], client: Client) -> None:
        self._client = client
        self._update_with_data(data)

    def _update_with_data(self, data: typing.Dict[str, typing.Any]) -> None:
        self.scopes = data.get("scopes", [])
        self.permissions = Permissions(int(data.get("permissions", 0)))


class TeamMember(BaseModel):
    """Represents the member of a :class:`Team`.

    Attributes
    ----------
    membership_state: :class:`builtins.int`
        The membership state of this team member. See :class:`TeamMembershipState` enum
        for all possible values.
    team: :class:`Team`
        The team that the member belongs to.
    user: :class:`User`
        The user belonging to this member. Note that this user object only includes the
        following valid attributes:

        - :attr:`User.id`
        - :attr:`User.name`
        - :attr:`User.discriminator`
        - :attr:`User.avatar`

        Other attributes may have the value of ``None`` regardless of whether the user
        has that feature or not.
    """
    if typing.TYPE_CHECKING:
        team: Team
        membership_state: int
        user: User

    __slots__ = (
        "_client",
        "team",
        "membership_state",
        "user",
    )

    def __init__(self, data: typing.Dict[str, typing.Any], team: Team) -> None:
        self.team = team
        self._client = team._client
        self._update_with_data(data)

    def _update_with_data(self, data: typing.Dict[str, typing.Any]) -> None:
        self.membership_state = data["membership_state"]
        self.user = User(data["user"], client=self._client)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(membership_state={self.membership_state}, user={self.user}, team={self.team})"


class Team(BaseModel, CreationTime, Comparable):
    """Represents a team.

    A team is a group of users sharing access to one or more applications.
    This class is generally obtained by :attr:`Application.team` attribute.

    Attributes
    ----------
    id: :class:`builtins.int`
        The snowflake ID of team.
    name: :class:`builtins.str`
        The name of team.
    icon: Optional[:class:`builtins.str`]
        The icon's hash for this team if any.
    owner_id: :class:`builtins.int`
        The ID of user who owns the team.
    members: List[:class:`TeamMember`]
        The list of team members that are part of this team.
    """
    if typing.TYPE_CHECKING:
        id: int
        name: str
        owner_id: int
        members: typing.List[TeamMember]
        icon: typing.Optional[str]

    __slots__ = (
        "_client",
        "id",
        "name",
        "owner_id",
        "members",
        "icon",
    )

    def __init__(self, data: typing.Dict[str, typing.Any], client: Client) -> None:
        self._client = client
        self._update_with_data(data)

    def _update_with_data(self, data: typing.Dict[str, typing.Any]) -> None:
        self.id = int(data["id"])
        self.name = data["name"]
        self.owner_id = int(data["owner_user_id"])
        self.members = [TeamMember(tm, team=self) for tm in data.get("members", [])]
        self.icon = data.get("icon")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, name={self.name!r}, icon={self.icon!r})"

    @property
    def owner(self) -> TeamMember:  # type: ignore # See below
        """The :class:`TeamMember` representing the owner of team."""
        # The members array is always guaranteed to include at
        # least the owner of the team. Unless Discord decides to
        # send improper data, this property should never be returning None.
        owner_id = self.owner_id
        for member in self.members:
            if member.user.id == owner_id:
                return member

    def icon_url(self, extension: str = UNDEFINED, size: int = UNDEFINED) -> typing.Optional[str]:
        """Returns the icon's URL for this team.

        If team has no icon set, This method would return ``None``.

        The ``extension`` parameter only supports following extensions
        in the case of team icons:

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
            f"/team-icons/{self.id}/{icon}",
            extension=extension,
            size=size,
            valid_exts=BASIC_STATIC_EXTS,
        )


class Application(BaseModel, CreationTime, Comparable):
    """Represents an application on Discord.

    |supports-comparison|

    Attributes
    ----------
    id: :class:`builtins.int`
        The snowflake ID of this application.
    name: :class:`builtins.str`
        The name of application.
    icon: Optional[:class:`builtins.str`]
        The icon's hash for this application if any.
    description: Optional[:class:`builtins.str`]
        The description of this application if any.
    terms_of_service_url: Optional[:class:`builtins.str`]
        The link for ToS of this application if any.
    privacy_policy_url: Optional[:class:`builtins.str`]
        The link for privacy policy of this application if any.
    verify_key: Optional[:class:`builtins.str`]
        The hex encoded key used by application for verification in interactions
        and the GameSDKs.
    slug: Optional[:class:`builtins.str`]
        If application is a game sold on Discord, the slug of application.
    cover_image: Optional[:class:`builtins.str`]
        The hash for default rich presence cover image for application if any.
    custom_install_url: Optional[:class:`builtins.str`]
        The custom authorization link used for installing or adding the application
        if any set.
    guild_id: Optional[:class:`builtins.int`]
        The ID of guild that the game is being sold in if any.
    primary_sku_id: Optional[:class:`builtins.int`]
        The primary SKU ID for this application if any.
    tags: List[:class:`builtins.str`]
        The list of tags describing the application.
    rpc_origins: List[:class:`builtins.str`]
        The list of RPC origin URLs, if RPC is enabled.
    bot_public: :class:`builtins.bool`
        Whether the application's related bot is available to add publicly.
    bot_require_code_grant: :class:`builtins.bool`
        Whether the application's related bot requires complete code grant OAuth2 flow
        in order to get added to a guild.
    flags: :class:`ApplicationFlags`
        The public flags of the application.
    owner: Optional[:class:`User`]
        The owner of this application. Note that this user object only includes the
        following valid attributes:

        - :attr:`User.id`
        - :attr:`User.name`
        - :attr:`User.discriminator`
        - :attr:`User.avatar`

        Other attributes may have the value of ``None`` regardless of whether the user
        has that feature or not.
    """

    if typing.TYPE_CHECKING:
        id: int
        name: str
        flags: ApplicationFlags
        owner: typing.Optional[User]
        team: typing.Optional[Team]
        icon: typing.Optional[str]
        description: typing.Optional[str]
        terms_of_service_url: typing.Optional[str]
        privacy_policy_url: typing.Optional[str]
        verify_key: typing.Optional[str]
        slug: typing.Optional[str]
        cover_image: typing.Optional[str]
        custom_install_url: typing.Optional[str]
        guild_id: typing.Optional[int]
        primary_sku_id: typing.Optional[int]
        tags: typing.List[str]
        rpc_origins: typing.List[str]
        bot_public: bool
        bot_require_code_grant: bool

    __slots__ = (
        "_client",
        "id",
        "name",
        "icon",
        "description",
        "rpc_origins",
        "bot_public",
        "bot_require_code_grant",
        "terms_of_service_url",
        "privacy_policy_url",
        "verify_key",
        "slug",
        "guild_id",
        "primary_sku_id",
        "cover_image",
        "tags",
        "custom_install_url",
        "flags",
        "owner",
        "install_params",
        "team",
    )

    def __init__(self, data: typing.Dict[str, typing.Any], client: Client) -> None:
        self._client = client
        self._update_with_data(data)

    def _update_with_data(self, data: typing.Dict[str, typing.Any]) -> None:
        self.id = int(data["id"])
        self.name = data["name"]
        self.icon = data.get("icon")
        self.description = data.get("description")
        self.rpc_origins = data.get("rpc_origins", [])
        self.bot_public = data.get("bot_public", False)
        self.bot_require_code_grant = data.get("bot_require_code_grant", False)
        self.terms_of_service_url = data.get("terms_of_service_url")
        self.privacy_policy_url = data.get("privacy_policy_url")
        self.verify_key = data.get("verify_key")
        self.slug = data.get("slug")
        self.guild_id = get_optional_snowflake(data, "guild_id")
        self.primary_sku_id = get_optional_snowflake(data, "primary_sku_id")
        self.cover_image = data.get("cover_image")
        self.tags = data.get("tags", [])
        self.custom_install_url = data.get("custom_install_url")
        self.flags = ApplicationFlags(data.get("flags", 0))

        owner = data.get("owner")
        install_params = data.get("install_params")
        team = data.get("team")
        self.owner = User(owner, client=self._client) if owner is not None else None
        self.install_params = ApplicationInstallParams(install_params, client=self._client) if install_params is not None else None
        self.team = Team(team, client=self._client) if team is not None else None

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, name={self.name}, icon={self.icon})"

    @property
    def guild(self) -> typing.Optional[Guild]:
        """The guild that the application is selling games in.

        This may be ``None`` if the guild is not cached by the
        client. Consider fetching the guild instead in case
        this attribute is ``None`` and :attr:`.guild_id` is
        a valid guild ID.

        Returns
        -------
        Optional[:class:`Guild`]
        """
        guild_id = self.guild_id
        if guild_id is None:
            return
        return self._client.cache.get_guild(guild_id)

    def cover_image_url(self, extension: str = UNDEFINED, size: int = UNDEFINED) -> typing.Optional[str]:
        """Returns the cover image's URL for this application.

        If application has no cover image set, This method would return ``None``.

        The ``extension`` parameter only supports following extensions
        in the case of application cover images:

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
        cover_image = self.cover_image

        if cover_image is None:
            return None

        if extension is UNDEFINED:
            extension = "png"

        return create_cdn_url(
            f"/app-icons/{self.id}/{cover_image}",
            extension=extension,
            size=size,
            valid_exts=BASIC_STATIC_EXTS,
        )

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
