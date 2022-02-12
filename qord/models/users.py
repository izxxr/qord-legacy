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

from qord.flags.users import UserFlags
from qord.models.base import BaseModel
from qord.enums import DefaultAvatar
from qord._helpers import create_cdn_url, get_image_data, EMPTY

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
    public_flags: :class:`UserFlags`
        The user's public flags.
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
                "premium_type", "system",  "locale", "avatar", "banner", "flags",
                "public_flags")

    def __init__(self, data: typing.Dict[str, typing.Any], client: Client) -> None:
        self._client = client
        self._update_with_data(data)

    def _update_with_data(self, data: typing.Dict[str, typing.Any]) -> None:
        self.id = int(data["id"])
        self.name = data["username"]
        self.discriminator = data["discriminator"]
        self.bot = data.get("bot", False)
        self.flags = UserFlags(data.get("flags", 0))
        self.public_flags = UserFlags(data.get("public_flags", 0))
        self.accent_color = data.get("accent_color", 0)
        self.premium_type = data.get("premium_type", 0)
        self.system = data.get("system", False)
        self.locale = data.get("locale", "en-US")
        self.avatar = data.get("avatar")
        self.banner = data.get("banner")

    @property
    def default_avatar(self) -> int:
        r"""Returns the default avatar index for this user.

        This index integer is calculated on the basis of user's
        :attr:`.discriminator`. See :class:`DefaultAvatar` for
        more information.

        Returns
        -------
        :class:`builtins.int`
        """
        return int(self.discriminator) % DefaultAvatar.INDEX

    def default_avatar_url(self) -> str:
        r"""Returns the default avatar URL for this user.

        Note that default avatar is generated on the basis of
        discriminator and does not implies the user's actual
        avatar. Consider using :meth:`.avatar_url` method instead
        if you want to obtain user's actual avatar's URL.

        Unlike other URL generator methods, Default avatars do not support
        custom sizes and file extension is always PNG.

        Returns
        -------
        :class:`builtins.str`
        """
        return create_cdn_url(f"/embed/avatars/{self.default_avatar}", extension="png")

    def avatar_url(self, extension: str = None, size: int = None) -> str:
        r"""Returns the avatar URL for this user.

        If user has no custom avatar set, This returns the result
        of :meth:`.default_avatar_url`.

        The ``extension`` parameter only supports following extensions
        in the case of user avatars:

        - :attr:`ImageExtension.GIF`
        - :attr:`ImageExtension.PNG`
        - :attr:`ImageExtension.JPG`
        - :attr:`ImageExtension.JPEG`
        - :attr:`ImageExtension.WEBP`

        Parameters
        ----------
        extension: :class:`builtins.str`
            The extension to use in the URL. If not supplied, An ideal
            extension will be picked depending on whether user has static
            or animated avatar.
        size: :class:`builtins.int`
            The size to append to URL. Can be any power of 2 between
            64 and 4096.

        Raises
        ------
        ValueError
            Invalid extension or size was passed.
        """
        if self.avatar is None:
            return self.default_avatar_url()

        extension = "gif" if self.is_avatar_animated() else "png"
        return create_cdn_url(f"/avatars/{self.id}/{self.avatar}", extension=extension, size=size)

    def banner_url(self, extension: str = None, size: int = None) -> typing.Optional[str]:
        r"""Returns the banner URL for this user.

        If user has no custom banner set, ``None`` is returned.

        The ``extension`` parameter only supports following extensions
        in the case of user banners:

        - :attr:`ImageExtension.GIF`
        - :attr:`ImageExtension.PNG`
        - :attr:`ImageExtension.JPG`
        - :attr:`ImageExtension.JPEG`
        - :attr:`ImageExtension.WEBP`

        Parameters
        ----------
        extension: :class:`builtins.str`
            The extension to use in the URL. If not supplied, An ideal
            extension will be picked depending on whether user has static
            or animated banner.
        size: :class:`builtins.int`
            The size to append to URL. Can be any power of 2 between
            64 and 4096.

        Raises
        ------
        ValueError
            Invalid extension or size was passed.
        """
        if self.banner is None:
            return

        extension = "gif" if self.is_banner_animated() else "png"
        return create_cdn_url(f"/banners/{self.id}/{self.banner}", extension=extension, size=size)

    def is_avatar_animated(self) -> bool:
        r"""Indicates whether the user has animated avatar.

        Having no custom avatar set will also return ``False``.

        Returns
        -------
        :class:`builtins.bool`
        """
        if self.avatar is None:
            return False

        return self.avatar.startswith("a_")

    def is_banner_animated(self) -> bool:
        r"""Indicates whether the user has animated banner.

        Having no custom banner set will also return ``False``.

        Returns
        -------
        :class:`builtins.bool`
        """
        if self.banner is None:
            return False

        return self.banner.startswith("a_")


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

    async def edit(self, *, name: str = None, avatar: typing.Optional[bytes] = EMPTY) -> None:
        r"""Edits the client user.

        Parameters
        ----------
        name: :class:`builtins.int`
            The new name of user.
        avatar: typing.Optional[:class:`builtins.int`]
            The new avatar of user. ``None`` could be used to denote
            the removal of avatar.

        Raises
        ------
        HTTPBadRequest
            The request body is not valid.
        HTTPException
            The editing failed.
        """
        payload = {}

        if name is not None:
            payload["username"] = name
        if avatar is not EMPTY:
            if avatar is None:
                payload["avatar"] = None
            else:
                payload["avatar"] = get_image_data(avatar)

        if payload:
            data = await self._client._rest.edit_current_user(payload=payload)
            self._update_with_data(data)