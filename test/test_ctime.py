import unittest
import sys

sys.path.insert(0, "../lib/scheduler/")
from ctime import *


class TestTime(unittest.TestCase):
    def test_init(self):
        x = CTime()
        self.assertEqual(x.getHour(), 0)
        self.assertEqual(x.getMinute(), 0)
        x = CTime(1, 1)
        self.assertEqual(x.getHour(), 1)
        self.assertEqual(x.getMinute(), 1)
        x = CTime(23, 59)
        self.assertEqual(x.getHour(), 23)
        self.assertEqual(x.getMinute(), 59)

    def test_eq(self):
        x = CTime()
        self.assertEqual(x, CTime())
        x = CTime(1, 1)
        self.assertEqual(x, CTime(1, 1))
        x = CTime(23, 59)
        self.assertEqual(x, CTime(23, 59))

    def test_add(self):
        x = CTime()
        x.add(CTime(1, 1))
        self.assertEqual(x.toString(), "01:01")
        x.add(CTime(22, 58))
        self.assertEqual(x.toString(), "23:59")
        x.add(CTime(0, 1))
        self.assertEqual(x, CTime())

        y = CTime()
        y.add_time(1, 1)
        self.assertEqual(y.toString(), "01:01")
        y.add_time(22, 58)
        self.assertEqual(y.toString(), "23:59")
        y.add_time(0, 1)
        self.assertEqual(y.toString(), "00:00")

    def test_minutes(self):
        x = CTime()
        self.assertEqual(x.asMinutes(), 0)
        x.add_time(1, 1)
        self.assertEqual(x.asMinutes(), 61)
        x.add_time(22, 58)
        self.assertEqual(x.asMinutes(), 1439)
        x.add_time(0, 1)
        self.assertEqual(x.asMinutes(), 0)


if __name__ == "__main__":
    unittest.main()
