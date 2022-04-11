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

from qord.internal.undefined import UNDEFINED

from datetime import datetime, timezone
from base64 import b64encode
import typing


__all__ = (
    "BASE_CDN_URL",
    "BASIC_STATIC_EXTS",
    "BASIC_EXTS",
    "create_cdn_url",
    "get_optional_snowflake",
    "compute_shard_id",
    "get_image_data",
    "parse_iso_timestamp",
)


BASE_CDN_URL = "https://cdn.discordapp.com"
BASIC_STATIC_EXTS = ["png", "jpg", "jpeg", "webp"]
BASIC_EXTS = ["png", "jpg", "jpeg", "webp", "gif"]

def create_cdn_url(path: str, extension: str, size: int = UNDEFINED, valid_exts: typing.List[str] = UNDEFINED):
    """Create a CDN URL with provided path, file extension and size."""

    if valid_exts is None:
        # Defaulting to general formats used on most endpoints which
        # are currently png, jpg, webp.
        # When using with endpoints that have special formats
        # consider passing the valid formats explicitly.
        valid_exts = BASIC_STATIC_EXTS

    if not extension.lower() in valid_exts:
        raise ValueError(f"Invalid image extension {extension!r}, Expected one of {', '.join(valid_exts)}")

    ret = f"{BASE_CDN_URL}{path}.{extension}"

    if size is not UNDEFINED:
        if size < 64 and size > 4096:
            raise ValueError("size must be between 64 and 4096. Got %s instead." % size)
        if not (size & (size-1) == 0) and (size != 0 and size-1 != 0):
            raise ValueError("size must be a power of 2 between 64 and 4096, %s is invalid." % size)

        return f"{ret}?size={size}"

    return ret

def get_optional_snowflake(data: typing.Dict[str, typing.Any], key: str) -> typing.Optional[int]:
    """Helper to obtain optional or nullable snowflakes from a raw payload."""
    try:
        return int(data[key])
    except (KeyError, ValueError, TypeError):
        return None

def compute_shard_id(guild_id: int, shards_count: int) -> int:
    """Computes shard ID for the provided guild ID with respect to given shards count."""
    return (guild_id >> 22) % shards_count

def get_image_data(img_bytes: bytes) -> str:
    """Gets Data URI format for provided image bytes."""

    if img_bytes.startswith(b"\x89\x50\x4E\x47\x0D\x0A\x1A\x0A"):
        content_type = "image/png"
    elif img_bytes[0:3] == b"\xff\xd8\xff" or img_bytes[6:10] in (b"JFIF", b"Exif"):
        content_type = "image/jpeg"
    elif img_bytes.startswith((b"\x47\x49\x46\x38\x37\x61", b"\x47\x49\x46\x38\x39\x61")):
        content_type = "image/gif"
    elif img_bytes.startswith(b"RIFF") and img_bytes[8:12] == b"WEBP":
        content_type = "image/webp"
    else:
        raise TypeError("Invalid image type was provided.")

    return f"data:{content_type};base64,{b64encode(img_bytes).decode('ascii')}"

def parse_iso_timestamp(timestamp: str) -> datetime:
    """Parse ISO timestamp string to a datetime.datetime instance."""
    return datetime.fromisoformat(timestamp)

def compute_creation_time(snowflake: int) -> datetime:
    """Computes the creation time of the given snowflake as UTC timezone aware datetime."""
    timestamp = ((snowflake >> 22) + 1420070400000) / 1000
    return datetime.fromtimestamp(timestamp, tz=timezone.utc)
