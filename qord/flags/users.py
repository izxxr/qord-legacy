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

class UserFlags(Flags):
    r""":class:`Flags` subclass that details the flags of a :class:`User`. This is mostly
    obtained using :attr:`User.flags` attribute.

    A user's flags include several things including the "badges" on the
    user's account etc.
    """

    staff = 1 << 0
    r"""User is a Discord employee/staff."""

    partner = 1 << 1
    r"""User is a owner of a partnered guild."""

    hypesquad = 1 << 2
    r"""User is a HypeSquad's events coordinator."""

    bug_hunter_level_1 = 1 << 3
    r"""User is a level 1 bug hunter."""

    hypesquad_bravery = 1 << 6
    r"""User is member of HypeSquad bravey house."""

    hypesquad_brilliance = 1 << 7
    r"""User is member of HypeSquad brilliance house."""

    hypesquad_brilliance = 1 << 8
    r"""User is member of HypeSquad balance house."""

    early_premium_supporter = 1 << 9
    r"""User is an early nitro supporter."""

    team = 1 << 10
    r"""User is a psuedo user, representing a team."""

    bug_hunter_level_2 = 1 << 14
    r"""User is a bug hunter of level 2."""

    verified_bot = 1 << 16
    r"""User is a verified bot."""

    verified_developer = 1 << 17
    r"""User is a "early" verified bot developer."""

    certified_moderator = 1 << 18
    r"""User is a certified Discord moderator."""

    bot_http_interactions = 1 << 19
    r"""The user (bot) only uses HTTPs for interactions."""
