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

from qord.flags.base import Flags


class Intents(Flags):
    r""":class:`Flags` subclass that details the gateway intents.

    Gateway intents allow you to toggle specific gateway events if whether
    you want to receive them or not. This also affects the caching for relevant
    entity. Gateway intents are useful to disable events that you don't need for
    your bot and decrease the workload. For example, if your bot doesn't need
    direct messages events, you can set :attr:`.direct_messages` to ``False``.

    Some intents are marked as privileged. These intents are required to be
    enabled explicitly from the bot's application page on Discord Developers Portal.
    If the bot is in more then 100 servers, These intents require verification
    and whitelisting.

    Attempting to enable these intents without enabling them from Developers Portal
    will cause the bot to terminate with :exc:`MissingPrivilegedIntents` error.

    Current privileged intents are:

    - :attr:`.members`
    - :attr:`.presences`
    """

    guilds = 1 << 0
    r"""Whether to enable guild events and caching.

    This intent is generally required by most bots and disabling it will
    cause most of functionality of library to be disabled. Only disable this
    when your bot is completely DMs or interactions based.
    """

    members = 1 << 1
    r"""Whether to enable events and caching for guild members. This
    also controls most of bot's user caching.

    This is a privileged intent, See :class:`GatewayIntents` documentation.
    """

    bans = 1 << 2
    r"""Whether to enable events for guild bans."""

    emojis_and_stickers = 1 << 3
    r"""Whether to enable events for guild stickers and emojis."""

    integrations = 1 << 4
    r"""Whether to enable events for guild integrations."""

    webhooks = 1 << 5
    r"""Whether to enable events for webhooks."""

    invites = 1 << 6
    r"""Whether to enable events for invites."""

    voice_states = 1 << 7
    r"""Whether to enable events for voice state updates."""

    presences = 1 << 8
    r"""Whether to enable events and for presences.

    This is a privileged intent, See :class:`GatewayIntents` documentation.
    """

    guild_messages = 1 << 9
    r"""Whether to enable events and caching for guild messages."""

    guild_message_reactions  = 1 << 10
    r"""Whether to enable events and caching for reactions on guild messages."""

    guild_message_typing = 1 << 11
    r"""Whether to enable events for message typing in guilds."""

    direct_messages = 1 << 12
    r"""Whether to enable events and caching for direct messages."""

    direct_message_reactions  = 1 << 13
    r"""Whether to enable events and caching for reactions on direct messages."""

    direct_message_typing = 1 << 14
    r"""Whether to enable events for message typing in DMs."""

    scheduled_events = 1 << 16
    r"""Whether to enable events and caching for guild scheduled events."""

    @classmethod
    def all(cls) -> Intents:
        r"""Returns the :class:`Intents` with all intents *including* privileged enabled."""
        return cls(sum(cls.__name_value_map__.values()))

    @classmethod
    def unprivileged(cls) -> Intents:
        r"""Returns the :class:`Intents` with all intents *excluding* privileged enabled."""
        ret = cls.all()
        ret.members = False
        ret.presences = False
        return ret
