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
from qord.models.guild_members import GuildMember
from qord._helpers import get_optional_snowflake, parse_iso_timestamp

import typing

if typing.TYPE_CHECKING:
    from qord.models.roles import Role
    from qord.models.channels import TextChannel, DMChannel
    from qord.models.guilds import Guild
    from datetime import datetime

    MessageableT = typing.Union[TextChannel, DMChannel]

class ChannelMention(BaseModel):
    """Represents a mention to a specific channel in a message's content.

    .. warning::
        Channels from other guilds can be mentioned in a message. As such you
        should not rely on resolving the mentioned channel from the parent message
        guild's cache. It is possible that the guild that the mention channel belongs
        to is not available to you mostly because the bot isn't the part of it.

    Attributes
    ----------
    message: :class:`Message`
        The message that the mention was done in.
    id: :class:`builtins.int`
        The ID of channel that was mentioned.
    guild_id: :class:`builtins.int`
        The ID of guild that the mentioned channel belonged to.
    type: :class:`builtins.int`
        The type of channel that was mentioned. See :class:`ChannelType` for
        possible values.
    name: :class:`builtins.str`
        The name of channel that was mentioned.
    """
    if typing.TYPE_CHECKING:
        message: Message
        id: int
        guild_id: int
        type: int
        name: str

    __slots__ = ("message", "_client", "id", "guild_id", "type", "name")

    def __init__(self, data: typing.Dict[str, typing.Any], message: Message) -> None:
        self.message = message
        self._client = message._client
        self._update_with_data(data)

    def _update_with_data(self, data: typing.Dict[str, typing.Any]) -> None:
        self.id = int(data["id"])
        self.guild_id = int(data["guild_id"])
        self.type = data["type"]
        self.name = data["name"]

class Attachment(BaseModel):
    """Represents an attachment that is attached to a message.

    Attributes
    ----------
    message: :class:`Message`
        The message associated to this attachment.
    filename: :class:`builtins.str`
        The name of file of attachment.
    description: Optional[:class:`builtins.str`]
        The description of attachment, If any.
    content_type: Optional[:class:`builtins.str`]
        The attachment's media type.
    size: :class:`builtins.int`
        The size of attachment; in bytes.
    url: :class:`builtins.str`
        The URL of this attachment.
    proxy_url: :class:`builtins.str`
        The proxy URL of this attachment.
    height: Optional[:class:`builtins.int`]
        The height of attachment, if the attachment is an image.
    width: Optional[:class:`builtins.int`]
        The width of attachment, if the attachment is an image.
    ephemeral: :class:`builtins.bool`
        Whether the attachment is part of ephemeral message.
    """
    if typing.TYPE_CHECKING:
        message: Message
        id: int
        filename: str
        size: int
        url: str
        proxy_url: str
        description: typing.Optional[str]
        content_type: typing.Optional[str]
        height: typing.Optional[int]
        width: typing.Optional[int]
        ephemeral: bool

    __slots__ = (
        "message",
        "_client",
        "id",
        "filename",
        "description",
        "content_type",
        "size",
        "url",
        "proxy_url",
        "height",
        "width",
        "ephemeral",
    )

    def __init__(self, data: typing.Dict[str, typing.Any], message: Message):
        self.message = message
        self._client = message._client
        self._update_with_data(data)

    def _update_with_data(self, data: typing.Dict[str, typing.Any]) -> None:
        self.id = int(data["id"])
        self.filename = data["filename"]
        self.description = data.get("description")
        self.content_type = data.get("content_type")
        self.size = data.get("size", 0)
        self.url = data.get("url") # type: ignore
        self.proxy_url = data.get("proxy_url") # type: ignore
        self.height = data.get("height")
        self.width = data.get("width")
        self.ephemeral = data.get("ephemeral", False)

