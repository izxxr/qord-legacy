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


class GatewayEvent:
    """An enumeration that details names of various events sent over gateway.

    These events names are commonly passed in :class:`Client.event` decorator for
    registering a listener for relevant event.
    """

    GATEWAY_DISPATCH = "gateway_dispatch"
    """Called whenever gateway sends a dispatch event. See :class:`events.GatewayDispatch` for more info."""

    SHARD_READY = "shard_ready"
    """Called whenever a shard is in ready state. See :class:`events.ShardReady` for more info."""

    READY = "ready"
    """Called whenever all shards are ready. See :class:`events.Ready` for more info."""

    RESUMED = "resumed"
    """Called whenever a shard successfully resumes a gateway session. See :class:`events.Resumed` for more info."""

    USER_UPDATE = "user_update"
    """Called whenever a user is updated. See :class:`events.UserUpdate` for more info."""

    GUILD_AVAILABLE = "guild_available"
    """Called whenever a guild becomes available to the client. See :class:`events.GuildAvailable` for more info."""

    GUILD_UNAVAILABLE = "guild_unavailable"
    """Called whenever a guild becomes unavailable to the client. See :class:`events.GuildUnavailable` for more info."""

    GUILD_JOIN = "guild_join"
    """Called whenever the bot joins a new guild. See :class:`events.GuildJoin` for more info."""

    GUILD_LEAVE = "guild_leave"
    """Called whenever the bot leaves a guild. See :class:`events.GuildLeave` for more info."""

    GUILD_UPDATE = "guild_update"
    """Called whenever a guild is updated. See :class:`events.GuildUpdate` for more info."""

    ROLE_CREATE = "role_create"
    """Called whenever a guild role is created. See :class:`events.RoleCreate` for more info."""

    ROLE_UPDATE = "role_update"
    """Called whenever a guild role is updated. See :class:`events.RoleUpdate` for more info."""

    ROLE_DELETE = "role_delete"
    """Called whenever a guild role is deleted. See :class:`events.RoleDelete` for more info."""

    GUILD_MEMBER_ADD = "guild_member_join"
    """Called whenever a member joins a guild. See :class:`events.GuildMemberAdd` for more info."""

    GUILD_MEMBER_REMOVE = "guild_member_remove"
    """Called whenever a member is removed i.e left, kicked or banned from a guild. See :class:`events.GuildMemberRemove` for more info."""

    GUILD_MEMBER_UPDATE = "guild_member_update"
    """Called whenever a member is updated. See :class:`events.GuildMemberUpdate` for more info."""

    CHANNEL_CREATE = "channel_create"
    """Called whenever a channel is created. See :class:`events.ChannelCreate` for more info."""

    CHANNEL_UPDATE = "channel_update"
    """Called whenever a channel is updated. See :class:`events.ChannelUpdate` for more info."""

    CHANNEL_PINS_UPDATE = "channel_pins_update"
    """Called whenver a message is pinned/unpinned in a channel. See :class:`events.ChannelPinsUpdate` for more info."""

    CHANNEL_DELETE = "channel_delete"
    """Called whenever a channel is deleted. See :class:`events.ChannelDelete` for more info."""

    TYPING_START = "typing_start"
    """Called whenever a user starts typing. See :class:`events.TypingStart` for more info."""

    MESSAGE_CREATE = "message_create"
    """Called whenever a message is sent. See :class:`events.MessageCreate` for more info."""

    MESSAGE_DELETE = "message_delete"
    """Called whenever a message is deleted. See :class:`events.MessageDelete` for more info."""

    MESSAGE_UPDATE = "message_update"
    """Called whenever a message is edited. See :class:`events.MessageUpdate` for more info."""

    MESSAGE_BULK_DELETE = "message_bulk_delete"
    """Called whenever multiple messages are deleted. See :class:`events.MessageDelete` for more info."""


class PremiumType:
    """An enumeration that details values for a user's premium aka nitro subscription.

    Most common place where this enumeration is useful is when working with the
    :attr:`User.premium_type` attribute.
    """

    NONE = 0
    """User has no nitro subcription."""

    NITRO_CLASSIC = 1
    """User has nitro classic subscription."""

    NITRO = 2
    """User has nitro subscription."""

class DefaultAvatar:
    """An enumeration that details values for a user's default avatar.

    A user's default avatar value is calculated on the basis of user's
    four digits discriminator. It can be generated by::

        default_avatar = int(user.discriminator) % DefaultAvatar.INDEX

    To get a user's default avatar value, You should use :attr:`User.default_avatar`
    attribute.
    """

    BLURPLE = 0
    """Blurple coloured default avatar."""

    GRAY = 1
    """Gray coloured default avatar."""

    GREEN = 2
    """Green coloured default avatar."""

    YELLOW = 3
    """Yellow coloured default avatar."""

    RED = 4
    """Red coloured default avatar."""

    PINK = 5
    """Pink coloured default avatar."""

    INDEX = 5
    """The zero based index integer used for generating the user's default avatar.

    This is based of number of colours available for default avatars.
    As such, If Discord adds a new avatar colour, This index will increment.
    """

