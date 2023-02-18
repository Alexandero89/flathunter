import unittest
from unittest import mock
import datetime
from datetime import time
from datetime import datetime as dt

from flathunter.time_utils import is_current_time_between, get_diff_in_secs, wait_during_period


class TimeUtilsTest(unittest.TestCase):

    def test_diff(self):
        self.assertEqual(get_diff_in_secs(time.fromisoformat("11:42:23"), time.fromisoformat("12:42:23")), 3600)
        self.assertEqual(get_diff_in_secs(time.fromisoformat("12:42:23"), time.fromisoformat("11:42:23")), 3600)

    @mock.patch("flathunter.time_utils.datetime", side_effect=lambda *args, **kw: datetime(*args, **kw))
    def test_is_current_time_between(self, mock_datetime):
        mock_datetime.now.side_effect = [
            dt.fromisoformat("2023-01-01 07:42"),
            dt.fromisoformat("2023-01-01 08:42"),
            dt.fromisoformat("2023-01-01 10:42"),
            dt.fromisoformat("2023-01-01 11:42"),
            dt.fromisoformat("2023-01-01 11:42"),
        ]

        self.assertTrue(is_current_time_between(time.fromisoformat("22:00"), time.fromisoformat("08:00")))
        self.assertFalse(is_current_time_between(time.fromisoformat("22:00"), time.fromisoformat("08:00")))
        self.assertTrue(is_current_time_between(time.fromisoformat("10:20"), time.fromisoformat("11:20")))
        self.assertFalse(is_current_time_between(time.fromisoformat("10:20"), time.fromisoformat("11:20")))
        self.assertFalse(is_current_time_between(time.fromisoformat("11:20"), time.fromisoformat("11:20")))

    @mock.patch("flathunter.time_utils.sleep")
    @mock.patch("flathunter.time_utils.datetime", side_effect=lambda *args, **kw: datetime(*args, **kw))
    def test_wait_during_period(self, mock_datetime, mock_sleep):
        mock_datetime.now.return_value = dt.fromisoformat("2023-01-01 10:01")

        wait_during_period(time.fromisoformat("22:00"), time.fromisoformat("11:00"))
        self.assertEqual(mock_sleep.call_args[0][0], 3540)

        mock_sleep.reset_mock()
        wait_during_period(time.fromisoformat("11:00"), time.fromisoformat("11:00"))
        self.assertFalse(mock_sleep.called)

