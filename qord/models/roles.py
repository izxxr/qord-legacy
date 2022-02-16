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
from qord._helpers import get_optional_snowflake, create_cdn_url, BASIC_STATIC_EXTS

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
        The position of this role.
    color: :class:`builtins.int`
        The integer representation of color of this role.
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
    __slots__ = ("_client", "guild", "id", "name", "position", "color", "hoist",
                "managed", "mentionable", "icon", "unicode_emoji", "bot_id",
                "integration_id", "premium_subscriber")

    def __init__(self, data: typing.Dict[str, typing.Any], guild: Guild) -> None:
        self.guild = guild
        self._client = guild._client
        self._update_with_data(data)

    def _update_with_data(self, data: typing.Dict[str, typing.Any]) -> None:
        # TODO: permissions
        self.id = int(data["id"])
        self.name = data["name"]

        self.position = data.get("position", 0)
        self.color = data.get("color", 0)
        self.hoist = data.get("hoist", False)
        self.managed = data.get("managed", False)
        self.mentionable = data.get("mentionable", False)

        self.icon = data.get("icon")
        self.unicode_emoji = data.get("unicode_emoji")
        self._apply_tags(data.get("tags", {}))

    def _apply_tags(self, data: typing.Dict[str, typing.Any]) -> None:
        self.bot_id = get_optional_snowflake(data, "bot_id")
        self.integration_id = get_optional_snowflake(data, "integration_id")

        # If this field is present (always `null`), It indicates `true` and it's
        # absence indicates `false`
        # No idea about this behaviour.
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