class ImageExtension:
    """An enumeration that details values for a various image extensions supported
    on the Discord CDN URLs.
    """

    PNG = "png"
    """PNG extension."""

    JPG = "jpg"
    """An alias of :attr:`.JPEG`."""

    JPEG = "jpeg"
    """JPEG extension."""

    WEBP = "webp"
    """WEBP extension."""

    GIF = "gif"
    """GIF extension. This is only supported for animated image resources."""

class VerificationLevel:
    """An enumeration that details values for a :class:`Guild`'s :attr:`~Guild.verification_level`

    Verification level defines the requirements for a user account to be member of the guild.
    """

    NONE = 0
    """No verification level set. Unrestricted."""

    LOW = 1
    """Users must have verified email bound to their account."""

    MEDIUM = 2
    """Users must also be registered to Discord for more then 5 minutes."""

    HIGH = 3
    """Users must also be part of the guild for more then 10 minutes."""

    VERY_HIGH = 4
    """Users must also have a verified phone number bound to their account."""

class NotificationLevel:
    """An enumeration that details values for a :class:`Guild`'s :attr:`~Guild.notification_level`

    Notification level defines the levels of notifications that the members of the
    guilds will receive upon messages.
    """

    ALL_MESSAGES = 0
    """Members will receive notifications for every single message sent in the guild."""

    ONLY_MENTIONS = 1
    """Members will receive notifications for only messages that mentions them."""

class ExplicitContentFilter:
    """An enumeration that details values for a :class:`Guild`'s :attr:`~Guild.explicit_content_filter`

    Explicit content filter defines the explicit content checks and filters done on the files
    sent in the guild messages.
    """

    DISABLED = 0
    """No scanning on sent files will be done."""

    MEMBERS_WITHOUT_ROLES = 1
    """Scanning will be done for messages sent by members that don't have any role assigned."""

    ALL_MEMBERS = 2
    """Scanning will be done for all messages."""

class NSFWLevel:
    """An enumeration that details values for a :class:`Guild`'s :attr:`~Guild.nsfw_level`

    NSFW level defines whether the guild is marked as Not Safe For Work (NSFW) or
    age restricted.
    """

    DEFAULT = 0
    """No explicit NSFW level is set."""

    EXPLICIT = 1
    """Guild is marked as explicit."""

    SAFE = 2
    """Guild is marked as Safe For Work (SFW)."""

    AGE_RESTRICTED = 3
    """Guild is marked as age restricted."""

class PremiumTier:
    """An enumeration that details values for a :class:`Guild`'s :attr:`~Guild.premium_tier`

    Premium tier defines the server boosts level of the guild.
    """

    NONE = 0
    """No boost level unlocked by the guild yet."""

    TIER_1 = 1
    """Guild has unlocked boost level 1 perks."""

    TIER_2 = 2
    """Guild has unlocked boost level 2 perks."""

    TIER_3 = 3
    """Guild has unlocked boost level 3 perks."""

class MFALevel:
    """An enumeration that details values for a :class:`Guild`'s :attr:`~Guild.mfa_level`

    MFA level defines the 2 factor authentication requirement for the guild moderators
    for performing moderative actions.
    """

    DISABLED = 0
    """2FA is not required for performing moderative actions."""

    ELEVATED = 1
    """2FA is required for performing moderative actions.."""

class ChannelType:
    """An enumeration that details the types of channels."""

    TEXT = 0
    """The channel is a guild's text channel."""

    DM = 1
    """The channel is a private DM between two users."""

    VOICE = 2
    """The channel is a guild's voice channel."""

    GROUP = 3
    """The channel is a private group DM channel."""

    CATEGORY = 4
    """The channel is a guild's category that holds other channels."""

    NEWS = 5
    """The channel is a guild's news channel."""

    STORE = 6
    """The channel is a guild's store channel."""

    NEWS_THREAD = 10
    """The channel is a thread created inside a news channel."""

    PUBLIC_THREAD = 11
    """The channel is a public thread."""

    PRIVATE_THREAD = 12
    """The channel is a private thread."""

    STAGE = 13
    """The channel is a guild's stage channel."""

class VideoQualityMode:
    """An enumeration that details the video quality mode of a :class:`VoiceChannel`."""

    AUTO = 1
    """Automatic quality. Discord will chose the best quality for optimal performance."""

    FULL = 2
    """720p quality."""
