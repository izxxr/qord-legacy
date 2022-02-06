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

from qord.exceptions import (
    ClientSetupRequired,
    HTTPBadRequest,
    HTTPException,
    HTTPForbidden,
    HTTPNotFound,
    HTTPServerError,
)
from qord.project_info import __version__, __github__
from qord.core.routes import Route

import aiohttp
import typing


class RestClient:
    r"""REST handling implementation including ratelimits prevention and handling."""

    if typing.TYPE_CHECKING:
        session: typing.Optional[aiohttp.ClientSession]
        session_owner: bool
        token: typing.Optional[str]
        max_retries: int

    def __init__(self, *,
        session: aiohttp.ClientSession = None,
        session_owner: bool = True,
        max_retries: int = 5,
    ) -> None:

        if session and isinstance(session, aiohttp.ClientSession):
            raise TypeError(f"Parameter 'session' must be an instance of aiohttp.ClientSession " \
                            f"object, Not {session.__class__!r}")
        if max_retries is None or max_retries == 0:
            max_retries = 1
        if not isinstance(max_retries, int) or max_retries > 5:
            raise TypeError(f"Parameter 'max_retries' must be an integer less than 5. " \
                            f"{max_retries!r} is not valid.")

        self.session = session
        self.session_owner: bool = session_owner
        self.token = None
        self.max_retries = max_retries or 5

    def _ensure_session(self) -> aiohttp.ClientSession:
        session = self.session

        if session and not session.closed:
            return session

        self.session = aiohttp.ClientSession()
        return self.session

    async def _resolve_response(self, response):
        if response.headers["content_type"] == "application/json":
            data = await response.json()
        else:
            data = await response.text()

        return data

    async def request(self, route: Route, reason: str = None, **options: typing.Any) -> typing.Any:
        session = self._ensure_session()

        token = self.token
        requires_auth = route.requires_auth

        if requires_auth and token is None:
            raise ClientSetupRequired("No bot token is set yet to perform this request. " \
                                      "Client is not setup yet.")

        headers = options.pop("headers", dict())

        headers["User-Agent"] = f"DiscordBot ({__github__}, {__version__})"

        if requires_auth:
            headers["Authorization"] = f"Bot {token}"
        if reason is not None and route.supports_reason:
            headers["X-Audit-Log-Reason"] = reason

        for attempt in range(self.max_retries):
            async with session.request(
                route.method,
                route.url,
                headers=headers,
                **options
            ) as response:

                status = response.status

                if status == 204:
                    # 204 *No Content*
                    return None

                data = await response.json()

                if status < 300:
                    return data
                elif status == 400:
                    raise HTTPBadRequest(response, data)
                elif status == 403:
                    raise HTTPForbidden(response, data)
                elif status == 404:
                    raise HTTPNotFound(response, data)
                elif status >= 500:
                    raise HTTPServerError(response, data)

                # unhandleable status code, raise it.
                raise HTTPException(response, data)

    async def close(self):
        if not self.session_owner:
            await self.session.close()

    # ----- Gateway -----

    async def get_gateway(self):
        route = Route("GET", "/gateway", requires_auth=False)
        data = await self.request(route)
        return data

    async def get_bot_gateway(self):
        route = Route("GET", "/gateway/bot", requires_auth=True)
        data = await self.request(route)
        return data