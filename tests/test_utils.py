"""Tests for qord.utils"""

from qord import utils, TimestampStyle

from datetime import datetime
import unittest


class TestUtils(unittest.TestCase):
    def test_create_timestamp(self) -> None:
        # March 27 2022, 15:07:43
        time_datetime = datetime(2022, 3, 27, 15, 7, 43)
        time_epoch = round(time_datetime.timestamp())

        timestamp = f"<t:{time_epoch}>"
        timestamp_styled = f"<t:{time_epoch}:{TimestampStyle.RELATIVE_TIME}>"

        assert utils.create_timestamp(time_datetime) == timestamp
        assert utils.create_timestamp(time_epoch) == timestamp
        assert utils.create_timestamp(time_datetime, TimestampStyle.RELATIVE_TIME) == timestamp_styled


if __name__ == "__main__":
    unittest.main()