import sys

sys.path.insert(0, "../lib/")
from gross import *
import unittest
sys.path.insert(0, "../lib/scheduler/")
from sheet import *


s1 = Service("P", 18, CTime(0, 30))
s2 = Service("M", 20, CTime(0, 30))
s3 = Service("W", 40, CTime(0, 15))
s4 = Service("E", 50, CTime(1, 10))
s5 = Service("L", 30, CTime(1, 0))
c1 = Customer("a", "l", [s1, s2])
c2 = Customer("b", "m", [s1, s2, s5])
c3 = Customer("c", "n", [s5])
c4 = Customer("d", "o", [s3, s4])
c5 = Customer("e", "p", [s1, s2, s3, s4, s5])


class TestGross(unittest.TestCase):
    def test_getTotal(self):
        x = ScheduleSheet()
        x.add_column("")
        x.setColumnName(0, "column 1")
        x.add_column("column 2")
        x.add_customer(0, 0, c1)
        x.add_customer(0, 6, c2)
        x.add_customer(1, 4, c3)
        x.add_customer(1, 8, c4)
        x.add_column("test")
        x.add_column("test")
        x.add_column("test")
        x.add_column("test")
        x.add_column("test")
        x.add_column("column 3")
        x.add_customer(7, 0, c5)
        j = x.toJSON()
        self.assertEqual(getPrice(j), 384)

    def test_empty(self):
        x = ScheduleSheet()
        j = x.toJSON()
        self.assertEqual(getPrice(j), 0)


if __name__ == "__main__":
    unittest.main()
