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

from qord.exceptions import MissingPrivilegedIntents, ShardCloseException

import asyncio
import zlib
import json
import sys
import time
import logging
import typing

if typing.TYPE_CHECKING:
    from qord.core.client import Client

class GatewayOP:
    DISPATCH = 0
    HEARTBEAT = 1
    IDENTIFY = 2
    PRESENCE_UPDATE = 3
    VOICE_STATE_UPDATE = 4
    RESUME = 6
    RECONNECT = 7
    REQUEST_GUILD_MEMBERS = 8
    INVALID_SESSION = 9
    HELLO = 10
    HEARTBEAT_ACK = 11

_LOGGER = logging.getLogger(__name__)
_ZLIB_SUFFIX = b'\x00\x00\xff\xff'
_UNHANDLEABLE_CODES = (4004, 4010, 4012, 4013, 4014)

class _SignalResume(Exception):
    def __init__(self, resume: bool = True, delay: float = None) -> None:
        self.resume = resume
        self.delay = delay


class Shard:
    r"""Represents a shard that connects to Discord gateway.

    A shard is simply a separate websocket connection to Discord gateway. In
    bots that are in less then 1000 guilds, There is generally only one shard
    that  maintains all the guilds. However when this limit is exceeded, Discord
    requires  the bots to shard their connection to equally divide the workload
    of guilds in multiple shards.

    Sharding is handled transparently by the library automatically and requires
    no user interaction. This class mostly is documented for completeness and
    is not usually not relevant to a general use case.

    You should not instansiate this class yourself. Instead, Consider using one
    of the following ways to obtain it:

    - :attr:`Client.shards`
    - :attr:`Client.get_shard`
    """
    if typing.TYPE_CHECKING:
        _worker_task: typing.Optional[asyncio.Task]
        _heartbeat_task: typing.Optional[asyncio.Task]
        _last_heartbeat: typing.Optional[float]
        _heartbeat_interval: typing.Optional[float]
        _session_id: typing.Optional[str]
        _sequence: typing.Optional[int]
        _latency: float

    def __init__(self, id: int, client: Client) -> None:
        self._id = id
        self._client = client

        # For faster attribute accessing
        self._rest = client._rest
        self._handle_dispatch = client._dispatch.handle

        self._running = False
        self._worker_task = None
        self._heartbeat_task = None
        self._inflator = None
        self._buffer = bytearray()
        self._identified = asyncio.Event()
        self._resume_on_connect = False

        self._clear_gateway_data()

    def _clear_gateway_data(self):
        self._last_heartbeat = None
        self._latency = float("inf")
        self._heartbeat_interval = None
        self._session_id = None
        self._sequence = None

    @property
    def id(self) -> int:
        r"""The ID of the shard. This starts from 0 and for each shard maintained by
        a client, This ID increments till :attr:`Client.shards_count`.

        In theory, If a client is running 5 shards for example. All shard IDs can
        be obtained by::

            >>> shard_ids = list(range(client.shards_count)) # shards_count is 5
            [0, 1, 2, 3, 4]

        Returns
        -------
        :class:`builtins.int`
        """
        return self._id

    @property
    def client(self) -> Client:
        r"""The client that instansiated the client.

        Returns
        -------
        :class:`Client`
        """
        return self._client

    @property
    def latency(self) -> float:
        r"""The latency of this shard. This is measured on the basis of delay between
        a heartbeat sent by the shard and it's acknowledgement sent by Discord gateway.

        Returns
        -------
        :class:`builtins.float`
        """
        return self._latency

    @property
    def heartbeat_interval(self) -> typing.Optional[float]:
        r"""The heartbeat interval for this shard. This is only available after
        shard has done the initial websocket handshake.

        Returns
        -------
        :class:`builtins.float`
        """
        return self._heartbeat_interval

    @property
    def session_id(self) -> typing.Optional[str]:
        r"""The current session ID for the shard. This is only available
        after shard has successfully connected to gateway.

        The session ID is not same for all shards. Furthermore, The session
        ID is not guaranteed to be same through the shard lifetime as shard
        may start new sessions for reconnection purposes.

        Returns
        -------
        :class:`builtins.str`
        """
        return self._session_id

    @property
    def sequence(self) -> typing.Optional[int]:
        r"""The current dispatch sequence number of the shard. This may be None.

        Returns
        -------
        :class:`builtins.int`
        """
        return self._sequence

    def _log(self, level: int, message: typing.Any, *args: typing.Any) -> None:
        _LOGGER.log(level, f"[Shard {self._id}] {message}", *args)

    def _decompress_message(self, message: bytes) -> typing.Any:
        self._buffer.extend(message)
        decomp = self._inflator.decompress(self._buffer) # type: ignore
        self._buffer = bytearray()

        return decomp.decode()

    def _notify_waiters(self):
        # This is a hack to prevent timeout error when initially
        # starting shards.
        self._identified.set()
        self._identified.clear()

    async def _receive(self) -> typing.Any:
        message = await self._websocket.receive() # type: ignore
        message = message.data

        if isinstance(message, bytes):
            if len(message) > 4 and message[-4:] != _ZLIB_SUFFIX:
                return

            message = self._decompress_message(message)

        if isinstance(message, int):
            # Close code more then likely.
            return message

        elif isinstance(message, str):
            try:
                ret = json.loads(message)
            except json.JSONDecodeError:
                # message is not a valid JSON?
                return message
            else:
                return ret

        return False

    async def _heartbeat_handler(self, interval: float):
        self._heartbeat_interval = interval
        self._log(logging.INFO, f"HEARTBEAT task started with interval of {interval} seconds.")

        while True:
            await self._send_heartbeat_packet()
            self._last_heartbeat = time.time()
            await asyncio.sleep(interval)

    async def _handle_recv(self) -> typing.Any:
        packet = await self._receive()

        if not packet:
            return

        if isinstance(packet, int):
            # Close code is sent.
            if not packet in _UNHANDLEABLE_CODES:
                raise _SignalResume(resume=True, delay=None)

            if packet == 4014:
                raise MissingPrivilegedIntents(shard=self)
            else:
                raise ShardCloseException(
                    self,
                    packet,
                    f"Shard closed with unhandleable close code: {packet}"
                )

        if packet is False:
            return False

        op = packet["op"]
        data = packet["d"]

        if op is GatewayOP.HELLO:
            if self._resume_on_connect:
                await self._send_resume_packet()
                self._resume_on_connect = False
            else:
                await self._send_identify_packet()

            interval = data["heartbeat_interval"] // 1000
            self._heartbeat_task = asyncio.create_task(
                self._heartbeat_handler(interval),
                name=f"shard-heartbeat-worker:{self._id}"
            )
            return True



        elif op is GatewayOP.HEARTBEAT_ACK:
            self._latency = time.time() - self._last_heartbeat # type: ignore

        elif op is GatewayOP.DISPATCH:
            self._sequence = packet["s"]

            event = packet["t"]

            if event == "READY":
                self._session_id = data["session_id"]
                self._identified.set()
                self._log(logging.INFO, "Established a new session with Discord gateway. (Session: %s)", self._session_id)

            elif event == "RESUMED":
                self._log(logging.INFO, "Resumed the session %s", self._session_id)

            await self._handle_dispatch(self, event, data)

        elif op is GatewayOP.HEARTBEAT:
            self._log(logging.DEBUG, "Gateway is requesting a HEARTBEAT.")
            await self._send_heartbeat_packet()

        elif op is GatewayOP.INVALID_SESSION:
            if self._session_id is None:
                # If we're here, We more then likely got identify ratelimited
                # this generally should never happen.
                self._notify_waiters()
                self._log(logging.INFO, "Session was prematurely invalidated.")

                raise _SignalResume(resume=False, delay=5.0)

            self._log(logging.INFO, "Session %s has been invalidated. Attempting to RESUME if possible.", self._session_id)
            # NOTE: inner payload (`data`) indicates whether the session is resumeable
            raise _SignalResume(resume=data, delay=5.0)

        elif op is GatewayOP.RECONNECT:
            self._log(logging.INFO, "Gateway has requested to reconnect the shard.")
            raise _SignalResume(resume=True)

        return True

    async def _launch(self, url: str) -> None:
        if self._running:
            raise RuntimeError("Shard is already running")

        self._running = True

        while self._running:
            session = self._rest._ensure_session()

            self._websocket = await session.ws_connect(url)
            self._inflator = zlib.decompressobj()

            while True:
                try:
                    recv = await self._handle_recv()
                except _SignalResume as signal:
                    if signal.delay:
                        self._log(logging.INFO, "Delaying %s seconds before reconnecting.", signal.delay)
                        await asyncio.sleep(signal.delay)

                    self._resume_on_connect = signal.resume
                    await self._close(code=4000)
                    break
                else:
                    if not recv:
                        self._log(logging.INFO, "Shard is closing.")
                        self._running = False
                        return

    async def _wrapped_launch(self, url: str, future: asyncio.Future) -> None:
        try:
            await self._launch(url)
        except Exception as exc:
            self._running = False
            future.set_result(exc)

    async def _close(self, code: int = 1000, _clean: bool = False) -> None:
        if self._heartbeat_task:
            self._heartbeat_task.cancel()
            self._heartbeat_task = None

        if self._websocket:
            await self._websocket.close(code=code)
            self._websocket = None

        if _clean:
            self._clear_gateway_data()
            self._identified.clear()
            self._worker_task.cancel()
            self._running = False
            self._worker_task = None

    async def _send_data(self, data: typing.Dict[str, typing.Any]) -> None:
        await self._websocket.send_str(json.dumps(data)) # type: ignore

    async def _send_heartbeat_packet(self):
        await self._send_data({
            "op": GatewayOP.HEARTBEAT,
            "d": self._sequence,
        })
        self._log(logging.DEBUG, "Sent the HEARTBEAT packet.")

    async def _send_identify_packet(self):
        await self._send_data({
            "op": GatewayOP.IDENTIFY,
            "d": {
                "properties": {
                    "$browser": "Qord",
                    "$device": "Qord",
                    "$os": sys.platform,
                },
                "intents": self._client.intents.value,
                "token": self._rest.token,
                "compress": True,
                "shard": [self._id, self._client.shards_count],
            },
        })
        self._log(logging.DEBUG, "Sent the IDENTIFY packet.")

    async def _send_resume_packet(self):
        await self._send_data({
            "op": GatewayOP.RESUME,
            "d": {
                "session_id": self._session_id,
                "token": self._rest.token,
                "seq": self._sequence,
            },
        })
        self._log(logging.DEBUG, "Sent the RESUME packet.")

