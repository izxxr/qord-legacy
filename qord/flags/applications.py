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


__all__ = (
    "ApplicationFlags",
)


class ApplicationFlags(Flags):
    """:class:`Flags` subclass that details the flags of a :class:`Application`. This is mostly
    obtained using :attr:`Application.flags` or :attr:`Client.application_flags` attribute.

    The application flags detail the features of an application.
    """

    gateway_presence = 1 << 12
    """Whether the application has gateway presence intent."""

    gateway_presence_limited = 1 << 13
    """Whether the application requires whitelisting to use gateway presence intent."""

    gateway_members = 1 << 14
    """Whether the application has gateway guild members intent."""

    gateway_members_limited = 1 << 15
    """Whether the application requires whitelisting to use gateway members intents."""

    verification_pending_guild_limit = 1 << 16
    """Indicates unusual growth of an app that prevents verification."""

    embedded = 1 << 17
    """Whether the application is embedded application in Discord client."""

    gateway_message_content = 1 << 18
    """Whether the application has gateway guild message content intent."""

    gateway_message_content_limited = 1 << 19
    """Whether the application requires whitelisting to use gateway message content intents."""
