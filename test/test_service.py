import sys
sys.path.insert(0, "../lib/")
from ctime import *
from service import *
import unittest



class TestService(unittest.TestCase):
    def test_init(self):
        s = Service("Pedi", 28, CTime(1, 0), abb="P")
        self.assertEqual(s.getName(), "Pedi")
        self.assertEqual(s.getTime(), CTime(1, 0))
        self.assertEqual(s.getPrice(), 28)
        self.assertEqual(s.getAbbrev(), "P")

        s = Service("Mani", 20, CTime(0, 30), abb="M")
        self.assertEqual(s.getName(), "Mani")
        self.assertEqual(s.getTime(), CTime(0, 30))
        self.assertEqual(s.getPrice(), 20)
        self.assertEqual(s.getAbbrev(), "M")

    def test_set(self):
        s = Service("Mani", 20, CTime(0, 30), abb="M")
        s.setName("test")
        s.setPrice(69)
        s.setTime(23, 59)
        s.setAbbrev("Poo")
        self.assertEqual(s.getAbbrev(), "Poo")
        self.assertEqual(s.getPrice(), 69)
        self.assertEqual(s.getTime(), CTime(23, 59))
        self.assertEqual(s.getName(), "test")


if __name__ == "__main__":
    unittest.main()
