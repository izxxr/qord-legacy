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

_REST_BASE_URL = "https://discord.com/api/v9"

class Route:
    __slots__ = ("method", "path", "requires_auth", "supports_reason", "params")

    def __init__(self,
        method: typing.Literal["GET", "POST", "PUT", "DELETE", "PATCH"],
        path: str,
        *,
        requires_auth: bool = True,
        supports_reason: bool = False,
        **params: typing.Any,
    ) -> None:

        self.method = method
        self.path = path
        self.requires_auth = requires_auth
        self.supports_reason = supports_reason
        self.params = params

    @property
    def url(self) -> str:
        return _REST_BASE_URL + self.path.format_map(self.params)

    def __repr__(self) -> str:
        return f"{self.method} {self.url}"

