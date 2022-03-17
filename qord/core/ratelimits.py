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


REST_BASE_URL = "https://discord.com/api/v10"


class Route:
    __slots__ = ("method", "path", "requires_auth", "params")

    def __init__(self,
        method: typing.Literal["GET", "POST", "PUT", "DELETE", "PATCH"],
        path: str,
        *,
        requires_auth: bool = True,
        **params: typing.Any,
    ) -> None:

        self.method = method
        self.path = path
        self.requires_auth = requires_auth
        self.params = params

    @property
    def url(self) -> str:
        return REST_BASE_URL + self.path.format_map(self.params)

    @property
    def bucket(self) -> str:
        params = self.params

        # Major parameters used for generating ratelimit bucket key.
        guild_id = params.get("guild_id")
        channel_id = params.get("channel_id")

        return f"{self.method}-{guild_id}:{channel_id}"

    def __repr__(self) -> str:
        return f"{self.method} {self.url}"


class RatelimitHandler:
    def __init__(self) -> None:
        self.global_ratelimit_cleared = asyncio.Event()
        self.global_ratelimit_cleared.set()

        # ratelimit_key is sent in X-Ratelimit-Bucket header from
        # Discord. It is a string identification of the ratelimit.
        # We are be using this key for storing the asyncio locks
        # for blocking requests on that route when the bucket is exhausted.
        #
        # The way below mappings work is:
        #
        # - locks mapping stores the asyncio.Lock instances for the
        #   related ratelimit key.
        #
        # - ratelimit_keys is the mapping of Route.bucket string to
        #   the ratelimit key associated to that bucket.
        #
        # - When get_lock() is called, it does a look up for given string
        #   which is the route bucket in the ratelimit_keys mapping
        #
        #   - If the key is found, it returns the lock object for the
        #     for that key from locks mapping.
        #
        #   - If the key is not found, It returns None which indicates
        #     that ratelimit state for the given bucket is currently unknown
        #     and not yet stored.

        # { ratelimit_key (str) : asyncio.Lock }
        self.locks = {}

        # { route.bucket (str) : ratelimit_key }
        self.ratelimit_keys = {}

    def set_global(self) -> None:
        self.global_ratelimit_cleared.clear()

    def reset_global(self) -> None:
        self.global_ratelimit_cleared.set()

    def get_lock(self, bucket: str) -> typing.Optional[asyncio.Lock]:
        key = self.ratelimit_keys.get(bucket)

        if key is None:
            # The ratelimit key for this bucket is unknown yet.
            return None

        try:
            return self.locks[key]
        except KeyError:
            self.locks[key] = lock = asyncio.Lock()
            return lock

    def set_lock(self, key: str, lock: asyncio.Lock) -> None:
        if key in self.locks:
            # This is a guard to prevent overwriting previously stored lock.
            return

        self.locks[key] = lock

    def set_ratelimit_key(self, bucket: str, key: str) -> None:
        self.ratelimit_keys[bucket] = key

    async def wait_until_global_reset(self) -> None:
        await self.global_ratelimit_cleared.wait()
