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
from qord.flags.permissions import Permissions
from qord._helpers import (
    get_image_data,
    get_optional_snowflake,
    create_cdn_url,
    BASIC_STATIC_EXTS,
    UNDEFINED,
)

import typing

if typing.TYPE_CHECKING:
    from qord.models.guilds import Guild


class Role(BaseModel):
    r"""Representation of a guild's role.

    Attributes
    ----------
    guild: :class:`Guild`
        The guild that this role belongs to.
    id: :class:`builtins.int`
        The snowflake ID of this role.
    name: :class:`builtins.str`
        The name of this role.
    position: :class:`builtins.int`
        The position of this role in the roles hierarchy.

        .. warning::
            Multiple roles in a guild may share same position. This is a
            Discord API limitation. As such, Do not rely on this attribute
            when comparing roles positions, Consider using :meth:`.is_higher_than`
            and :meth:`.is_lower_than` methods instead that efficiently check
            the role positions.

    color: :class:`builtins.int`
        The integer representation of color of this role.
    permissions: :class:`Permissions`
        The permissions of this role.
    hoist: :class:`builtins.bool`
        Whether members with this role are shown separately from
        other online members in the members list.
    managed: :class:`builtins.bool`
        Whether this role is managed by an integration.
    mentionable: :class:`builtins.bool`
        Whether this role is mentionable by other roles.
    icon: Optional[:class:`builtins.str`]
        The icon hash for this role. If role has no icon set, This
        is ``None``
    unicode_emoji: Optional[:class:`builtins.str`]
        The unicode emoji set as icon of this role. ``None`` indicates
        that this role has no unicode emoji set.
    bot_id: Optional[:class:`builtins.int`]
        The ID of bot that this role is for if any. If this role
        is not managed by a bot, then this is ``None``.
    integration_id: Optional[:class:`builtins.int`]
        The ID of integration that this role is for if any. If this role
        is not managed by an integration, then this is ``None``.
    premium_subscriber: :class:`builtins.bool`
        Whether this role is the guild's "Server Booster" role and
        is given to members that boost the guild.
    """
    if typing.TYPE_CHECKING:
        id: int
        name: str
        position: int
        color: int
        hoist: bool
        managed: bool
        mentionable: bool
        icon: typing.Optional[str]
        unicode_emoji: typing.Optional[str]
        bot_id: typing.Optional[int]
        integration_id: typing.Optional[int]
        premium_subscriber: bool

    __slots__ = ("_client", "_rest", "guild", "id", "name", "position", "color", "hoist",
                "managed", "mentionable", "icon", "unicode_emoji", "bot_id",
                "integration_id", "premium_subscriber", "permissions")

    def __init__(self, data: typing.Dict[str, typing.Any], guild: Guild) -> None:
        self.guild = guild
        self._client = guild._client
        self._rest = guild._client._rest
        self._update_with_data(data)

    def _update_with_data(self, data: typing.Dict[str, typing.Any]) -> None:
        self.id = int(data["id"])
        self.name = data["name"]

        self.position = data.get("position", 0)
        self.color = data.get("color", 0)
        self.hoist = data.get("hoist", False)
        self.managed = data.get("managed", False)
        self.mentionable = data.get("mentionable", False)
        self.permissions = Permissions(int(data.get("permissions", 0)))

        self.icon = data.get("icon")
        self.unicode_emoji = data.get("unicode_emoji")
        self._apply_tags(data.get("tags", {}))

    def _apply_tags(self, data: typing.Dict[str, typing.Any]) -> None:
        self.bot_id = get_optional_snowflake(data, "bot_id")
        self.integration_id = get_optional_snowflake(data, "integration_id")

        # If this field is present (always `null`), It indicates `true` and it's
        # absence indicates `false`
        if "premium_subscriber" in data:
            self.premium_subscriber = True
        else:
            self.premium_subscriber = False

    @property
    def mention(self) -> str:
        r"""Returns the string used for mentioning this role in Discord.

        Returns
        -------
        :class:`builtins.str`
        """
        return f"<@&{self.id}>"

    def icon_url(self, extension: str = None, size: int = None) -> typing.Optional[str]:
        r"""Returns the icon URL for this user.

        If role has no icon set, This method would return ``None``.

        The ``extension`` parameter only supports following extensions
        in the case of role icons:

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
        if self.icon is None:
            return None
        if extension is None:
            extension = "png"

        return create_cdn_url(
            f"/role-icons/{self.id}/{self.icon}",
            extension=extension,
            size=size,
            valid_exts=BASIC_STATIC_EXTS,
        )

    def is_bot_managed(self) -> bool:
        r"""Checks whether the role is managed by a bot.

        Bot managed roles don't have the :attr:`.bot_id`
        set to ``None``.

        Returns
        -------
        :class:`builtins.bool`
        """
        return self.bot_id is not None

    def is_integration_managed(self) -> bool:
        r"""Checks whether the role is managed by an integration.

        Integration managed roles don't have the :attr:`.bot_id`
        set to ``None``.

        Returns
        -------
        :class:`builtins.bool`
        """
        return self.integration_id is not None

    def is_default(self) -> bool:
        r"""Checks whether this role is the guild's default
        i.e the "@everyone" role.

        Guild default roles have the same ID as the parent
        guild.

        Returns
        -------
        :class:`builtins.bool`
        """
        return (self.id == self.guild.id)

    def is_higher_than(self, other: Role) -> bool:
        r"""Compares this role with another role of the same guild
        and checks whether this role is higher than the other.

        Parameters
        ----------
        other: :class:`Role`
            The role to check against.

        Raises
        -------
        RuntimeError
            The provided role is not associated to the guild
            that this role is associated to.
        """
        if not isinstance(other, Role):
            raise TypeError("Parameter other must be an instance of Role.")
        if self.guild.id != other.guild.id:
            raise RuntimeError("Cannot compare against role of different guild.")

        if self.position == other.position:
            return self.id > other.id

        return self.position > other.position

    def is_lower_than(self, other: Role) -> bool:
        r"""Compares this role with another role of the same guild
        and checks whether this role is lower than the other.

        Parameters
        ----------
        other: :class:`Role`
            The role to check against.

        Raises
        -------
        RuntimeError
            The provided role is not associated to the guild
            that this role is associated to.
        """
        return (not self.is_higher_than(other))

    async def delete(self, *, reason: str = None) -> None:
        r"""Deletes this role.

        This operation requires the :attr:`~Permissions.manage_roles` permission
        for the client user in the guild.

        Parameters
        ----------
        reason: :class:`builtins.str`
            The reason for performing this operation that shows up on the
            audit log entry.

        Raises
        ------
        HTTPForbidden
            You are missing the :attr:`~Permissions.manage_roles` permissions.
        HTTPException
            The deletion failed failed.
        """
        await self._rest.delete_role(guild_id=self.guild.id, role_id=self.id, reason=reason)

    async def edit(self, *,
        name: str = None,
        permissions: Permissions = None,
        hoist: bool = None,
        mentionable: bool = None,
        icon: typing.Optional[bytes] = UNDEFINED,
        unicode_emoji: typing.Optional[str] = UNDEFINED,
        color: typing.Optional[int] = UNDEFINED,
        reason: str = None,
    ) -> None:
        r"""Edits this role.

        This operation requires the :attr:`~Permissions.manage_roles` permission
        for the client user in the parent guild.

        When the request is successful, This role is updated in place with
        the returned data.

        Parameters
        ----------
        name: :class:`builtins.str`
            The name of this role.
        permissions: :class:`Permissions`
            The permissions for this role.
        color: typing.Optional[:class:`builtins.int`]
            The color value of this role. ``None`` can be used
            to reset the role color to default.
        hoist: :class:`builtins.bool`
            Whether this role should appear hoisted from other roles.
        icon: typing.Optional[:class:`builtins.bytes`]
            The bytes representing the icon of this role. The guild
            must have ``ROLES_ICON`` feature to set this. This parameter
            cannot be mixed with ``unicode_emoji``. ``None`` can be used
            to remove the icon.
        unicode_emoji: typing.Optional[:class:`builtins.str`]
            The unicode emoji used as icon for this role. The guild
            must have ``ROLES_ICON`` feature to set this. This
            parameter cannot be mixed with ``icon``. ``None`` can be used
            to remove the icon.
        mentionable: :class:`builtins.bool`
            Whether this role is mentionable.
        reason: :class:`builtins.str`
            The reason for performing this action that shows up on
            the audit log entry.

        Raises
        ------
        HTTPForbidden
            You are missing the :attr:`~Permissions.manage_roles` permissions.
        HTTPException
            The editing failed.
        """
        json = {}

        if name is not None:
            json["name"] = name
        if permissions is not None:
            json["permissions"] = str(permissions.value)
        if hoist is not None:
            json["hoist"] = hoist
        if mentionable is not None:
            json["mentionable"] = mentionable
        if color is not UNDEFINED:
            json["color"] = 0 if color is None else color # '0' is default.
        if icon is not UNDEFINED:
            json["icon"] = None if icon is None else get_image_data(icon)
        if unicode_emoji is not UNDEFINED:
            json["unicode_emoji"] = unicode_emoji

        if json:
            data = await self._rest.edit_role(
                guild_id=self.guild.id,
                role_id=self.id,
                json=json,
                reason=reason
            )
            self._update_with_data(data)