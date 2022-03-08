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

from qord._helpers import parse_iso_timestamp
from datetime import datetime
import dataclasses
import typing


class Embed:
    """Represents a message embed.

    This class is mainly for facilitating the creation of rich embeds for
    sending in bot or webhook messages.

    This class is also returned in several API responses like :attr:`Message.embeds`.
    Due to this reason, Some fields on the class are not able to be set by bots.
    These fields are generally returned for embeds from API that are created by
    external resources. You should not be setting those fields manually.

    Parameters
    ----------
    url: :class:`builtins.str`
        The URL of this embed this is hypedlinked in embed's title.
    title: :class:`builtins.str`
        The title of the embed.
    color: :class:`builtins.int`
        The integer representation of color of this embed.
    description: :class:`builtins.str`
        The description of the embed.
    timestamp: :class:`datetime`
        The datetime representation of timestamp that is shown in footer
        of the embed.
    author: :class:`EmbedAuthor`
        The author of this embed.
    image: :class:`EmbedImage`
        The image of this embed.
    thumbnail: :class:`EmbedThumbnail`
        The thumbnail of this embed.
    footer: :class:`EmbedFooter`
        The footer of this embed.
    """

    def __init__(
        self,
        *,
        url: str = None,
        title: str = None,
        color: int = None,
        description: str = None,
        timestamp: datetime = None,
        author: EmbedAuthor = None,
        image: EmbedImage = None,
        thumbnail: EmbedThumbnail = None,
        footer: EmbedFooter = None,
    ):
        self.url = url
        self.title = title
        self.color = color
        self.timestamp = timestamp
        self.description = description

        self._thumbnail = thumbnail
        self._footer = footer
        self._author = author
        self._image  = image
        self._fields = []

        # Non-customisable fields
        self._provider = None
        self._video = None

    @property
    def provider(self) -> typing.Optional[EmbedProvider]:
        """The provider of embed if any.

        This property cannot be set manually as it is not available
        for bots and webhooks to set.

        Returns
        -------
        Optional[:class:`EmbedProvider`]
        """
        return self._provider

    @property
    def video(self) -> typing.Optional[EmbedVideo]:
        """The video of embed if any.

        This property cannot be set manually as it is not available
        for bots and webhooks to set.

        Returns
        -------
        Optional[:class:`EmbedVideo`]
        """
        return self.video

    @property
    def thumbnail(self) -> typing.Optional[EmbedThumbnail]:
        """The thumbnail of embed if any.

        This property can be set a value of :class:`EmbedThumbnail` manually.
        Setting the value to ``None`` will remove it.

        Returns
        -------
        Optional[:class:`EmbedThumbnail`]
        """
        return self._thumbnail

    @thumbnail.setter
    def thumbnail(self, new: EmbedThumbnail) -> None:
        if not isinstance(new, EmbedThumbnail):
            raise TypeError("Embed.thumbnail must be an instance of EmbedThumbnail")

        self._thumbnail = new

    @property
    def image(self) -> typing.Optional[EmbedImage]:
        """The image of embed if any.

        This property can be set a value of :class:`EmbedImage` manually.
        Setting the value to ``None`` will remove it.

        Returns
        -------
        Optional[:class:`EmbedImage`]
        """
        return self._image

    @image.setter
    def image(self, new: EmbedImage) -> None:
        if not isinstance(new, EmbedImage):
            raise TypeError("Embed.image must be an instance of EmbedImage")

        self._image = new

    @property
    def footer(self) -> typing.Optional[EmbedFooter]:
        """The footer of embed if any.

        This property can be set a value of :class:`EmbedFooter` manually.
        Setting the value to ``None`` will remove it.

        Returns
        -------
        Optional[:class:`EmbedFooter`]
        """
        return self._footer

    @footer.setter
    def footer(self, new: EmbedFooter) -> None:
        if not isinstance(new, EmbedFooter):
            raise TypeError("Embed.footer must be an instance of EmbedFooter")

        self._footer = new

    @property
    def author(self) -> typing.Optional[EmbedAuthor]:
        """The author of embed if any.

        This property can be set a value of :class:`EmbedAuthor` manually.
        Setting the value to ``None`` will remove it.

        Returns
        -------
        Optional[:class:`EmbedFooter`]
        """
        return self._author

    @author.setter
    def author(self, new: EmbedAuthor) -> None:
        if not isinstance(new, EmbedAuthor):
            raise TypeError("Embed.author must be an instance of EmbedAuthor")

        self._author = new

    @property
    def fields(self) -> typing.List[EmbedField]:
        """The list of fields present on the embed.

        Returns
        -------
        List[:class:`EmbedField`]
        """
        return self._fields.copy()

    def set_field(
        self,
        *,
        name: str,
        value: str,
        inline: bool = False,
        index: int = None,
    ) -> EmbedField:
        """Sets a field on the embed at provided position.

        This method by default adds the field to the last of current field
        however ``index`` parameter can be passed to provide an explicit index
        for the field where it should be inserted.

        Parameters
        ----------
        name: :class:`builtins.str`
            The :attr:`~EmbedField.name` of field.
        value: :class:`builtins.str`
            The :attr:`~EmbedField.value` of field.
        inline: :class:`builtins.bool`
            Whether the field should be :attr:`~EmbedField.inline` with last
            field of embed. Defaults to ``True``.
        index: :class:`builtins.int`
            The index where the field should be inserted. When not
            supplied, The field is appended.

        Returns
        -------
        :class:`EmbedField`
            The field that was created.
        """
        field = EmbedField(name=name, value=value, inline=inline)

        if index is None:
            self._fields.append(field)
        else:
            self._fields.insert(index, field)

        return field

    def pop_field(self, index: int = None) -> typing.Optional[EmbedField]:
        """Removes a field from the provided position (last by default).

        Parameters
        ----------
        index: :class:`builtins.int`
            The index of field to remove. When not supplied, Removes the
            last field.

        Returns
        -------
        Optional[:class:`EmbedField`]
            The removed field. If no field existed on provided
            index, ``None`` is returned
        """
        try:
            if index is None:
                return self._fields.pop()
            else:
                return self._fields.pop(index)
        except IndexError:
            return None

    def clear_fields(self) -> None:
        """Clears the fields that are currently present on the embed."""
        self._fields.clear()

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        ret = {}

        if self.url is not None:
            ret["url"] = self.url

        if self.title is not None:
            ret["title"] = self.title

        if self.color is not None:
            ret["color"] = self.color

        if self.timestamp is not None:
            ret["timestamp"] = self.timestamp.isoformat()

        if self.description is not None:
            ret["description"] = self.description

        if self._author is not None:
            ret["author"] = self._author.to_dict()

        if self._footer is not None:
            ret["footer"] = self._footer.to_dict()

        if self._image is not None:
            ret["image"] = self._image.to_dict()

        if self._thumbnail is not None:
            ret["thumbnail"] = self._thumbnail.to_dict()

        ret["fields"] = [f.to_dict() for f in self._fields]
        return ret

    @classmethod
    def from_dict(cls, data: typing.Dict[str, typing.Any]) -> Embed:
        ts = data.get("timestamp")
        embed = cls(
            title=data.get("title"),
            description=data.get("description"),
            timestamp=parse_iso_timestamp(ts) if ts is not None else None,
            color=data.get("color"),
            url=data.get("url"),
        )

        if author := data.get("author"):
            embed._author = EmbedAuthor.from_dict(author)

        if footer := data.get("footer"):
            embed._footer = EmbedFooter.from_dict(footer)

        if provider := data.get("provider"):
            embed._provider = EmbedProvider.from_dict(provider)

        if image := data.get("image"):
            embed._image = EmbedImage.from_dict(image)

        if thumbnail := data.get("thumbnail"):
            embed._thumbnail = EmbedThumbnail.from_dict(thumbnail)

        if video := data.get("video"):
            embed._video = EmbedVideo.from_dict(video)

        embed._fields = [EmbedField.from_dict(f) for f in data.get("fields", [])]
        return embed

