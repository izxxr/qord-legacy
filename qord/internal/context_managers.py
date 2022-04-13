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

import asyncio
import typing

if typing.TYPE_CHECKING:
    from qord.bases import BaseMessageChannel


class TypingContextManager:
    def __init__(self, channel: BaseMessageChannel) -> None:
        self.channel = channel
        self._typing = False
        self._task = None

    async def _typing_task(self) -> None:
        while self._typing:
            await self.channel.trigger_typing()
            # The typing indicator disappears after 9-10 seconds
            await asyncio.sleep(8)

    async def __aenter__(self) -> None:
        coro = self._typing_task()
        self._typing = True
        self._task = asyncio.create_task(coro)

    async def __aexit__(self, *args) -> None:
        self._typing = False
        task = self._task

        if task and not task.cancelled():
            task.cancel()
