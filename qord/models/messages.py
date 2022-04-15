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
from qord.models.emojis import PartialEmoji, Emoji
from qord.flags.messages import MessageFlags
from qord.dataclasses.embeds import Embed
from qord.dataclasses.message_reference import MessageReference
from qord.enums import MessageType
from qord.internal.helpers import compute_snowflake, get_optional_snowflake, parse_iso_timestamp
from qord.internal.undefined import UNDEFINED
from qord.internal.mixins import Comparable, CreationTime

from datetime import datetime
import typing

if typing.TYPE_CHECKING:
    from qord.models.roles import Role
    from qord.models.channels import TextChannel, DMChannel
    from qord.models.guilds import Guild
    from qord.dataclasses.allowed_mentions import AllowedMentions
    from qord.dataclasses.files import File

    MessageableT = typing.Union[TextChannel, DMChannel]


__all__ = (
    "ChannelMention",
    "Reaction",
    "Attachment",
    "Message",
)


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


class Reaction(BaseModel):
    """Represents a reaction on a :class:`Message`.

    Attributes
    ----------
    message: :class:`Message`
        The message that this reaction belongs to.
    count: :class:`builtins.int`
        The count of this reaction.
    emoji: :class:`PartialEmoji`
        The emoji for this reaction.
    me: :class:`builtins.bool`
        Whether the reaction is added by the bot user.
    """

    if typing.TYPE_CHECKING:
        message: Message
        emoji: PartialEmoji
        count: int
        me: bool

    __slots__ = (
        "_client",
        "message",
        "emoji",
        "count",
        "me",
    )

    def __init__(self, data: typing.Dict[str, typing.Any], message: Message) -> None:
        self.message = message
        self._client = message._client
        self._update_with_data(data)

    def _update_with_data(self, data: typing.Dict[str, typing.Any]) -> None:
        self.emoji = PartialEmoji(data["emoji"], client=self._client)
        self.count = data.get("count", 1)
        self.me = data.get("me", False)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(count={self.count}, me={self.me}, emoji={self.emoji!r})"

    async def users(self, *, limit: typing.Optional[int] = None, after: int = UNDEFINED) -> typing.AsyncIterator[typing.Union[GuildMember, User]]:
        """Asynchronous Iterator for fetching the users who have reacted to this reaction.

        Parameters
        ----------
        limit: Optional[:class:`builtins.int`]
            The number of users to fetch. When not provided, all users are fetched.
        after: Union[:class:`builtins.int`, :class:`datetime.datetime`]
            For pagination, If an ID is given, Fetch the user after that user ID.
            If a datetime object is given, Fetch the user created after that time.

        Yields
        ------
        Union[:class:`GuildMember`, :class:`User`]
            The users that reacted with this reaction. When member intents are present
            and reaction is in a guild, :class:`GuildMember` is returned. In some cases,
            such as when member has left the guild or member isn't cached, the :class:`User`
            is yielded.
        """

        limit = limit or self.count
        getter = self.message._rest.get_reaction_users
        message_id = self.message.id
        channel_id = self.message.channel_id
        guild = self.message.guild
        emoji = _get_reaction_emoji(self)

        if isinstance(after, datetime):
            after = compute_snowflake(after)

        while limit > 0:
            current_limit = min(limit, 100)

            data = await getter(
                channel_id=channel_id,
                message_id=message_id,
                emoji=emoji,
                after=after,
                limit=current_limit,
            )

            limit -= len(data)

            if data:
                after = int(data[-1]["id"])

            for user_payload in data:
                user = None
                user_id = int(user_payload["id"])

                if guild:
                    user = guild.cache.get_member(user_id)

                if user is None:
                    user = User(user_payload, client=self._client)

                yield user


def _get_reaction_emoji(emoji_or_reaction: typing.Union[Reaction, PartialEmoji, Emoji, str]) -> str:
    if isinstance(emoji_or_reaction, str):
        ret = emoji_or_reaction
    elif isinstance(emoji_or_reaction, (PartialEmoji, Emoji)):
        ret = emoji_or_reaction.mention
    elif isinstance(emoji_or_reaction, Reaction):
        ret = emoji_or_reaction.emoji.mention
    else:
        raise TypeError("Expected emoji to be an instance of Emoji, PartialEmoji, Reaction or str. Got %r"
                        % emoji_or_reaction.__class__)

    # <a:name:12345> -> name:12345
    # <:name:12345> -> name:12345
    # has no effect on unicode emoji
    return ret.strip("<a:>")

