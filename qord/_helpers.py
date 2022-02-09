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

r"""*Non-public* internal utilities."""

from __future__ import annotations

import typing

BASE_CDN_URL = "https://cdn.discordapp.com"


def create_cdn_url(path: str, extension: str, size: int = None, valid_exts: typing.List[str] = None):
    r"""Create a CDN URL with provided path, file extension and size."""

    if valid_exts is None:
        # Defaulting to general formats used on most endpoints which
        # are currently gif, png, jpg, webp.
        # When using with endpoints that have special formats
        # consider passing the valid formats explicitly.
        valid_exts = ["png", "jpeg", "jpg", "webp"]

    if not extension.lower() in valid_exts:
        raise ValueError(f"Invalid image extension {extension!r}, Expected one of {', '.join(valid_exts)}")

    ret = f"{BASE_CDN_URL}{path}.{extension}"

    if size is not None:
        if size < 64 and size > 4096:
            raise ValueError("size must be between 64 and 4096. Got %s instead." % size)
        if not (size & (size-1) == 0) and (size != 0 and size-1 != 0):
            raise ValueError("size must be a power of 2 between 64 and 4096, %s is invalid." % size)

        return f"{ret}?size={size}"

    return ret

def get_optional_snowflake(data: typing.Dict[str, typing.Any], key: str) -> typing.Optional[int]:
    r"""Helper to obtain optional or nullable snowflakes from a raw payload."""
    try:
        return int(data[key])
    except (KeyError, ValueError, TypeError):
        return None
