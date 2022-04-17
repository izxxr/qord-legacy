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

from abc import ABC, abstractmethod
import typing

if typing.TYPE_CHECKING:
    from qord.models.users import User
    from qord.models.guilds import Guild
    from qord.models.roles import Role
    from qord.models.guild_members import GuildMember
    from qord.models.channels import GuildChannel, PrivateChannel
    from qord.models.messages import Message
    from qord.models.emojis import Emoji
    from qord.models.scheduled_events import ScheduledEvent
    from qord.models.stage_instances import StageInstance


__all__ = (
    "Cache",
    "GuildCache",
)

class Cache(ABC):
    """Base class for creating custom cache handlers.

    This class is exposed to allow users to create implement custom cache handlers
    and configure them in a :class:`Client` using the ``cache`` parameter.

    Example::

        class MyCache(qord.Cache):
            # Implement abstract methods.
            ...

        cache = MyCache()
        client = qord.Client(cache=cache)

    Parameters
    ----------
    message_limit: :class:`builtins.int`
        The number of messages to cache at a time. Defaults to ``100``. ``None`` or
        ``0`` will disable message cache.

    Attributes
    ----------
    message_limit: :class:`builtins.int`
        The number of messages to cache at a time.
    """

    def __init__(self, message_limit: int = 100) -> None:
        if not isinstance(message_limit, int):
            raise TypeError("message_limit parameter must be an integer.")
        if message_limit is None:
            message_limit = 0

        self.message_limit = message_limit

    @property
    def message_cache_enabled(self) -> bool:
        """Indicates whether the message cache is enabled.

        Returns
        -------
        :class:`builtins.bool`
        """
        return self.message_limit > 0

    @abstractmethod
    def clear(self) -> None:
        """Clears the entire cache."""

    @abstractmethod
    def users(self) -> typing.List[User]:
        """Returns all users that are currently cached.

        Returns
        -------
        List[:class:`User`]
        """

    @abstractmethod
    def get_user(self, user_id: int) -> typing.Optional[User]:
        """Gets a :class:`User` from the cache with provided user ID.

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
        """Adds a :class:`User` to the cache.

        Parameters
        ----------
        user: :class:`User`
            The user to add in the cache.
        """

    @abstractmethod
    def delete_user(self, user_id: int) -> typing.Optional[User]:
        """Removes a :class:`User` from the cache from the given ID.

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
    def guilds(self) -> typing.List[Guild]:
        """Returns all guilds that are currently cached.

        Returns
        -------
        List[:class:`Guild`]
        """

    @abstractmethod
    def get_guild(self, guild_id: int) -> typing.Optional[Guild]:
        """Gets a :class:`Guild` from the cache with provided guild ID.

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
        """Adds a :class:`Guild` to the cache.

        Parameters
        ----------
        guild: :class:`Guild`
            The guild to add in the cache.
        """

    @abstractmethod
    def delete_guild(self, guild_id: int) -> typing.Optional[Guild]:
        """Removes a :class:`Guild` from the cache from the given ID.

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

    @abstractmethod
    def messages(self) -> typing.List[Message]:
        """Gets all messages that are currently cached.

        Returns
        -------
        List[:class:`Message`]
            The list of messages cached.
        """

    @abstractmethod
    def add_message(self, message: Message) -> None:
        """Adds a :class:`Message` to the cache.

        Once the :attr:`.message_limit` is reached, The messages
        that are previously cache are removed, Clearing the message
        cache.

        Parameters
        ----------
        message: :class:`Message`
            The message to add in the cache.
        """

    @abstractmethod
    def get_message(self, message_id: int) -> typing.Optional[Message]:
        """Gets a :class:`Message` from the cache by the provided message ID.

        Parameters
        ----------
        message_id: :class:`builtins.int`
            The message ID to get message for.

        Returns
        -------
        Optional[:class:`Message`]
            The gotten message if any. If no message existed with provided ID,
            ``None`` is returned.
        """

    @abstractmethod
    def delete_message(self, message_id: int) -> typing.Optional[Message]:
        """Deletes a :class:`Message` from the cache by the provided message ID.

        Parameters
        ----------
        message_id: :class:`builtins.int`
            The message ID to remove message for.

        Returns
        -------
        Optional[:class:`Message`]
            The deleted message if any. If no message existed with provided ID,
            ``None`` is returned.
        """

    @abstractmethod
    def private_channels(self) -> typing.List[PrivateChannel]:
        """Gets all private channels that are currently cached.

        Returns
        -------
        List[:class:`PrivateChannel`]
            The list of private channels cached.
        """

    @abstractmethod
    def add_private_channel(self, private_channel: PrivateChannel) -> None:
        """Adds a :class:`PrivateChannel` to the cache.

        Parameters
        ----------
        private_channel: :class:`Message`
            The private channel to add in the cache.
        """

    @abstractmethod
    def get_private_channel(self, channel_id: int) -> typing.Optional[PrivateChannel]:
        """Gets a :class:`PrivateChannel` from the cache by the provided channel ID.

        Parameters
        ----------
        channel_id: :class:`builtins.int`
            The private channel ID to get channel for.

        Returns
        -------
        Optional[:class:`PrivateChannel`]
            The gotten channel if any. If no private channel existed with provided ID,
            ``None`` is returned.
        """

    @abstractmethod
    def delete_private_channel(self, channel_id: int) -> typing.Optional[PrivateChannel]:
        """Deletes a :class:`PrivateChannel` from the cache by the provided channel ID.

        Parameters
        ----------
        channel_id: :class:`builtins.int`
            The private channel ID to delete channel for.

        Returns
        -------
        Optional[:class:`PrivateChannel`]
            The deleted channel if any. If no private channel existed with provided ID,
            ``None`` is returned.
        """


