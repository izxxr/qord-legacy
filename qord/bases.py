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

from qord.models.messages import Message
from qord._helpers import UNDEFINED

from abc import ABC, abstractmethod
import typing

if typing.TYPE_CHECKING:
    from qord.core.rest import RestClient


class MessagesSupported(ABC):
    r"""A base class that implements support for messages managament.

    Almost all classes that support the :class:`Message` related operations
    inherit this class. The most common example is :class:`TextChannel`.
    """
    _rest: RestClient

    @abstractmethod
    async def _get_message_channel(self) -> typing.Any:
        raise NotImplementedError

    async def fetch_message(self, message_id: int) -> Message:
        """Fetches a :class:`Message` from the provided message ID.

        Parameters
        ----------
        message_id: :class:`builtins.int`
            The ID of message to fetch.

        Returns
        -------
        :class:`Message`
            The fetched message.

        Raises
        ------
        HTTPNotFound
            Invalid or unknown message ID passed. Message might be deleted.
        HTTPForbidden
            Missing permissions to fetch that message.
        HTTPException
            The fetching failed.
        """
        channel = await self._get_message_channel()
        data = await self._rest.get_message(channel_id=channel.id, message_id=message_id)
        return Message(data, channel=channel)

    async def fetch_pins(self) -> typing.List[Message]:
        """Fetches the messages that are currently pinned in the channel.

        Returns
        -------
        List[:class:`Message`]
            The pinned messages in the channel.

        Raises
        ------
        HTTPForbidden
            Missing permissions to fetch the pins.
        HTTPException
            The fetching failed.
        """
        channel = await self._get_message_channel()
        data = await self._rest.get_pinned_messages(channel_id=channel.id)
        return [Message(item, channel=channel) for item in data]

    # TODO: Add the remaining fields support here.
    async def send(
        self,
        content: str = UNDEFINED,
        *,
        tts: bool = UNDEFINED,
    ):
        """Sends a message to the channel.

        If channel is a text based guild channel, This requires the
        :attr:`~Permissions.send_messages` permission in the channel.

        For direct messages channel, No specific permission is required
        however relevant user must share a guild with the bot and the bot must
        not be blocked by the user.

        Parameters
        ----------
        content: :class:`builtins.str`
            The content of message.
        tts: :class:`builtins.bool`
            Whether the sent message is a Text-To-Speech message.

        Returns
        -------
        :class:`Message`
            The message that was sent.

        Raises
        ------
        HTTPForbidden
            You are not allowed to send message in this channel.
        HTTPBadRequest
            The message has invalid data.
        HTTPException
            The sending failed for some reason.
        """
        json = {}

        if content is not UNDEFINED:
            json["content"] = content
        if tts is not UNDEFINED:
            json["tts"] = tts

        channel = await self._get_message_channel()
        data = await self._rest.send_message(channel_id=channel.id, json=json)
        return Message(data, channel=channel)