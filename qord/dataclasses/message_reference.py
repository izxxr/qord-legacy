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

from qord.internal.helpers import get_optional_snowflake
import typing

if typing.TYPE_CHECKING:
    from qord.models.messages import Message


class MessageReference:
    """Represents a reference to another message in a :class:`Message`.

    This class also allows you to create custom message references for replying
    to messages via :meth:`~BaseMessageChannel.send` method.

    .. note::
        If you have the :class:`Message` that you are replying to, consider using the
        :meth:`~Message.reply` method for more user friendly API interface.

    .. tip::
        For creating message replies, Only ``message_id`` parameter is required however
        ``channel_id`` and ``guild_id`` would be validated when supplied.

    From API responses, This class is present on :attr:`Message.message_reference`
    attribute indicating a reference to another message. It is sent when the :class:`Message`
    has the following type/flag:

    - :class:`MessageFlags.is_crosspost`
    - :class:`MessageType.REPLY`
    - :class:`MessageType.CHANNEL_FOLLOW_ADD`
    - :class:`MessageType.CHANNEL_PIN_ADD`
    - :class:`MessageType.THREAD_STARTER_MESSAGE`

    Parameters
    ----------
    message_id: :class:`builtins.int`
        The ID of message being replied.
    channel_id: :class:`builtins.int`
        The ID of channel that the referenced message belongs to.
    guild_id: :class:`builtins.int`
        The ID of guild that the referenced message belongs to, if any.
    fail_if_not_exists: :class:`builtins.bool`
        Whether the API should throw :class:`HTTPException` if the message
        being referenced does not exist. Defaults to ``True``.

    Attributes
    ----------
    message_id: Optional[:class:`builtins.int`]
        The ID of message that is being referenced.

        For message of type :attr:`~MessageType.CHANNEL_FOLLOW_ADD`, This is
        ``None``.
    channel_id: Optional[:class:`builtins.int`]
        The ID of channel that the reference belongs to.
        This is always present when getting this class from an API
        response and is optional when instansiating the class manually.
    guild_id: Optional[:class:`builtins.int`]
        The ID of guild that the reference belongs to, if any.
    """

    if typing.TYPE_CHECKING:
        message_id: typing.Optional[int]
        channel_id: typing.Optional[int]
        guild_id: typing.Optional[int]

    def __init__(
        self,
        message_id: int,
        channel_id: typing.Optional[int] = None,
        guild_id: typing.Optional[int] = None,
        *,
        fail_if_not_exists: bool = True,
    ) -> None:

        self.message_id = message_id
        self.channel_id = channel_id
        self.guild_id   = guild_id
        self.fail_if_not_exists = fail_if_not_exists

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        ret = {"message_id": self.message_id, "fail_if_not_exists": self.fail_if_not_exists}

        if self.channel_id is not None:
            ret["channel_id"] = self.channel_id

        elif self.guild_id is not None:
            ret["guild_id"] = self.guild_id

        return ret

    @classmethod
    def from_dict(cls, data: typing.Dict[str, typing.Any]) -> MessageReference:
        # For API responses, The message_id key is optional while
        # it is annotated as `int` in constructor to aid user facing API.
        return cls(
            message_id=get_optional_snowflake(data, "message_id"), # type: ignore # See above
            channel_id=int(data["channel_id"]),
            guild_id=get_optional_snowflake(data, "guild_id"),
        )

    @classmethod
    def from_message(cls, message: Message, *, fail_if_not_exists: bool = True) -> MessageReference:
        """Creates a message reference from a :class:`Message`.

        .. tip::
            For creating message replies, Only ``message_id`` parameter is required however
            ``channel_id`` and ``guild_id`` would be validated when supplied.

        Parameters
        ----------
        message: :class:`Message`
            The message to create reference for.
        fail_if_not_exists: :class:`builtins.bool`
            Whether the API should throw :class:`HTTPException` when sending
            message with this reference if the message being referenced does
            not exist. Defaults to ``True``.

        Returns
        -------
        :class:`MessageReference`
            The created reference for given message.
        """
        return cls(
            message_id=message.id,
            channel_id=message.channel_id,
            guild_id=message.guild_id,
            fail_if_not_exists=fail_if_not_exists,
        )

