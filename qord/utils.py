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

"""
qord.utils
~~~~~~~~~~

General utilities to aid in specific common tasks.
"""

from __future__ import annotations

from datetime import datetime
import typing


def create_timestamp(
    time: typing.Optional[typing.Union[datetime, int, float]] = None,
    style: typing.Optional[str] = None,
) -> str:

    """Creates a markdown timestamp from the given datetime object or unix timestamp.

    Parameters
    ----------
    time: Optional[Union[:class:`datetime.datetime`, :class:`builtins.int`, :class:`builtins.float`]]
        The timestamp to use. If not given, The result of :meth:`datetime.datetime.now` is used.
        If a datetime object is given, The epoch timestamp would be extracted from it. If
        a float is given, It would be rounded of.
    style: :class:`builtins.str`
        The style for the timestamp. If not provided, The default style
        is used, See :class:`TimestampStyle` for all possible values.

        .. note::
            This parameter is not validated by the library in case Discord
            adds a new style. You should consider validating it yourself.

    Returns
    -------
    :class:`builtins.str`
        The created timestamp in proper format.
    """
    if time is None:
        time = round(datetime.now().timestamp())
    elif isinstance(time, datetime):
        time = round(time.timestamp())
    elif isinstance(time, float):
        time = round(time)

    if style is None:
        return f"<t:{time}>"
    else:
        return f"<t:{time}:{style}>"
