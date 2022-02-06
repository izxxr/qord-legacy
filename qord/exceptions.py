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
    from aiohttp import ClientResponse


__all__ = (
    "QordException",
    "ClientSetupRequired",
    "HTTPException",
    "HTTPBadRequest",
    "HTTPForbidden",
    "HTTPNotFound",
    "HTTPServerError",
)

class QordException(Exception):
    r"""Base exception class for all exceptions raised by the library."""

class ClientSetupRequired(QordException):
    r"""An exception indicating that client setup is required to perform the attempted
    operation that caused the exception.

    For HTTPs operations, This generally means that requested endpoint requires
    authorization with a bot token but no bot token is set yet.

    You must call :meth:`Client.setup` with a proper bot token first to setup
    the client first before retrying.
    """
    pass

class HTTPException(QordException):
    r"""Base exception class for all exceptions that indicate failure of a HTTP request
    i.e request returned with an unsuccessful status code..

    Attributes
    ----------
    response: :class:`aiohttp.ClientResponse`
        The failed request response.
    data: Union[:class:`builtins.dict`, :class:`builtins.str`]
        The data from the response. In most cases, This is a dictionary representing
        the JSON responose however in rare cases like CloudFlare errors, This can be
        a string of raw HTML.
    """
    def __init__(self, response: ClientResponse, data: typing.Union[str, dict]) -> None:
        self.response = response
        self.data = data

        if isinstance(data, dict):
            try:
                data = data["message"]
            except KeyError:
                pass

        super().__init__(data)

class HTTPBadRequest(HTTPException):
    r""":exc:`HTTPException` indicating a ``400 Bad Request`` response."""

class HTTPForbidden(HTTPException):
    r""":exc:`HTTPException` indicating a ``403 Forbidden`` response."""

class HTTPNotFound(HTTPException):
    r""":exc:`HTTPException` indicating a ``404 Not Found`` response."""

class HTTPServerError(HTTPException):
    r""":exc:`HTTPException` indicating a 500s response."""
