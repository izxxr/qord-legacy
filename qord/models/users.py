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

from qord.models.base import BaseModel
import typing

if typing.TYPE_CHECKING:
    from qord.core.client import Client

class User(BaseModel):
    r"""Representation of a Discord user entity.

    Attributes
    ----------
    id: :class:`builtins.int`
        The ID of user.
    name: :class:`builtins.str`
        The username of user.
    discriminator: :class:`builtins.str`
        The four digits discriminator for the user.
    avatar: typing.Optional[:class:`builtins.str`]
        The user's avatar hash. This can be ``None`` if user has no custom
        avatar set. For obtaining the URL, consider using :meth:`.avatar_url`.
    bot: :class:`builtins.bool`
        Whether the user is a bot.
    system: :class:`builtins.bool`
        Whether the user is official Discord system user.
    banner: typing.Optional[:class:`builtins.str`]
        The user's banner hash. This can be ``None`` if user has no custom
        banner set. For obtaining the URL, consider using :meth:`.banner_url`.
    accent_color: :class:`builtins.int`
        An integer representation of user's accent colour.
    locale: :class:`builtins.str`
        The user's chosen default language.
    flags: :class:`UserFlags`
        The user's flags.
    premium_type: :class:`builtins.int`
        The user's premium subscription type integer value. See :class:`PremiumType` for
        more information about all values meaning.
    """

    if typing.TYPE_CHECKING:
        id: int
        name: str
        discriminator: str
        bot: bool
        system: bool
        accent_color: int
        locale: str
        premium_type: int
        avatar: typing.Optional[str]
        banner: typing.Optional[str]

    __slots__ = ("_client", "id", "name", "discriminator", "bot", "accent_color",
                "premium_type", "system",  "locale", "avatar", "banner",)

    def __init__(self, data: typing.Dict[str, typing.Any], client: Client) -> None:
        self._client = client
        self._update_with_data(data)

    def _update_with_data(self, data: typing.Dict[str, typing.Any]) -> None:
        self.id = int(data["id"])
        self.name = data["username"]
        self.discriminator = data["discriminator"]
        self.bot = data.get("bot", False)
        self.accent_color = data.get("accent_color", 0)
        self.premium_type = data.get("premium_type", 0)
        self.system = data.get("system", False)
        self.locale = data.get("locale", "en-US")
        self.avatar = data.get("avatar")
        self.banner = data.get("banner")


class ClientUser(User):
    r"""Representation of user entity for the connected client.

    This class also subclasses :class:`User`. You can obtain class using the
    :class:`Client.user` attribute.

    Attributes
    ----------
    verified: typing.Optional[:class:`builtins.bool`]
        Whether the user is verified using a valid email. Requires the ``email``
        OAuth2 scope.
    email: typing.Optional[:class:`builtins.str`]
        The email of this user. Requires the ``email`` OAuth2 scope, ``None`` otherwise.
    mfa_enabled: :class:`builtins.bool`
        Whether the user has 2FA enabled on their account.
    """
    if typing.TYPE_CHECKING:
        verified: typing.Optional[bool]
        email: typing.Optional[str]
        mfa_enabled: bool

    __slots__ = ("email", "verified", "mfa_enabled")

    def _update_with_data(self, data: typing.Dict[str, typing.Any]) -> None:
        super()._update_with_data(data)

        self.email = data.get("email")
        self.verified = data.get("verified")
        self.mfa_enabled = data.get("mfa_enabled", False)
