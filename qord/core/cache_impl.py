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

from qord.core.cache import Cache, GuildCache
from qord.models.users import User
from qord.models.guilds import Guild
from qord.models.roles import Role
from qord.models.guild_members import GuildMember

import weakref
import typing


class DefaultCache(Cache):
    r"""In-memory cache implementation.

    This is the default cache handler used by the :class:`Client` that
    implements basic "in memory" caching. Obtainable through :attr:`Client.cache`.

    .. tip::
        If you want to implement custom cache handlers, See the :class:`Cache`
        documentation.
    """

    def clear(self) -> None:
        self._users = weakref.WeakValueDictionary()
        self._guilds = dict()

    def users(self) -> typing.Sequence[User]:
        return list(self._users.values())

    def get_user(self, user_id: int) -> typing.Optional[User]:
        if not isinstance(user_id, int):
            raise TypeError("Parameter user_id must be an integer.")

        return self._users.get(user_id)

    def add_user(self, user: User) -> None:
        if not isinstance(user, User):
            raise TypeError("Parameter user must be an instance of User.")

        self._users[user.id] = user

    def delete_user(self, user_id: int) -> typing.Optional[User]:
        if not isinstance(user_id, int):
            raise TypeError("Parameter user_id must be an integer.")

        return self._users.pop(user_id, None)

    def guilds(self) -> typing.Sequence[Guild]:
        return list(self._guilds.values())

    def get_guild(self, guild_id: int) -> typing.Optional[Guild]:
        if not isinstance(guild_id, int):
            raise TypeError("Parameter guild_id must be an integer.")

        return self._guilds.get(guild_id)

    def add_guild(self, guild: Guild) -> None:
        if not isinstance(guild, Guild):
            raise TypeError("Parameter guild must be an instance of Guild.")

        self._guilds[guild.id] = guild

    def delete_guild(self, guild_id: int) -> typing.Optional[Guild]:
        if not isinstance(guild_id, int):
            raise TypeError("Parameter guild_id must be an integer.")

        return self._guilds.pop(guild_id, None)


class DefaultGuildCache(GuildCache):
    r"""In-memory cache implementation for guilds.

    This is the default cache handler used by the :class:`Client` that
    implements basic "in memory" caching for entities related to :class:`Guild`. Obtainable
    through :attr:`Guild.cache`.

    .. tip::
        If you want to implement custom cache handlers, See the :class:`GuildCache`
        documentation.
    """

    def clear(self) -> None:
        self._roles: typing.Dict[int, Role] = {}
        self._members: typing.Dict[int, GuildMember] = {}

    def roles(self) -> typing.Sequence[Role]:
        r"""Returns all roles that are currently cached.

        This implementation sorts the returned sequence of roles
        in ascending order according to their :attr:`~Role.position`.

        Returns
        -------
        Sequence[:class:`Role`]
        """
        roles = list(self._roles.values())
        roles.sort(key=lambda role: role.position)
        return roles

    def add_role(self, role: Role) -> None:
        if not isinstance(role, Role):
            raise TypeError("Parameter role must be an instance of Role.")

        self._roles[role.id] = role

    def get_role(self, role_id: int) -> typing.Optional[Role]:
        if not isinstance(role_id, int):
            raise TypeError("Parameter role_id must be an integer.")

        return self._roles.get(role_id)

    def delete_role(self, role_id: int) -> typing.Optional[Role]:
        if not isinstance(role_id, int):
            raise TypeError("Parameter role_id must be an integer.")

        return self._roles.pop(role_id, None)

    def members(self) -> typing.Sequence[GuildMember]:
        return list(self._members.values())

    def add_member(self, member: GuildMember) -> None:
        if not isinstance(member, GuildMember):
            raise TypeError("Parameter member must be an instance of GuildMember.")

        self._members[member.user.id] = member

    def get_member(self, user_id: int) -> typing.Optional[GuildMember]:
        if not isinstance(user_id, int):
            raise TypeError("Parameter user_id must be an integer.")

        return self._members.get(user_id)

    def delete_member(self, user_id: int) -> typing.Optional[GuildMember]:
        if not isinstance(user_id, int):
            raise TypeError("Parameter user_id must be an integer.")

        return self._members.pop(user_id)
