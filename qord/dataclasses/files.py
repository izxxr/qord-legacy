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
import os

if typing.TYPE_CHECKING:
    from io import BufferedReader


class File:
    """Represents a file that is sent in messages.

    Example usage with :meth:`~BaseMessageChannel.send` method::

        file = qord.File("path/to/file.png")
        await channel.send(files=[file])

    Parameters
    ----------
    content: Union[:class:`builtins.str`, :class:`builtins.bytes`, :class:`io.BufferedReader`]
        The content of files. If a string is being passed, It would be considered
        the file path and would be opened and red in "read binary" mode.

        When passing a :class:`builtins.bytes` object, The ``name`` parameter
        must be included.
    name: :class:`builtins.str`
        The name of file. This parameter is required when passing :class:`builtins.bytes`
        in ``content`` parameter.
    spoiler: :class:`builtins.bool`
        Whether the file should be marked as spoiler when sent.
    description: :class:`builtins.str`
        The description of attachment.

    Attributes
    ----------
    content: :class:`builtins.bytes`
        The file contents.
    """

    if typing.TYPE_CHECKING:
        content: bytes
        name: str
        spoiler: bool
        description: typing.Optional[str]

    def __init__(
        self,
        content: typing.Union[str, bytes, BufferedReader],
        /,
        *,
        name: str = None,
        description: str = None,
        spoiler: bool = False,
    ) -> None:

        if isinstance(content, str):
            with open(content, "rb") as f:
                self.content = f.read()

            if name is None:
                name = os.path.basename(content)

        elif isinstance(content, bytes):
            if name is None:
                raise TypeError("name parameter must be passed when passing in bytes object.")

            self.content = content

        elif isinstance(content, BufferedReader):
            if not content.readable():
                raise RuntimeError("content is not readable.")

            self.content = content.read()

            if name is None:
                name = content.name

        if name is None:
            raise RuntimeError("Could not resolve the file name, probably invalid type.")

        self.name = name
        self.description = description
        self.spoiler = spoiler or name.startswith("SPOILER_")

    @property
    def proper_name(self) -> str:
        """Returns the proper name of file with required prefixes attached if any."""

        if self.spoiler and not self.name.startswith("SPOILER_"):
            return f"SPOILER_{self.name}"

        return self.name
