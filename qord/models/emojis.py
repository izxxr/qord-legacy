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

import typing

if typing.TYPE_CHECKING:
    from qord.models.guilds import Guild
    from qord.models.roles import Role


__all__ = (
    "Emoji",
)


class Emoji(BaseModel):
    """Represents a custom guild emoji.

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
