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

from qord import events
import inspect
import typing

if typing.TYPE_CHECKING:
    from qord.core.client import Client
    from qord.core.shard import Shard


def event_dispatch_handler(name: str):
    def _wrap(func: typing.Callable[[DispatchHandler, Shard, typing.Any], typing.Any]):
        func.__handler_event__ = name
        return func

    return _wrap


class DispatchHandler:
    r"""Internal class that handles gateway events dispatches."""

    def __init__(self, client: Client) -> None:
        self.client = client
        self.invoke = client.invoke_event
        self._update_handlers()

    def _update_handlers(self):
        self._handlers = {}
        members = inspect.getmembers(self)

        for _, member in members:
            try:
                self._handlers[member.__handler_event__] = member
            except AttributeError:
                pass

    async def handle(self, shard: Shard, title: str, data: typing.Any) -> None:
        event = events.GatewayDispatch(shard=shard, title=title, data=data)
        self.invoke("gateway_dispatch", event)

        try:
            handler = self._handlers[title]
        except KeyError:
            return
        else:
            await handler(shard, data)

    @event_dispatch_handler("READY")
    async def on_ready(self, shard, data):
        print("Handler called.")