class GuildCache(ABC):
    """Abstract base class for creating custom cache handler for guilds.

    You can use this class to implement custom cache handlers for caching guild
    related entities and configure them in a :class:`Client` by overriding the
    :meth:`.get_guild_cache` method.

    Parameters
    ----------
    guild: :class:`Guild`
        The guild that this cache handler belongs to.
    """
    def __init__(self, guild: Guild) -> None:
        self.guild = guild

    @abstractmethod
    def clear(self) -> None:
        """Clears the entire cache."""

    @abstractmethod
    def roles(self) -> typing.List[Role]:
        """Returns all roles that are currently cached.

        Returns
        -------
        List[:class:`Role`]
        """

    @abstractmethod
    def get_role(self, role_id: int) -> typing.Optional[Role]:
        """Gets a :class:`Role` from the cache with provided role ID.

        Parameters
        ----------
        role_id: :class:`builtins.int`
            The ID of role to get.

        Returns
        -------
        Optional[:class:`Role`]
            The gotten role if found. If no role existed with provided ID,
            ``None`` is returned.
        """

    @abstractmethod
    def add_role(self, role: Role) -> None:
        """Adds a :class:`Role` to the cache.

        Parameters
        ----------
        role: :class:`Role`
            The role to add in the cache.
        """

    @abstractmethod
    def delete_role(self, role_id: int) -> typing.Optional[Role]:
        """Removes a :class:`Role` from the cache from the given ID.

        Parameters
        ----------
        role_id: :class:`builtins.int`
            The ID of role to delete.

        Returns
        -------
        Optional[:class:`Role`]
            The deleted role if any. If no role existed with provided ID,
            ``None`` is returned.
        """

    @abstractmethod
    def members(self) -> typing.List[GuildMember]:
        """Returns all members that are currently cached.

        Returns
        -------
        List[:class:`GuildMember`]
        """

    @abstractmethod
    def get_member(self, user_id: int) -> typing.Optional[GuildMember]:
        """Gets a :class:`GuildMember` from the cache for provided user ID.

        Parameters
        ----------
        user_id: :class:`builtins.int`
            The ID of user to get member of.

        Returns
        -------
        Optional[:class:`GuildMember`]
            The gotten member if found. If no member existed with provided ID,
            ``None`` is returned.
        """

    @abstractmethod
    def add_member(self, member: GuildMember) -> None:
        """Adds a :class:`GuildMember` to the cache.

        Parameters
        ----------
        member: :class:`GuildMember`
            The member to add in the cache.
        """

    @abstractmethod
    def delete_member(self, user_id: int) -> typing.Optional[GuildMember]:
        """Removes a :class:`GuildMember` from the cache for provided user ID.

        Parameters
        ----------
        user_id: :class:`builtins.int`
            The ID of user to delete the member of.

        Returns
        -------
        Optional[:class:`GuildMember`]
            The deleted member if any. If no member existed with provided ID,
            ``None`` is returned.
        """


    @abstractmethod
    def channels(self) -> typing.List[GuildChannel]:
        """Returns all channels that are currently cached.

        Returns
        -------
        List[:class:`GuildChannel`]
        """

    @abstractmethod
    def get_channel(self, channel_id: int) -> typing.Optional[GuildChannel]:
        """Gets a :class:`GuildChannel` from the cache for provided channel ID.

        Parameters
        ----------
        channel_id: :class:`builtins.int`
            The ID of channel to get.

        Returns
        -------
        Optional[:class:`GuildChannel`]
            The gotten channel if found. If no channel existed with provided ID,
            ``None`` is returned.
        """

    @abstractmethod
    def add_channel(self, channel: GuildChannel) -> None:
        """Adds a :class:`GuildChannel` to the cache.

        Parameters
        ----------
        channel: :class:`GuildChannel`
            The channel to add in the cache.
        """

    @abstractmethod
    def delete_channel(self, channel_id: int) -> typing.Optional[GuildChannel]:
        """Removes a :class:`GuildChannel` from the cache for provided channel ID.

        Parameters
        ----------
        channel_id: :class:`builtins.int`
            The ID of channel to delete.

        Returns
        -------
        Optional[:class:`GuildChannel`]
            The deleted channel if any. If no channel existed with provided ID,
            ``None`` is returned.
        """

    @abstractmethod
    def emojis(self) -> typing.List[Emoji]:
        """Returns all the emojis that are currently cached.

        Returns
        -------
        List[:class:`Emoji`]
        """

    @abstractmethod
    def set_emojis(self, emojis: typing.List[Emoji]) -> None:
        """Replaces the emojis cache with the given list of emojis.

        All previous emojis are removed from cache and new emojis
        from the given list are added to cache.

        Parameters
        ----------
        emojis: List[:class:`Emoji`]
            The list of emojis to set.
        """

    @abstractmethod
    def get_emoji(self, emoji_id: int) -> typing.Optional[Emoji]:
        """Gets a :class:`Emoji` from the cache for provided emoji ID.

        Parameters
        ----------
        emoji_id: :class:`builtins.int`
            The ID of emoji to get.

        Returns
        -------
        Optional[:class:`Emoji`]
            The gotten emoji if found. If no emoji existed with provided ID,
            ``None`` is returned.
        """

    @abstractmethod
    def add_emoji(self, emoji: Emoji) -> None:
        """Adds a :class:`Emoji` to the cache.

        Parameters
        ----------
        emoji: :class:`Emoji`
            The emoji to add in the cache.
        """

    @abstractmethod
    def delete_emoji(self, emoji_id: int) -> typing.Optional[Emoji]:
        """Removes a :class:`Emoji` from the cache for provided emoji ID.

        Parameters
        ----------
        emoji_id: :class:`builtins.int`
            The ID of emoji to get.

        Returns
        -------
        Optional[:class:`Emoji`]
            The deleted emoji if found. If no emoji existed with provided ID,
            ``None`` is returned.
        """

    @abstractmethod
    def scheduled_events(self) -> typing.List[ScheduledEvent]:
        """Returns all scheduled events that are currently cached.

        Returns
        -------
        List[:class:`ScheduledEvent`]
        """

    @abstractmethod
    def get_scheduled_event(self, scheduled_event_id: int) -> typing.Optional[ScheduledEvent]:
        """Gets a :class:`ScheduledEvent` from the cache for provided event ID.

        Parameters
        ----------
        scheduled_event_id: :class:`builtins.int`
            The ID of scheduled event to get.

        Returns
        -------
        Optional[:class:`ScheduledEvent`]
            The gotten event if found. If no event existed with provided ID,
            ``None`` is returned.
        """

    @abstractmethod
    def add_scheduled_event(self, scheduled_event: ScheduledEvent) -> None:
        """Adds a :class:`ScheduledEvent` to the cache.

        Parameters
        ----------
        scheduled_event: :class:`ScheduledEvent`
            The event to add in the cache.
        """

    @abstractmethod
    def delete_scheduled_event(self, scheduled_event_id: int) -> typing.Optional[ScheduledEvent]:
        """Removes a :class:`ScheduledEvent` from the cache for provided event ID.

        Parameters
        ----------
        scheduled_event_id: :class:`builtins.int`
            The ID of scheduled event to remove.

        Returns
        -------
        Optional[:class:`ScheduledEvent`]
            The removed event if any. If no event existed with provided ID,
            ``None`` is returned.
        """

    @abstractmethod
    def stage_instances(self) -> typing.List[StageInstance]:
        """Returns all stage instances that are currently cached.

        Returns
        -------
        List[:class:`StageInstance`]
        """

    @abstractmethod
    def get_stage_instance(self, stage_instance_id: int) -> typing.Optional[StageInstance]:
        """Gets a :class:`StageInstance` from the cache for provided instance ID.

        Parameters
        ----------
        stage_instance_id: :class:`builtins.int`
            The ID of stage instance to get.

        Returns
        -------
        Optional[:class:`StageInstance`]
            The gotten stage instance if found. If no instance existed with provided ID,
            ``None`` is returned.
        """

    @abstractmethod
    def add_stage_instance(self, stage_instance: StageInstance) -> None:
        """Adds a :class:`StageInstance` to the cache.

        Parameters
        ----------
        stage_instance: :class:`StageInstance`
            The stage instance to add in the cache.
        """

    @abstractmethod
    def delete_stage_instance(self, stage_instance_id: int) -> typing.Optional[StageInstance]:
        """Removes a :class:`StageInstance` from the cache for provided ID.

        Parameters
        ----------
        stage_instance_id: :class:`builtins.int`
            The ID of stage instance to remove.

        Returns
        -------
        Optional[:class:`StageInstance`]
            The removed stage instance if any. If none existed with provided ID,
            ``None`` is returned.
        """
