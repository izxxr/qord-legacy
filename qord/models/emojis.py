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
from qord.internal.undefined import UNDEFINED
from qord.internal.helpers import get_optional_snowflake
from qord.internal.mixins import Comparable

import typing

if typing.TYPE_CHECKING:
    from qord.core.client import Client
    from qord.models.guilds import Guild
    from qord.models.roles import Role


__all__ = (
    "PartialEmoji",
    "Emoji",
)


class PartialEmoji(BaseModel):
    """Represents a partial emoji.

    A partial emoji is returned by in API responses in following cases:

    - For representing standard unicode emojis.
    - For representing emojis in reactions.
    - A full :class:`Emoji` object cannot be resolved from cache.

    This class supports comparison between :class:`Emoji` and :class:`PartialEmoji`.

    .. tip::
        If you have the custom emoji's parent guild, You can resolve the
        complete :class:`Emoji` object using the :meth:`.resolve` method.

    Attributes
    ----------
    id: Optional[:class:`builtins.int`]
        The ID of emoji. This can be ``None`` when the class is representing
        a standard unicode emoji rather than a custom emoji.
    name: Optional[:class:`builtins.str`]
        The name of emoji. For standard unicode emojis, This is the actual emoji
        representation and for the custom emojis, It's the emoji's name.

        For custom emojis obtained from message reactions events, This may be ``None``
        when the custom emoji data isn't available to the API. This generally happens
        when the emoji was deleted.
    animated: :class:`builtins.bool`
        Whether the emoji is animated. For unicode emojis, This is always ``False``.
    """

    if typing.TYPE_CHECKING:
        id: typing.Optional[int]
        name: typing.Optional[str]
        animated: bool

    def __init__(self, data: typing.Dict[str, typing.Any], client: Client) -> None:
        self._client = client
        self._update_with_data(data)

    def _update_with_data(self, data: typing.Dict[str, typing.Any]) -> None:
        self.id = get_optional_snowflake(data, "id")
        self.name = data.get("name")
        self.animated = data.get("animated", False)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, name={self.name!r}, animated={self.animated})"

    def __eq__(self, other: typing.Any) -> bool:
        if isinstance(other, Emoji):
            return other.id == self.id
        elif isinstance(other, self.__class__):
            return other.id == self.id and other.name == self.name

        return False

    @property
    def mention(self) -> str:
        """The string used for mentioning/rendering the emoji in Discord client.

        Returns
        -------
        :class:`builtins.str`
        """
        if self.is_unicode_emoji():
            # Name is always present here.
            return self.name  # type: ignore

        if self.animated:
            return f"<a:{self.name}:{self.id}>"

        return f"<:{self.name}:{self.id}>"

    def is_unicode_emoji(self) -> bool:
        """Indicates whether the emoji is a unicode emoji.

        Unicode emojis don't have an ID associated to them.

        Returns
        -------
        :class:`builtins.bool`
        """
        return self.id is None

    async def resolve(self, guild: Guild) -> Emoji:
        """Resolves the full :class:`Emoji` object.

        Note that this operation is not possible for unicode
        emojis (i.e :meth:`.is_unicode_emoji` returns ``True``)

        This method attempts to resolve the emoji from given
        guild's cache and if not found, would make an HTTP request
        to fetch the emoji. If the emoji is not found, the
        :class:`HTTPNotFound` error is raised.

        Parameters
        ----------
        guild: :class:`Guild`
            The guild to fetch the emoji from.

        Returns
        -------
        :class:`Emoji`
            The resolved emoji.

        Raises
        ------
        RuntimeError
            The emoji is a unicode emoji.
        HTTPNotFound
            The emoji could not be resolved.
        """
        if self.is_unicode_emoji():
            raise RuntimeError("Cannot resolve a unicode emoji.")

        # id is always an int here.
        emoji_id: int = self.id  # type: ignore
        ret = guild.cache.get_emoji(emoji_id)

        if ret:
            return ret

        ret = await guild.fetch_emoji(emoji_id)
        return ret