class Message(BaseModel):
    """Represents a message generated in channels by users, bots and webhooks.

    Attributes
    ----------
    channel: Union[:class:`TextChannel`]
        The channel in which message was sent.
    id: :class:`builtins.int`
        The ID of this message.
    type: :class:`builtins.int`
        The type of this message.
    channel_id: :class:`builtins.int`
        The channel ID that the message was sent in.
    created_at: :class:`datetime.datetime`
        The time when this message was sent.
    tts: :class:`builtins.bool`
        Whether the message is a TTS message.
    mention_everyone: :class:`builtins.bool`
        Whether the @everyone role is mentioned in the message.
    pinned: :class:`builtins.bool`
        Whether the message is pinned.
    author: Union[:class:`User`, :class:`GuildMember`]
        The author of this message.

        .. note::
            This may not point to an actual user when the message is created
            by a webhook. If the :attr:`.webhook_id` is not ``None`` then the
            user would represent the ID, name and avatar of the webhook and
            would not represent an "actual" user.

    mentions: List[:class:`User`, :class:`GuildMember`]
        The list of mentions in this message.
    mentioned_roles: List[:class:`Role`]
        The list of roles mentioned in this message.
    mentioned_channels: List[:class:`ChannelMention`]
        The list of channels mentioned in this message.
    guild: Optional[:class:`Guild`]
        The guild that this message belongs to.
    content: Optional[:class:`builtins.str`]
        The content of this message.
    nonce: Optional[Union[:class:`builtins.int`, :class:`builtins.str`]]
        The nonce used for indicating whether the message was sent.
    edited_at: Optional[:class:`datetime.datetime`]
        The time when the message was last edited or ``None`` if never.
    guild_id: Optional[:class:`builtins.int`]
        The ID of guild that this message belongs to.
    webhook_id: Optional[:class:`builtins.int`]
        The ID of webhook that generated this message. Note that when
        this is present, the :attr:`.author` will be a "fake" :class:`User`
        object represeting ID, name and avatar of the webhook and would
        not point to a valid user.
    application_id: Optional[:class:`builtins.int`]
        The ID of application that generated this application only if the
        message is response to an interaction.
    attachments: List[:class:`Attachment`]
        The list of attachments attached to the message.
    """

    if typing.TYPE_CHECKING:
        channel: MessageableT
        id: int
        type: int
        channel_id: int
        created_at: datetime
        tts: bool
        mention_everyone: bool
        pinned: bool
        author: typing.Union[User, GuildMember]
        mentions: typing.List[typing.Union[User, GuildMember]]
        mentioned_roles: typing.List[Role]
        mentioned_role_ids: typing.List[int]
        mentioned_channels: typing.List[ChannelMention]
        attachments: typing.List[Attachment]
        guild: typing.Optional[Guild]
        content: typing.Optional[str]
        nonce: typing.Optional[typing.Union[str, int]]
        edited_at: typing.Optional[datetime]
        guild_id: typing.Optional[int]
        webhook_id: typing.Optional[int]
        application_id: typing.Optional[int]

    __slots__ = ("channel", "_client", "_cache", "_rest", "id", "type", "channel_id", "guild_id",
                "webhook_id", "application_id", "created_at", "guild", "content", "tts",
                "mention_everyone", "mentioned_role_ids", "mentioned_channels", "nonce",
                "pinned", "edited_at", "author", "mentions", "mentioned_roles", "attachments")

    def __init__(self, data: typing.Dict[str, typing.Any], channel: MessageableT) -> None:
        self.channel = channel
        self._client = channel._client
        self._rest = channel._rest
        self._cache = self._client._cache
        self._update_with_data(data)

    def _update_with_data(self, data: typing.Dict[str, typing.Any]) -> None:
        # TODO: Following fields are not supported yet:
        # - embeds
        # - reactions
        # - activity
        # - application
        # - flags
        # - message_reference
        # - referenced_message
        # - interaction
        # - thread
        # - components
        # - sticker_items

        self.id = int(data["id"])
        self.type = data["type"]
        self.channel_id = int(data["channel_id"])
        self.guild_id = guild_id = get_optional_snowflake(data, "guild_id")
        self.webhook_id = get_optional_snowflake(data, "webhook_id")
        self.application_id = get_optional_snowflake(data, "application_id")
        self.created_at = parse_iso_timestamp(data["timestamp"])
        self.guild = self._cache.get_guild(guild_id) if guild_id is not None else None
        self.content = data.get("content")
        self.tts = data.get("tts", False)
        self.mention_everyone = data.get("mention_everyone", False)
        self.mentioned_role_ids = [int(r) for r in data.get("mention_roles", [])] # Undocumented.
        self.mentioned_channels = [ChannelMention(c, self) for c in data.get("mention_channels", [])]
        self.nonce = data.get("nonce")
        self.pinned = data.get("pinned", False)
        self.attachments = [Attachment(a, message=self) for a in data.get("attachments", [])]
        edited_at = data.get("edited_timestamp")
        self.edited_at = parse_iso_timestamp(edited_at) if edited_at is not None else None

        self._handle_author(data)
        self._handle_mentions(data)
        self._handle_mention_roles(data)

    # Data handlers (to avoid making mess in the initialization code)

    def _handle_mentions(self, data) -> None:
        guild = self.guild
        mentions = []

        for user_data in data.get("mentions", []):
            user_id = int(user_data["id"])
            if "member" in user_data:
                try:
                    member = guild._cache.get_member(user_id)
                except AttributeError:
                    # No guild present for some reason.
                    pass
                else:
                    if member is None:
                        member_data = user_data["member"]
                        member_data["user"] = user_data
                        member = GuildMember(member_data, guild=guild) # type: ignore

                    mentions.append(member)
                    continue

            user = self._cache.get_user(user_id)
            if user is None:
                user = User(user_data, client=self._client)
            mentions.append(user)

        self.mentions = mentions

    def _handle_author(self, data) -> None:
        guild = self.guild
        author = data["author"]

        if guild is not None:
            try:
                member_data = data["member"]
            except KeyError:
                self.author = User(author, client=self._client)
            else:
                # The "user" will always be an actual here user.
                user_id = int(author["id"])
                member = guild._cache.get_member(user_id)

                if member is None:
                    member_data["user"] = author
                    self.author = GuildMember(member_data, guild=guild)
                else:
                    self.author = member
        else:
            self.author = User(author, client=self._client)

    def _handle_mention_roles(self, data) -> None:
        guild = self.guild

        if guild is None:
            return

        mentioned_roles = []

        for role_id in self.mentioned_role_ids:
            role = guild._cache.get_role(role_id) # type: ignore
            if role is not None:
                mentioned_roles.append(role)

        self.mentioned_roles = mentioned_roles

    async def delete(self) -> None:
        """Deletes this message.

        Raises
        ------
        HTTPNotFound
            Message is already deleted.
        HTTPForbidden
            You don't have permission to do this.
        HTTPException
            The operation failed.
        """
        await self._rest.delete_message(channel_id=self.channel_id, message_id=self.id)

