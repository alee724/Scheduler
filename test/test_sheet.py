from sheet import *
from ctime import *
from service import *
import unittest
from customer import *
import sys

sys.path.insert(0, "../lib/scheduler/")

s1 = Service("P", 18, CTime(0, 30))
s2 = Service("M", 20, CTime(0, 30))
s3 = Service("W", 40, CTime(0, 15))
s4 = Service("E", 50, CTime(1, 10))
s5 = Service("L", 30, CTime(1, 0))
c1 = Customer("a", "l", {s1, s2})
c2 = Customer("b", "m", {s1, s2, s5})
c3 = Customer("c", "n", {s5})
c4 = Customer("d", "o", {s3, s4})
c5 = Customer("e", "p", {s1, s2, s3, s4, s5})


class TestGrid(unittest.TestCase):
    def test_add_columns(self):
        x = Grid()
        self.assertEqual(x.getLength(), 0)
        x.add_column("")
        self.assertEqual(x.getLength(), 1)
        x.add_column("")
        self.assertEqual(x.getLength(), 2)
        x.add_column("")
        self.assertEqual(x.getLength(), 3)
        x.add_column("")
        self.assertEqual(x.getLength(), 4)
        x.add_column("")
        self.assertEqual(x.getLength(), 5)
        x.add_column("")
        self.assertEqual(x.getLength(), 6)
        x.add_column("")
        self.assertEqual(x.getLength(), 7)
        x.add_column("")
        self.assertEqual(x.getLength(), 8)
        x.add_column("")
        self.assertEqual(x.getLength(), 9)
        x.add_column("")
        self.assertEqual(x.getLength(), 10)
        x.add_column("")
        self.assertEqual(x.getLength(), 11)
        x.add_column("")
        self.assertEqual(x.getLength(), 12)
        x.add_column("")
        self.assertEqual(x.getLength(), 13)

    def test_remove_columns(self):
        x = Grid()
        self.assertEqual(x.getLength(), 0)
        x.add_column("")
        self.assertEqual(x.getLength(), 1)
        x.add_column("")
        self.assertEqual(x.getLength(), 2)
        x.add_column("")
        self.assertEqual(x.getLength(), 3)

        c1 = x.getColumn(0)
        c1.add_item(0, "test")
        try:
            x.remove_column(0)
            raise Exception
        except NonemptyColumnException:
            pass
        x.remove_column(1)
        self.assertEqual(x.getLength(), 2)
        x.remove_column(1)
        self.assertEqual(x.getLength(), 1)


class TestSheet(unittest.TestCase):
    def test_init(self):
        x = ScheduleSheet()
        x.add_column("")
        self.assertEqual(x.getInterval(), 15)
        self.assertEqual(x.getStart(), CTime(8, 0))
        self.assertEqual(x.getEnd(), CTime(20, 0))

    def test_time_to_len(self):
        x = ScheduleSheet()
        x.add_column("")
        self.assertEqual(x.time_to_length(CTime(1, 0)), 4)
        self.assertEqual(x.time_to_length(CTime(1, 5)), 4)
        self.assertEqual(x.time_to_length(CTime(1, 10)), 5)
        self.assertEqual(x.time_to_length(CTime(23, 59)), 96)

    def test_add_customer(self):
        x = ScheduleSheet(start_time=0, end_time=1)
        x.add_column("")
        x.add_customer(0, 0, c1)
        try:
            x.add_customer(0, 1, c2)
        except BadArgument:
            pass
        y = ScheduleSheet(start_time=0, end_time=4)
        y.add_column("")
        y.add_customer(0, 4, c2)
        try:
            y.add_customer(0, 1, c1)
        except BadArgument:
            pass
        y.add_customer(0, 0, c1)

    def test_move_customer(self):
        x = ScheduleSheet(start_time=0, end_time=4)
        x.add_column("")
        x.add_customer(0, 0, c1)
        x.add_customer(0, 4, c2)
        try:
            x.move_customer(0, 3, 0, 1)
            raise Exception
        except CustomerOverlap:
            pass
        try:
            x.move_customer(0, 13, 0, 1)
            raise Exception
        except BadIndex:
            pass
        x.move_customer(0, 3, 0, 12)

        x.add_column("")
        x.move_customer(0, 13, 1, 0)

    def test_remove_customer(self):
        x = ScheduleSheet(start_time=0, end_time=4)
        x.add_column("")
        x.add_customer(0, 0, c1)
        x.add_customer(0, 4, c2)
        x.add_column("")
        x.add_customer(1, 2, c5)
        x.remove_customer(0, 3)
        x.remove_customer(0, 4)
        x.remove_customer(1, 15)

    def test_split_customer(self):
        x = ScheduleSheet(start_time=0, end_time=4)
        x.add_column("")
        x.add_customer(0, 0, c1)
        x.add_customer(0, 4, c2)
        x.add_column("")
        x.add_customer(1, 2, c5)
        x.split_customer(0, 0, {s1})
        x.split_customer(1, 2, {s3, s5})
        col1 = x.getColumn(0)
        col2 = x.getColumn(1)
        self.assertEqual(col1.getNumItems(), 3)
        self.assertEqual(col2.getNumItems(), 2)

    def test_set_services(self):
        x = ScheduleSheet(start_time=0, end_time=4)
        x.add_column("")
        x.add_customer(0, 0, c1)
        x.add_customer(0, 4, c2)
        x.add_column("")
        x.set_customer_services(0, 0, {s1, s2, s3})
        x.set_customer_services(0, 4, {s1})


if __name__ == "__main__":
    unittest.main()