class Emoji(BaseModel, Comparable):
    """Represents a custom guild emoji.

    |supports-comparison|

    Attributes
    ----------
    guild: :class:`Guild`
        The guild that this emoji belongs to.
    id: :class:`builtins.int`
        The ID of this emoji.
    name: :class:`builtins.str`
        The name of this emoji.
    user: Optional[:class:`User`]
        The user that created this emoji, this can be ``None``.
    require_colons: :class:`builtins.bool`
        Whether the emoji requires to be wrapped in colons for rendering
        in Discord client.
    managed: :class:`builtins.bool`
        Whether the emoji is managed by an integration e.g Twitch.
    animated: :class:`builtins.bool`
        Whether the emoji is animated.
    available: :class:`builtins.bool`
        Whether the emoji is available. This may be ``False`` due to
        losing the server boosts causing less emoji slots in the guild.
    """

    if typing.TYPE_CHECKING:
        guild: Guild
        id: int
        name: str
        user: typing.Optional[User]
        require_colons: bool
        managed: bool
        animated: bool
        available: bool
        _role_ids: typing.List[int]
        _cached_roles: typing.Optional[typing.List[Role]]

    __slots__ = (
        "guild",
        "_client",
        "id",
        "name",
        "user",
        "require_colons",
        "managed",
        "animated",
        "available",
        "_role_ids",
        "_cached_roles",
    )

    def __init__(self, data: typing.Dict[str, typing.Any], guild: Guild) -> None:
        self.guild = guild
        self._client = guild._client
        self._update_with_data(data)

    def _update_with_data(self, data: typing.Dict[str, typing.Any]) -> None:
        # Discord Docs mark id and name as optional and nullable however
        # that is only the case for partial and unicode emojis. We'll
        # have a separate class for dealing with these two counterparts
        # so we don't have to worry about these fields being null or
        # absent here.
        self.id = int(data["id"])
        self.name = data["name"]
        self.require_colons = data.get("require_colons", True)
        self.available = data.get("available", True)
        self.managed = data.get("managed", False)
        self.animated = data.get("animated", False)
        self._role_ids = [int(role_id) for role_id in data.get("roles", [])]
        self._cached_roles = None

        try:
            user_payload = data["user"]
        except KeyError:
            self.user = None
        else:
            self.user = User(user_payload, client=self._client)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, name={self.name!r}, animated={self.animated})"

    @property
    def mention(self) -> str:
        """The string used to mention/render the emoji in Discord client.

        Returns
        -------
        :class:`builtins.str`
        """
        if self.animated:
            return f"<a:{self.name}:{self.id}>"

        return f"<:{self.name}:{self.id}>"

    @property
    def roles(self) -> typing.List[Role]:
        """The list of roles that can use this emoji.

        If the returned list is empty, the emoji is unrestricted
        and can be used by anyone in the guild.

        Returns
        -------
        List[:class:`Role`]
        """
        cached = self._cached_roles

        if cached is not None:
            return cached

        cached = []
        guild_cache = self.guild._cache

        for role_id in self._role_ids:
            role = guild_cache.get_role(role_id)

            if role:
                cached.append(role)

        self._cached_roles = cached
        return cached

    def is_useable(self) -> bool:
        """Checks whether the emoji can be used by the bot.

        Returns
        -------
        :class:`builtins.bool`
        """
        me = self.guild.me

        if me is None:
            return False

        required_roles = self.roles

        if not required_roles:
            return True

        own_roles = me.roles
        return any(role in own_roles for role in required_roles)

    async def edit(
        self,
        name: str = UNDEFINED,
        roles: typing.Optional[typing.List[Role]] = UNDEFINED,
        reason: typing.Optional[str] = None,
    ) -> None:
        """Edits this emoji.

        This operation requires :attr:`~Permissions.manage_emojis_and_stickers`
        permission in the parent emoji guild.

        Parameters
        ----------
        name: :class:`builtins.str`
            The name of emoji.
        roles: Optional[List[:class:`Role`]]
            The list of roles that can use this emoji. ``None`` or empty
            list denotes that emoji is unrestricted.
        reason: :class:`builtins.str`
            The reason for performing this action that appears on guild
            audit log.

        Raises
        ------
        HTTPForbidden
            You are missing permissions to do this.
        HTTPException
            The editing failed.
        """
        json = {}

        if name is not UNDEFINED:
            json["name"] = name

        if roles is not UNDEFINED:
            if roles is None:
                roles = []

            json["roles"] = [r.id for r in roles]

        if json:
            guild = self.guild
            data = await guild._rest.edit_guild_emoji(
                guild_id=guild.id,
                emoji_id=self.id,
                json=json,
                reason=reason,
            )
            self._update_with_data(data)

    async def delete(self, reason: typing.Optional[str] = None) -> None:
        """Deletes this emoji.

        This operation requires :attr:`~Permissions.manage_emojis_and_stickers`
        permission in the parent emoji guild.

        Parameters
        ----------
        reason: :class:`builtins.str`
            The reason for performing this action that appears on guild
            audit log.

        Raises
        ------
        HTTPForbidden
            You are missing permissions to do this.
        HTTPException
            The deleting failed.
        """
        guild = self.guild
        await guild._rest.delete_guild_emoji(
            guild_id=guild.id,
            emoji_id=self.id,
            reason=reason,
        )
