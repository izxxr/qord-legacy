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

from qord.internal.helpers import compute_creation_time

import typing

if typing.TYPE_CHECKING:
    from datetime import datetime


__all__ = (
    "Comparable",
)


class Comparable:
    __slots__ = ()

    id: int

    def __eq__(self, other: typing.Any) -> bool:
        return isinstance(other, self.__class__) and other.id == self.id


class CreationTime:
    __slots__ = ()

    id: int

    @property
    def created_at(self) -> datetime:
        """The time when this entity was created.

        Returns
        -------
        :class:`datetime.datetime`
            UTC aware datetime object representing the creation time.
        """
        return compute_creation_time(self.id)
