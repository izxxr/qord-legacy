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
from qord.models.users import User
from qord.internal.undefined import UNDEFINED
from qord.internal.helpers import (
    create_cdn_url,
    get_optional_snowflake,
    parse_iso_timestamp,
    BASIC_STATIC_EXTS,
)

import typing

if typing.TYPE_CHECKING:
    from datetime import datetime
    from qord.models.channels import VoiceChannel, StageChannel
    from qord.models.guilds import Guild


__all__ = (
    "ScheduledEvent",
)


class ScheduledEvent(BaseModel):
    """Represents a guild scheduled event.

    Attributes
    ----------
    guild: :class:`Guild`
        The guild that belongs to this scheduled event.
    id: :class:`builtins.int`
        The ID of this scheduled event.
    guild_id: :class:`builtins.int`
        The ID of guild that the event belongs to.
    name: :class:`builtins.str`
        The name of event.
    privacy_level: :class:`builtins.int`
        The privacy level of this event. All possible values are detailed in :class:`EventPrivacyLevel`.
    status: :class:`builtins.int`
        The current status of this event. All possible values are detailed in :class:`EventStatus`.
    entity_type: :class:`builtins.int`
        The type of entity that belongs to this event. All possible values are detailed in :class:`EventEntityType`.
    subscribers_count: Optional[:class:`builtins.int`]
        The number of users subscribed to this event.
    description: Optional[:class:`builtins.str`]
        The description of event, if any.
    starts_at: :class:`datetime.datetime`
        The time when the event starts.
    ends_at: Optional[:class:`datetime.datetime`]
        The time when the event ends. This can be ``None``.
    channel_id: Optional[:class:`builtins.int`]
        The ID of voice or stage channel in which the event is being
        hosted, This is always ``None`` when :attr:`.entity_type` is :attr:`~EventEntityType.EXTERNAL`.
    creator_id: Optional[:class:`builtins.int`]
        The ID of user who created the event. For events created before 25 October 2021, This is ``None``.
    entity_id: Optional[:class:`builtins.int`]
        The ID of entity (stage instance) that is hosting the event.
    creator: Optional[:class:`User`]
        The user who created the event. For events created before 25 October 2021, This is ``None``.
    location: Optional[:class:`builtins.str`]
        The location where the event is hosted. This is only present when :attr:`.entity_type` is :attr:`~EventEntityType.EXTERNAL`.
    cover_image: Optional[:class:`builtins.str`]
        The cover image's hash for the event, if any.
    """

    if typing.TYPE_CHECKING:
        id: int
        guild_id: int
        name: str
        privacy_level: int
        status: int
        entity_type: int
        starts_at: datetime
        subscribers_count: typing.Optional[int]
        channel_id: typing.Optional[int]
        creator_id: typing.Optional[int]
        entity_id: typing.Optional[int]
        description: typing.Optional[str]
        ends_at: typing.Optional[datetime]
        location: typing.Optional[str]
        creator: typing.Optional[User]
        cover_image: typing.Optional[str]

    __slots__ = (
        "guild",
        "_client",
        "id",
        "guild_id",
        "channel_id",
        "creator_id",
        "entity_id",
        "name",
        "description",
        "privacy_level",
        "status",
        "entity_type",
        "starts_at",
        "subscribers_count",
        "creator",
        "cover_image",
        "location",
        "ends_at",
    )

    def __init__(self, data: typing.Dict[str, typing.Any], guild: Guild) -> None:
        self.guild = guild
        self._client = guild._client
        self._update_with_data(data)

    def _update_with_data(self, data: typing.Dict[str, typing.Any]) -> None:
        self.id = int(data["id"])
        self.guild_id = int(data["guild_id"])
        self.channel_id = get_optional_snowflake(data, "channel_id")
        self.creator_id = get_optional_snowflake(data, "creator_id")
        self.entity_id = get_optional_snowflake(data, "entity_id")
        self.name = data.get("name", "")
        self.description = data.get("description")
        self.privacy_level = data.get("privacy_level", 2)
        self.status = data.get("status", 1)
        self.entity_type = data.get("entity_type", 1)
        self.cover_image = data.get("image")
        self.subscribers_count = data.get("user_count")
        self.starts_at = parse_iso_timestamp(data["scheduled_start_time"])
        ends_at = data.get("ends_at")
        self.ends_at = parse_iso_timestamp(ends_at) if ends_at else None

        try:
            self.creator = User(data["creator"], client=self._client)
        except KeyError:
            self.creator = None

        self._apply_entity_metadata(data)

    def _apply_entity_metadata(self, data: typing.Dict[str, typing.Any]) -> None:
        metadata = data.get("entity_metadata") or {}
        self.location = metadata.get("location")

    @property
    def channel(self) -> typing.Optional[typing.Union[VoiceChannel, StageChannel]]:
        """The channel in which event is hosted.

        Returns
        -------
        Optional[Union[:class:`VoiceChannel`, :class:`StageChannel`]]
        """
        channel_id = self.channel_id

        if channel_id is None:
            return None

        # This will always return VoiceChannel or StageChannel
        return self.guild.cache.get_channel(channel_id)  # type: ignore

    def cover_image_url(self, extension: str = UNDEFINED, size: int = UNDEFINED) -> typing.Optional[str]:
        """Returns the cover image's URL for this event.

        If event has no cover image set, This method would return ``None``.

        The ``extension`` parameter only supports following extensions
        in the case of event cover images:

        - :attr:`ImageExtension.PNG`
        - :attr:`ImageExtension.JPG`
        - :attr:`ImageExtension.JPEG`
        - :attr:`ImageExtension.WEBP`

        Parameters
        ----------
        extension: :class:`builtins.str`
            The extension to use in the URL. If not supplied, Defaults
            to :attr:`~ImageExtension.PNG`.
        size: :class:`builtins.int`
            The size to append to URL. Can be any power of 2 between
            64 and 4096.

        Raises
        ------
        ValueError
            Invalid extension or size was passed.
        """
        cover_image = self.cover_image

        if cover_image is None:
            return None

        if extension is UNDEFINED:
            extension = "png"

        return create_cdn_url(
            f"/guild-events/{self.id}/{cover_image}",
            extension=extension,
            size=size,
            valid_exts=BASIC_STATIC_EXTS,
        )
