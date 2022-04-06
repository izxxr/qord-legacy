"""Tests for qord.Flags"""

from qord.flags.base import Flags

import unittest

class Permissions(Flags):
    send_messages = 1 << 0
    read_message_history = 1 << 1
    view_channel = 1 << 2
    manage_messages = 1 << 3
    manage_channels = 1 << 4

class TestFlags(unittest.TestCase):
    def test_value(self) -> None:
        flags = Permissions(send_messages=True, manage_messages=True, manage_channels=False)
        assert flags.value == (Permissions.send_messages | Permissions.manage_messages)

        flags.value = (Permissions.send_messages | Permissions.manage_channels)

        assert flags.send_messages
        assert flags.manage_channels

        flags.view_channel = True

        assert flags.value == (
            Permissions.send_messages
            | Permissions.manage_channels
            | Permissions.view_channel
        )

        flags.view_channel = False

        assert flags.value == (
            Permissions.send_messages
            | Permissions.manage_channels
        )


    def test_comparison(self) -> None:
        flags = Permissions(send_messages=True, manage_messages=True)
        assert flags == Permissions(send_messages=True, manage_messages=True)
        assert flags > Permissions(send_messages=True)
        assert flags < Permissions(send_messages=True, manage_messages=True, manage_channels=True)

if __name__ == "__main__":
    unittest.main()