###############
# Embed items #
###############

class _EmbedItem:
    def to_dict(self) -> typing.Dict[str, typing.Any]:
        raise NotImplementedError

    @classmethod
    def from_dict(cls, data: typing.Dict[str, typing.Any]) -> _EmbedItem:
        raise NotImplementedError


@dataclasses.dataclass()
class EmbedField(_EmbedItem):
    """A data class representing an embed's field."""

    name: str
    """The name of field."""

    value: str
    """The value of field."""

    inline: bool = True
    """Whether the field lines with the last field on the embed, Defaults to ``True``."""

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        return {
            "name": self.name,
            "value": self.value,
            "inline": self.inline,
        }

    @classmethod
    def from_dict(cls, data: typing.Dict[str, typing.Any]) -> _EmbedItem:
        return cls(
            name=data["name"],
            value=data["value"],
            inline=data.get("inline", True)
        )

@dataclasses.dataclass()
class EmbedImage(_EmbedItem):
    """A data class representing an embed's :attr:`~Embed.image`."""

    url: str
    """The URL of the image."""

    proxy_url: typing.Optional[str] = None
    """The proxy URL of the image.

    |embed-restricted-field|
    """

    height: typing.Optional[int] = None
    """The height of the image.

    |embed-restricted-field|
    """

    width: typing.Optional[int] = None
    """The width of the image.

    |embed-restricted-field|
    """

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        return {
            "url": self.url,
        }

    @classmethod
    def from_dict(cls, data: typing.Dict[str, typing.Any]) -> _EmbedItem:
        return cls(
            url=data["url"],
            proxy_url=data.get("proxy_url"),
            height=data.get("height"),
            width=data.get("width"),
        )

