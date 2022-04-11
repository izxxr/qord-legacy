from qord.internal import helpers
import datetime
import unittest

class TestInternalHelpers(unittest.TestCase):
    def test_compute_creation_time(self) -> None:
        snowflake = 175928847299117063
        creation_time = datetime.datetime(2016, 4, 30, 11, 18, 25, 796000, datetime.timezone.utc)

        assert helpers.compute_creation_time(snowflake) == creation_time
