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
from qord.flags.messages import MessageFlags
from qord.dataclasses.embeds import Embed
from qord.dataclasses.message_reference import MessageReference
from qord.enums import MessageType
from qord.internal.helpers import get_optional_snowflake, parse_iso_timestamp
from qord.internal.undefined import UNDEFINED

import typing

if typing.TYPE_CHECKING:
    from qord.models.roles import Role
    from qord.models.channels import TextChannel, DMChannel
    from qord.models.guilds import Guild
    from qord.dataclasses.allowed_mentions import AllowedMentions
    from qord.dataclasses.files import File
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
        The type of this message. See :class:`MessageType` for possible values.
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
    embeds: List[:class:`Embed`]
        The list of embeds attached to the message.
    flags: :class:`MessageFlags`
        The flags of this message.
    message_reference: Optional[:class:`MessageReference`]
        The referenced message if any, See the :class:`MessageReference` documentation
        for the list of scenarios when this attribute is not ``None``.
    referenced_message: Optional[:class:`Message`]
        The referenced message. This is only valid when :attr:`.type` is either
        :attr:`~MessageType.REPLY` or :attr:`~MessageType.THREAD_STARTER_MESSAGE`.

        For thread starter messages, This is always present. For replies however, If
        this is None, It indicates that either the message was deleted or wasn't sent
        loaded by Discord API.
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
        flags: MessageFlags
        message_reference: typing.Optional[MessageReference]
        referenced_message: typing.Optional[Message]
        author: typing.Union[User, GuildMember]
        mentions: typing.List[typing.Union[User, GuildMember]]
        mentioned_roles: typing.List[Role]
        mentioned_role_ids: typing.List[int]
        mentioned_channels: typing.List[ChannelMention]
        attachments: typing.List[Attachment]
        embeds: typing.List[Embed]
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
                "pinned", "edited_at", "author", "mentions", "mentioned_roles", "attachments",
                "embeds", "flags", "message_reference", "referenced_message")

    def __init__(self, data: typing.Dict[str, typing.Any], channel: MessageableT) -> None:
        self.channel = channel
        self._client = channel._client
        self._rest = channel._rest
        self._cache = self._client._cache
        self._update_with_data(data)

    def _update_with_data(self, data: typing.Dict[str, typing.Any]) -> None:
        # TODO: Following fields are not supported yet:
        # - reactions
        # - activity
        # - application
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
        self.flags = MessageFlags(data.get("message_flags", 0))
        self.mention_everyone = data.get("mention_everyone", False)
        self.mentioned_role_ids = [int(r) for r in data.get("mention_roles", [])] # Undocumented.
        self.mentioned_channels = [ChannelMention(c, self) for c in data.get("mention_channels", [])]
        self.nonce = data.get("nonce")
        self.pinned = data.get("pinned", False)
        self.attachments = [Attachment(a, message=self) for a in data.get("attachments", [])]
        self.embeds = [Embed.from_dict(e) for e in data.get("embeds", [])]
        edited_at = data.get("edited_timestamp")
        message_reference = data.get("message_reference")
        self.edited_at = parse_iso_timestamp(edited_at) if edited_at is not None else None
        self.message_reference = MessageReference.from_dict(message_reference) if message_reference is not None else None

        self._handle_author(data)
        self._handle_mentions(data)
        self._handle_mention_roles(data)
        self._handle_referenced_message(data)

    # Data handlers (to avoid making mess in the initialization code)

    def _handle_mentions(self, data) -> None:
        guild = self.guild
        mentions = []

        for user_data in data.get("mentions", []):
            user_id = int(user_data["id"])
            if "member" in user_data:
                # Mention is in a guild

                if guild is None:
                    continue

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

    def _handle_referenced_message(self, data) -> None:
        if not self.type in (MessageType.THREAD_STARTER_MESSAGE, MessageType.REPLY):
            return

        try:
            referenced_message_data = data["referenced_message"]
        except KeyError:
            # If the key is absent on message reply, it indicates that the
            # message was not attempted to be fetched by API.
            self.referenced_message = None
            return
        else:
            if referenced_message_data is None:
                # Replied message deleted.
                self.referenced_message = None
                return

        if self.type is MessageType.REPLY:
            # For replies, the channel is always same as message channel
            channel = self.channel
        else:
            # In case of threads, the channel is never other than a guild channel.
            guild = self.guild

            if guild is None:
                channel = None
            else:
                channel_id = int(referenced_message_data["channel_id"]) # Always present
                channel = guild._cache.get_channel(channel_id)

        if channel is None:
            self.referenced_message = None
            return

        self.referenced_message = self.__class__(referenced_message_data, channel=channel) # type: ignore


    async def delete(self) -> None:
        """Deletes this message.

        To delete other's messages, the :attr:`~Permissions.manage_messages`
        permission is required in the target channel.

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

    async def reply(self, *args, fail_if_not_exists: bool = True, **kwargs) -> Message:
        """Replies to this message.

        This is an equivalent to :meth:`~BaseMessageChannel.send` that handles
        the instansiation of message reference. All parameters except
        ``message_reference`` that are passed in :meth:`~BaseMessageChannel.send`
        are valid in this method too. Additional parameters are documented below:

        Parameters
        ----------
        *args:
            The positional arguments of :meth:`~BaseMessageChannel.send`.
        fail_if_not_exists: :class:`builtins.bool`
            Whether to throw :exc:`HTTPException` if the replied message
            does not exist. If set to ``False``, If the message is deleted, A
            a default non-reply message would be sent.
        **kwargs:
            The keyword arguments of :meth:`~BaseMessageChannel.send`.

        Returns
        -------
        :class:`Message`
            The sent message.
        """
        if kwargs.pop("message_reference", None):
            raise TypeError("Message.reply() does not support message_reference parameter.")

        message_reference = MessageReference.from_message(self, fail_if_not_exists=fail_if_not_exists)
        return (await self.channel.send(*args, message_reference=message_reference, **kwargs))

    async def edit(
        self,
        content: str = UNDEFINED,
        *,
        embed: Embed = UNDEFINED,
        file: File = UNDEFINED,
        flags: MessageFlags = UNDEFINED,
        allowed_mentions: AllowedMentions = UNDEFINED,
        embeds: typing.List[Embed] = UNDEFINED,
        files: typing.List[File] = UNDEFINED,
    ):
        """Edits the message.

        Bots can only modify the ``flags`` of other author's messages. All
        other fields can only be edited if bot is the message's author.

        When successful the message is updated in-place.

        Parameters
        ----------
        content: :class:`builtins.str`
            The new content of message. It is worth noting that the mentions
            in this content will not respect the allowed mentions properties
            that were set during sending of message. A new :class:`AllowedMentions`
            must be supplied for new content.
        allowed_mentions: :class:`AllowedMentions`
            The mentions to allow in the message's new content.
        flags: :class:`MessageFlags`
            The message flags for the edited message. Bots can only
            apply or remove the :attr:`~MessageFlags.suppress_embeds` flag.
            Other flags are unsupported. This is the only field that can be
            set or unset by bots on other user's messages.
        embed: :class:`Embed`
            The embed to include in message, cannot be mixed with ``embeds``.
        embeds: List[:class:`Embed`]
            The list of embeds to include in the message, cannot be mixed with ``embed``.
        file: :class:`File`
            The file to include in message, cannot be mixed with ``files``.
        files: List[:class:`File`]
            The list of file attachments to include in message, cannot be mixed with ``file``.

        Raises
        ------
        TypeError
            Invalid arguments passed.
        HTTPForbidden
            You are not allowed to send message in this channel.
        HTTPBadRequest
            The message has invalid data.
        HTTPException
            The editing failed for some reason.
        """
        if embed is not UNDEFINED and embeds is UNDEFINED:
            raise TypeError("embed and embeds parameters cannot be mixed.")

        if file is not UNDEFINED and files is not UNDEFINED:
            raise TypeError("file and files parameters cannot be mixed.")

        json = {}

        if content is not UNDEFINED:
            json["content"] = content

        if flags is not UNDEFINED:
            json["flags"] = flags.value

        if allowed_mentions is not UNDEFINED:
            json["allowed_mentions"] = allowed_mentions.to_dict()

        if file is not UNDEFINED:
            files = [file]

        if embed is not UNDEFINED:
            if embed is None:
                json["embeds"] = []
            else:
                json["embeds"] = [embed.to_dict()]

        if embeds is not UNDEFINED:
            if embeds is None:
                json["embeds"] = []
            else:
                json["embeds"] = [embed.to_dict() for embed in embeds]

        data = await self._rest.edit_message(
                channel_id=self.channel_id,
                message_id=self.id,
                json=json,
                files=files,
            )
        self._update_with_data(data)
