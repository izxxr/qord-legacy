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
    "MessageFlags",
)


class MessageFlags(Flags):
    """:class:`Flags` subclass that details the flags of a :class:`Message`.

    This is mostly obtained using :attr:`Message.flags` attribute.
    """

    crossposted = 1 << 0
    """The message is crossposted to following channels."""

    is_crosspost = 1 << 1
    """The message is a crosspost from another channel."""

    suppress_embeds = 1 << 2
    """The message does not include any embeds."""

    source_message_deleted = 1 << 3
    """The source message for a crosspost message is deleted."""

    urgent = 1 << 4
    """The message is an urgent message from system."""

    has_thread = 1 << 5
    """The message has a thread associated to tit."""

    ephemeral = 1 << 6
    """The message is an ephemeral message, in response to interaction."""

    loading = 1 << 7
    """The message is an interaction response and application is in "Thinking" state."""

    thread_role_mention_failed = 1 << 8
    """This message failed to mention some roles and add their members in a thread."""