class Attachment(BaseModel, Comparable, CreationTime):
    """Represents an attachment that is attached to a message.

    |supports-comparison|

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

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, filename={self.filename!r}, url={self.url!r})"


class Message(BaseModel, Comparable):
    """Represents a message generated in channels by users, bots and webhooks.

    |supports-comparison|

    Attributes
    ----------
    channel: Union[:class:`TextChannel`, :class:`DMChannel`]
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
    reactions: List[:class:`Reaction`]
        The list of reactions on this message.
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
        reactions: typing.List[Reaction]
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
                "embeds", "flags", "message_reference", "referenced_message", "reactions")

    def __init__(self, data: typing.Dict[str, typing.Any], channel: MessageableT) -> None:
        self.channel = channel
        self._client = channel._client
        self._rest = channel._rest
        self._cache = self._client._cache
        self._update_with_data(data)

    def _update_with_data(self, data: typing.Dict[str, typing.Any]) -> None:
        # TODO: Following fields are not supported yet:
        # - activity
        # - application
        # - interaction
        # - thread
        # - components
        # - sticker_items

        if "type" in data:
            # This is always present during MESSAGE_CREATE but can be
            # absent for some reason in MESSAGE_UPDATE event.
            self.type = data["type"]

        self.id = int(data["id"])
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
        self.reactions = [Reaction(r, message=self) for r in data.get("reactions", [])]
        edited_at = data.get("edited_timestamp")
        message_reference = data.get("message_reference")
        self.edited_at = parse_iso_timestamp(edited_at) if edited_at is not None else None
        self.message_reference = MessageReference.from_dict(message_reference) if message_reference is not None else None

        self._handle_author(data)
        self._handle_mentions(data)
        self._handle_mention_roles(data)
        self._handle_referenced_message(data)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, content={self.content!r}, author={self.author!r})"

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

    def _handle_reaction_add(self, emoji: typing.Dict[str, typing.Any], user: typing.Union[User, GuildMember]) -> Reaction:
        emoji_id = get_optional_snowflake(emoji, "id")
        emoji_name = emoji.get("name")
        existing_reaction = None

        for reaction in self.reactions:
            reaction_emoji = reaction.emoji

            if reaction_emoji.id == emoji_id and reaction_emoji.name == emoji_name:
                existing_reaction = reaction
                break

        if existing_reaction is None:
            data = {
                "count": 1,
                "me": user.id == self._client.user.id,  # type: ignore
                "emoji": emoji,
            }
            reaction = Reaction(data, message=self)
            self.reactions.append(reaction)
            return reaction
        else:
            existing_reaction.count += 1
            existing_reaction.me = user.id == self._client.user.id  # type: ignore
            return existing_reaction

    def _handle_reaction_remove(self, emoji: typing.Dict[str, typing.Any], user: typing.Union[User, GuildMember]) -> typing.Optional[Reaction]:
        emoji_id = get_optional_snowflake(emoji, "id")
        emoji_name = emoji.get("name")
        existing_reaction = None

        for reaction in self.reactions:
            reaction_emoji = reaction.emoji

            if reaction_emoji.id == emoji_id and reaction_emoji.name == emoji_name:
                existing_reaction = reaction
                break

        if existing_reaction is None:
            return None

        existing_reaction.count -= 1

        if existing_reaction.count == 0:
            # Reaction count = 0 means there are no reactions
            self.reactions.remove(existing_reaction)

        if user.id == self._client.user.id:  # type: ignore
            # Our user removed the reaction
            existing_reaction.me = False

        return existing_reaction

    def _handle_reaction_clear_emoji(self, emoji: typing.Dict[str, typing.Any]) -> typing.Optional[Reaction]:
        found_reaction = None
        emoji_id = get_optional_snowflake(emoji, "id")
        emoji_name = emoji.get("name")

        for reaction in self.reactions:
            reaction_emoji = reaction.emoji

            if reaction_emoji.id == emoji_id and reaction_emoji.name == emoji_name:
                found_reaction = reaction
                break

        if found_reaction is None:
            return None

        self.reactions.remove(found_reaction)
        return found_reaction

    @property
    def url(self) -> str:
        """The URL for this message.

        Returns
        -------
        :class:`builtins.str`
        """
        guild_id = self.guild_id

        if guild_id is not None:
            return f"https://discord.com/channels/{guild_id}/{self.channel_id}/{self.id}"

        return f"https://discord.com/channels/@me/{self.channel_id}/{self.id}"

    async def crosspost(self) -> None:
        """Crossposts the message across the channels following the message's channel.

        This operation is only possible with messages sent in a :class:`NewsChannel`.
        In order to crosspost message sent by the bot, the :attr:`~Permissions.send_messages`
        permission is required otherwise :attr:`~Permissions.manage_messages` permission
        is required.

        Raises
        ------
        HTTPForbidden
            You are not allowed to do this.
        HTTPException
            Crossposting failed.
        """
        await self._rest.crosspost_message(channel_id=self.channel_id, message_id=self.id)

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
        if embed is not UNDEFINED and embeds is not UNDEFINED:
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

    async def add_reaction(self, emoji: typing.Union[Emoji, PartialEmoji, str]) -> None:
        """Adds a reaction to the message.

        This operation requires :attr:`~Permissions.read_message_history` permission
        and additionally :attr:`~Permissions.add_reactions` permission if no one
        has reacted to the message yet.

        .. warning::
            It is a common misconception of passing unicode emoji in Discord markdown
            format such as ``:smile:``. The emoji must be passed as unicode emoji. For
            custom emojis, The format ``<:name:id>`` is used.

        Parameters
        ----------
        emoji: Union[:class:`builtins.str`, :class:`Emoji`, :class:`PartialEmoji`]
            The emoji to react with.

        Raises
        ------
        HTTPForbidden
            Missing permissions.
        HTTPException
            The operation failed.
        """
        await self._rest.add_reaction(
            channel_id=self.channel_id,
            message_id=self.id,
            emoji=_get_reaction_emoji(emoji),
        )

    async def remove_reation(self, emoji: typing.Union[Emoji, PartialEmoji, Reaction, str], user: typing.Union[User, GuildMember] = UNDEFINED) -> None:
        """Removes a reaction from the message.

        When removing own reaction (not passing the ``user`` parameter), No permissions
        are required however when removing other's reactions, The :attr:`~Permissions.manage_messages`
        permissions are needed.

        .. warning::
            It is a common misconception of passing unicode emoji in Discord markdown
            format such as ``:smile:``. The emoji must be passed as unicode emoji. For
            custom emojis, The format ``<:name:id>`` is used.

        Parameters
        ----------
        emoji: Union[:class:`builtins.str`, :class:`Emoji`, :class:`PartialEmoji`, :class:`Reaction`]
            The emoji to remove reaction of.
        user: Union[:class:`User`, :class:`GuildMember`]
            The user to remove reaction of. If not provided, This defaults to own
            (bot) user.

        Raises
        ------
        HTTPForbidden
            Missing permissions.
        HTTPException
            The operation failed.
        """
        if user is UNDEFINED:
            await self._rest.remove_own_reaction(
                channel_id=self.channel_id,
                message_id=self.id,
                emoji=_get_reaction_emoji(emoji),
            )
        else:
            await self._rest.remove_user_reaction(
                channel_id=self.channel_id,
                message_id=self.id,
                user_id=user.id,
                emoji=_get_reaction_emoji(emoji),
            )

    async def clear_reactions(self, emoji: typing.Union[Emoji, PartialEmoji, Reaction, str] = UNDEFINED) -> None:
        """Clears all reactions or reactions for a specific emoji from the message.

        The :attr:`~Permissions.manage_messages` permissions are needed to
        perform this action.

        .. warning::
            It is a common misconception of passing unicode emoji in Discord markdown
            format such as ``:smile:``. The emoji must be passed as unicode emoji. For
            custom emojis, The format ``<:name:id>`` is used.

        Parameters
        ----------
        emoji: Union[:class:`builtins.str`, :class:`Emoji`, :class:`PartialEmoji`, :class:`Reaction`]
            The emoji to clear reactions of. If not provided, All reactions are
            removed from the message.

        Raises
        ------
        HTTPForbidden
            Missing permissions.
        HTTPException
            The operation failed.
        """
        if emoji is UNDEFINED:
            await self._rest.clear_reactions(
                channel_id=self.channel_id,
                message_id=self.id,
            )
        else:
            await self._rest.clear_reactions_for_emoji(
                channel_id=self.channel_id,
                message_id=self.id,
                emoji=_get_reaction_emoji(emoji),
            )
