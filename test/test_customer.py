import sys

sys.path.insert(0, "../lib/")
from customer import *
import unittest
from service import *
from ctime import *

global s1, s2, s3, s4, s5
s1 = Service("P", 10, CTime(0, 30))
s2 = Service("M", 20, CTime(0, 30))
s3 = Service("G", 18, CTime(1, 0))
s4 = Service("W", 28, CTime(0, 15))
s5 = Service("S", 30, CTime(1, 0))


class TestCustomer(unittest.TestCase):
    def test_init(self):
        c = Customer("a", "l", {s1, s2, s3})
        self.assertEqual(c.getName(), "a l")
        self.assertEqual(c.getTime(), CTime(2, 0))
        self.assertEqual(c.getServices(), {s1, s2, s3})

        c = Customer("bryan", "lee", {s2, s3, s5})
        self.assertEqual(c.getName(), "bryan lee")
        self.assertEqual(c.getTime(), CTime(2, 30))
        self.assertEqual(c.getServices(), {s2, s3, s5})

    def test_add(self):
        c = Customer("a", "l", {s1})
        self.assertEqual(c.getTime(), CTime(0, 30))
        c.add_service(s1)
        self.assertEqual(c.getTime(), CTime(0, 30))
        c.add_service(s2)
        self.assertEqual(c.getTime(), CTime(1, 0))
        c.add_service(s5)
        self.assertEqual(c.getTime(), CTime(2, 0))

    def test_remove(self):
        c = Customer("a", "l", {s1, s2, s3, s4, s5})
        c.remove_service(s1)
        self.assertEqual(c.getServices(), {s2, s3, s4, s5})
        c.remove_service(s2)
        self.assertEqual(c.getServices(), {s3, s4, s5})
        c.remove_service(s3)
        self.assertEqual(c.getServices(), {s4, s5})
        c.remove_service(s4)
        self.assertEqual(c.getServices(), {s5})
        c.remove_service(s5)
        self.assertEqual(c.getServices(), set())

    def test_name(self):
        c = Customer("a", "l", {s1, s2, s3, s4, s5})
        self.assertEqual(c.getName(), "a l")
        c.setName()
        self.assertEqual(c.getName(), "a l")
        c.setName(first="b")
        self.assertEqual(c.getName(), "b l")
        c.setName(first="a", last="c")
        self.assertEqual(c.getName(), "a c")


if __name__ == "__main__":
    unittest.main()