@dataclasses.dataclass()
class EmbedThumbnail(_EmbedItem):
    """A data class representing an embed's :attr:`~Embed.thumbnail`."""

    url: str
    """The URL of the thumbnail image."""

    proxy_url: typing.Optional[str] = None
    """The proxy URL of the thumbnail image.

    |embed-restricted-field|
    """

    height: typing.Optional[int] = None
    """The height of the thumbnail.

    |embed-restricted-field|
    """

    width: typing.Optional[int] = None
    """The width of the thumbnail.

    |embed-restricted-field|
    """

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        return {
            "url": self.url,
        }

    @classmethod
    def from_dict(cls, data: typing.Dict[str, typing.Any]) -> _EmbedItem:
        return cls(
            url=data["url"],
            proxy_url=data.get("proxy_url"),
            height=data.get("height"),
            width=data.get("width"),
        )

@dataclasses.dataclass()
class EmbedVideo(_EmbedItem):
    """A data class representing an embed's :attr:`~Embed.video`.

    Embed videos are only returned by embeds from API responses that are
    created by external sources. Videos cannot be set by bots or webhooks.
    As such, this class is not meant to be instansiated manually.
    """

    url: str
    """The URL of video."""

    proxy_url: typing.Optional[str] = None
    """The proxy URL of the video."""

    height: typing.Optional[int] = None
    """The height of the video."""

    width: typing.Optional[int] = None
    """The width of the video."""

    @classmethod
    def from_dict(cls, data: typing.Dict[str, typing.Any]) -> _EmbedItem:
        return cls(
            url=data["url"],
            proxy_url=data.get("proxy_url"),
            height=data.get("height"),
            width=data.get("width"),
        )

@dataclasses.dataclass()
class EmbedProvider(_EmbedItem):
    """A data class representing an embed's :attr:`~Embed.provider`.

    Embed providers are only returned by embeds from API responses that are
    created by external sources. Provider cannot be set by bots or webhooks.
    As such, this class is not meant to be instansiated manually.
    """

    name: typing.Optional[str] = None
    """The name of provider."""

    url: typing.Optional[str] = None
    """The URL of provider."""

    @classmethod
    def from_dict(cls, data: typing.Dict[str, typing.Any]) -> _EmbedItem:
        return cls(
            name=data.get("name"),
            url=data.get("url"),
        )

@dataclasses.dataclass()
class EmbedAuthor(_EmbedItem):
    """A data class representing an embed's :attr:`~Embed.author`."""

    name: str
    """The name of author."""

    url: typing.Optional[str] = None
    """The URL of author."""

    icon_url: typing.Optional[str] = None
    """The URL of icon shown on author."""

    proxy_icon_url: typing.Optional[str] = None
    """The proxy URL of the author icon.

    |embed-restricted-field|
    """

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        return {
            "name": self.name,
            "url": self.url,
            "icon_url": self.icon_url,
        }

    @classmethod
    def from_dict(cls, data: typing.Dict[str, typing.Any]) -> _EmbedItem:
        return cls(
            name=data["name"],
            url=data.get("url"),
            icon_url=data.get("icon_url"),
            proxy_icon_url=data.get("proxy_icon_url"),
        )

@dataclasses.dataclass()
class EmbedFooter(_EmbedItem):
    """A data class representing an embed's :attr:`~Embed.footer`."""

    text: typing.Optional[str] = None
    """The name of author."""

    icon_url: typing.Optional[str] = None
    """The URL of icon shown on footers."""

    proxy_icon_url: typing.Optional[str] = None
    """The proxy URL of the footer icon.

    |embed-restricted-field|
    """

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        return {
            "text": self.text,
            "icon_url": self.icon_url,
        }

    @classmethod
    def from_dict(cls, data: typing.Dict[str, typing.Any]) -> _EmbedItem:
        return cls(
            text=data["text"],
            icon_url=data.get("icon_url"),
            proxy_icon_url=data.get("proxy_icon_url"),
        )
