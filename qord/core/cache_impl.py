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
from qord.models.channels import GuildChannel, PrivateChannel
from qord.models.messages import Message

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
        self._private_channels = weakref.WeakValueDictionary()
        self._guilds = dict()
        self._messages = dict()

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

    def messages(self) -> typing.Sequence[Message]:
        return list(self._messages.values())

    def get_message(self, message_id: int) -> typing.Optional[Message]:
        if not isinstance(message_id, int):
            raise TypeError("Parameter message_id must be an integer.")

        return self._messages.get(message_id)

    def add_message(self, message: Message) -> None:
        if not isinstance(message, Message):
            raise TypeError("Parameter message must be an instance of Message")

        messages = self._messages

        if len(messages) >= self.message_limit:
            messages.clear()

        messages[message.id] = message

    def delete_message(self, message_id: int) -> typing.Optional[Message]:
        if not isinstance(message_id, int):
            raise TypeError("Parameter message_id must be an integer.")

        return self._messages.pop(message_id, None)

    def private_channels(self) -> typing.Sequence[PrivateChannel]:
        return list(self._private_channels.values())

    def add_private_channel(self, private_channel: PrivateChannel) -> None:
        if not isinstance(private_channel, PrivateChannel):
            raise TypeError("Parameter private_channel must be an instance of PrivateChannel")

        self._private_channels[private_channel.id] = private_channel

    def get_private_channel(self, channel_id: int) -> typing.Optional[PrivateChannel]:
        if not isinstance(channel_id, int):
            raise TypeError("Parameter channel_id must be an integer.")

        return self._private_channels.get(channel_id, None)

    def delete_private_channel(self, channel_id: int) -> typing.Optional[PrivateChannel]:
        if not isinstance(channel_id, int):
            raise TypeError("Parameter channel_id must be an integer.")

        return self._private_channels.pop(channel_id, None)


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
        self._channels: typing.Dict[int, GuildChannel] = {}

    def roles(self) -> typing.Sequence[Role]:
        roles = list(self._roles.values())
        # Multiple roles may share same positions so
        # we cannot rely on this behaviour.
        roles.sort(key=lambda role: role.position) # Undocumented, see above
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

        return self._members.pop(user_id, None)

    def channels(self) -> typing.Sequence[GuildChannel]:
        ret = list(self._channels.values())
        # Multiple channels may share the same position so
        # we cannot rely on this behaviour.
        ret.sort(key=lambda c: c.position) # Undocumented, see above
        return ret

    def get_channel(self, channel_id: int) -> typing.Optional[GuildChannel]:
        if not isinstance(channel_id, int):
            raise TypeError("Parameter channel_id must be an integer.")

        return self._channels.get(channel_id)

    def add_channel(self, channel: GuildChannel) -> None:
        if not isinstance(channel, GuildChannel):
            raise TypeError("Parameter channel must be an instance of GuildChannel.")

        self._channels[channel.id] = channel

    def delete_channel(self, channel_id: int) -> typing.Optional[GuildChannel]:
        if not isinstance(channel_id, int):
            raise TypeError("Parameter channel_id must be an integer.")

        return self._channels.pop(channel_id, None)
