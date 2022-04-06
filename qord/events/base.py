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

import typing

if typing.TYPE_CHECKING:
    from qord.core.shard import Shard

__all__ = (
    "BaseEvent",
    "BaseGatewayEvent",
)

class BaseEvent:
    """Base class for events.

    All custom events must inherit from this class. When subclassing the
    ``event_name`` parameter is required.

    .. note::
        Parameters documented below are passed during subclassing.

    Parameters
    ----------
    event_name: :class:`builtins.str`
        The string representation of name of event. This is used for
        identifying the event and must be unique.

        .. warning::
            Do not use event names that are already reserved by the library
            for example the event names from :class:`GatewayEvent`.
    """

    __event_name__: str

    def __init_subclass__(cls, event_name: str) -> None:
        if not isinstance(event_name, str):
            raise TypeError("'event_name' parameter must be str.")

        cls.__event_name__ = event_name


@typing.runtime_checkable
class BaseGatewayEvent(typing.Protocol):
    """A :class:`typing.Protocol` that details events sent over the gateway.

    This protocol supports runtime checks like :meth:`isinstance`
    or :meth:`issubclass` etc.
    """

    shard: typing.Optional[Shard]
    """The shard that received this event over gateway.

    This attribute can be ``None`` in events that are not shard specific and are
    not invoked by a shard. The most common example is :class:`events.Ready`.
    """