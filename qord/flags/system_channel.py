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
    "SystemChannelFlags",
)


class SystemChannelFlags(Flags):
    r""":class:`Flags` subclass that details the flags for a guild's system channel."""

    suppress_join_notifications = 1 << 0
    r"""Whether system channel will not receive a random message when a member joins."""

    suppress_premium_subscriptions = 1 << 1
    r"""Whether system channel will not receive a notification when someone boosts the guild."""

    suppress_guild_reminders = 1 << 2
    r"""Whether system channel will not receive tips for setting up guilds."""

    suppress_join_notification_replies = 1 << 3
    r"""Whether messages sent on member join in system channel allow replying with stickers."""
