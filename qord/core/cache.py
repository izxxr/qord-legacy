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

from qord.models.users import User
from qord.models.guilds import Guild

from abc import ABC, abstractmethod
import weakref
import typing


class Cache(ABC):
    r"""Base class for creating custom cache handlers.

    This class is exposed to allow users to create implement custom cache handlers
    and configure them in a :class:`Client` using the ``cache`` parameter.

    Example::

        class MyCache(qord.Cache):
            # Implement abstract methods.
            ...

        cache = MyCache()
        client = qord.Client(cache=cache)
    """

    @abstractmethod
    def clear(self) -> None:
        r"""Clears the entire cache."""

    @abstractmethod
    def users(self) -> typing.Sequence[User]:
        r"""Returns all users that are currently cached.

        Returns
        -------
        Sequence[:class:`User`]
        """

    @abstractmethod
    def get_user(self, user_id: int) -> typing.Optional[User]:
        r"""Gets a :class:`User` from the cache with provided user ID.

        Parameters
        ----------
        user_id: :class:`builtins.int`
            The ID of user to get.

        Returns
        -------
        Optional[:class:`User`]
            The gotten user if found. If no user existed with provided ID,
            ``None`` is returned.
        """

    @abstractmethod
    def add_user(self, user: User) -> None:
        r"""Adds a :class:`User` to the cache.

        Parameters
        ----------
        user: :class:`User`
            The user to add in the cache.
        """

    @abstractmethod
    def delete_user(self, user_id: int) -> typing.Optional[User]:
        r"""Removes a :class:`User` from the cache from the given ID.

        Parameters
        ----------
        user_id: :class:`builtins.int`
            The ID of user to delete.

        Returns
        -------
        Optional[:class:`User`]
            The deleted user if any. If no user existed with provided ID,
            ``None`` is returned.
        """

    @abstractmethod
    def guilds(self) -> typing.Sequence[Guild]:
        r"""Returns all guilds that are currently cached.

        Returns
        -------
        Sequence[:class:`Guild`]
        """
    @abstractmethod
    def get_guild(self, guild_id: int) -> typing.Optional[Guild]:
        r"""Gets a :class:`Guild` from the cache with provided guild ID.

        Parameters
        ----------
        guild_id: :class:`builtins.int`
            The ID of guild to get.

        Returns
        -------
        Optional[:class:`Guild`]
            The gotten guild if found. If no guild existed with provided ID,
            ``None`` is returned.
        """

    @abstractmethod
    def add_guild(self, guild: Guild) -> None:
        r"""Adds a :class:`Guild` to the cache.

        Parameters
        ----------
        guild: :class:`Guild`
            The guild to add in the cache.
        """

    @abstractmethod
    def delete_guild(self, guild_id: int) -> typing.Optional[Guild]:
        r"""Removes a :class:`Guild` from the cache from the given ID.

        Parameters
        ----------
        guild_id: :class:`builtins.int`
            The ID of guild to delete.

        Returns
        -------
        Optional[:class:`Guild`]
            The deleted guild if any. If no guild existed with provided ID,
            ``None`` is returned.
        """


class GuildCache(ABC):
    r"""Abstract base class for creating custom cache handler for guilds.

    You can use this class to implement custom cache handlers for caching guild
    related entities and configure them in a :class:`Client` by overriding the
    :meth:`.get_guild_cache` method.
    """
    def __init__(self, guild: Guild) -> None:
        self.guild = guild

    @abstractmethod
    def clear(self) -> None:
        r"""Clears the entire cache."""

class DefaultCache(Cache):
    r"""In-memory cache implementation.

    This is the default cache handler used by the :class:`Client` that
    implements basic "in memory" caching.

    .. tip:: "Custom cache handler"
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

    .. tip:: "Custom cache handler"
        If you want to implement custom cache handlers, See the :class:`GuildCache`
        documentation.
    """

    def clear(self) -> None:
        ...
