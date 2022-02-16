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


class Permissions(Flags):
    r"""A class that provides rich interface for manipulating permissions bitwise value.

    This class subclasses :class:`Flags`. See it's documentation for more info about
    using this class for working with permissions.
    """

    create_instant_invite = 1 << 0
    r"""Allows creating instant guild or channel invites."""

    kick_members = 1 << 1
    r"""Allows kicking other members from a guild."""

    ban_members = 1 << 2
    r"""Allows banning other members from a guild."""

    administrator = 1 << 3
    r"""Bypasses all permissions.

    Members with this permission enabled have all permissions enabled
    and they bypass all permission overwrites.
    """

    manage_channels = 1 << 4
    r"""Allows management of the guild channels."""

    manage_guild = 1 << 5
    r"""Allows management of the guild settings including adding bots."""

    add_reactions = 1 << 6
    r"""Allows the addition of reactions on messages."""

    view_audit_log = 1 << 7
    r"""Allows viewing of the guild's audit log."""

    priority_speaker = 1 << 8
    r"""Allows usage of priority speaker in a guild voice channel."""

    stream = 1 << 9
    r"""Allows live streaming in a voice channel."""

    view_channel = 1 << 10
    r"""Allows viewing guild channel."""

    send_messages = 1 << 11
    r"""Allows to send messages in text channels."""

    send_tts_messages = 1 << 12
    r"""Allows the users to send TTS messages through ``/tts`` command."""

    manage_messages = 1 << 13
    r"""Allows management of messages."""

    embed_links = 1 << 14
    r"""Allows usage of embedded links in the messages."""

    attach_files = 1 << 15
    r"""Allows attaching files to the messages."""

    read_message_history = 1 << 16
    r"""Allows reading a text channel's message history."""

    mention_everyone = 1 << 17
    r"""Allows mentioning the @everyone and @here roles."""

    use_external_emojis = 1 << 18
    r"""Allows usage of emojis from other guilds."""

    view_guild_insights = 1 << 19
    r"""Allows viewing the guild's insights data."""

    connect = 1 << 20
    r"""Allows joining a voice or stage channel."""

    speak = 1 << 21
    r"""Allows speaking in a voice channel."""

    mute_members = 1 << 22
    r"""Allows muting members in a voice channel."""

    deafen_members = 1 << 23
    r"""Allows deafening members in a voice channel."""

    move_members = 1 << 24
    r"""Allows moving and removing members from a voice channel."""

    use_vad = 1 << 25
    r"""Allows usage of voice activity detection in a voice channel."""

    change_nickname = 1 << 26
    r"""Allows changing own username in the guild."""

    manage_nicknames = 1 << 27
    r"""Allows changing other members nickname in a guild."""

    manage_roles = 1 << 28
    r"""Allows management of guild roles."""

    manage_permissions = manage_roles
    r"""An alias for :attr:`.manage_roles`."""

    manage_webhooks = 1 << 29
    r"""Allows management of guild webhooks."""

    manage_emojis_and_stickers = 1 << 30
    r"""Allows management of emojis and stickers of a guild."""

    use_application_commands = 1 << 31
    r"""Allows usage of application commands in a guild."""

    request_to_speak = 1 << 32
    r"""Allows requesting to speak in a stage channel."""

    manage_events = 1 << 33
    r"""Allows management of guild scheduled events."""

    manage_threads = 1 << 34
    r"""Allows management of threads."""

    create_public_threads = 1 << 35
    r"""Allows creation of public or news threads."""

    create_private_threads = 1 << 36
    r"""Allows creation of private threads."""

    use_external_stickers = 1 << 37
    r"""Allows usage of external stickers."""

    send_messages_in_threads = 1 << 38
    r"""Allows sending of messages in therads."""

    start_embedded_activities = 1 << 39
    r"""Allows starting embedded activities in a voice channel."""

    moderate_members = 1 << 40
    r"""Allows moderating members including managing members timeout."""
