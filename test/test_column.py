import unittest
import sys

sys.path.insert(0, "../lib/")
from column import *


class TestLst(unittest.TestCase):
    def test_check(self):
        a = Lst(5, True)
        b = Lst(5, 1.0)
        c = Lst(5, None)
        d = Lst(5, 1)
        e = Lst(5, "")
        self.assertEqual(5, len(a.contents))
        self.assertEqual(5, len(b.contents))
        self.assertEqual(5, len(c.contents))
        self.assertEqual(5, len(d.contents))
        self.assertEqual(5, len(e.contents))

    def test_make(self):
        a = Lst(5, True)
        b = Lst(5, 1.0)
        c = Lst(5, None)
        d = Lst(5, 1)
        e = Lst(5, "")

        for i in a.contents:
            self.assertTrue(i == True)
        for i in b.contents:
            self.assertTrue(i == 1.0)
        for i in c.contents:
            self.assertTrue(i == None)
        for i in d.contents:
            self.assertTrue(i == 1)
        for i in e.contents:
            self.assertTrue(i == "")


class TestColumn(unittest.TestCase):
    def test_add(self):
        a = Column("", rows=5)
        a.add_item(0, 1)
        a.add_item(2, True)
        a.add_item(4, 2.0)
        self.assertEqual(a.contents[0], 1)
        self.assertEqual(a.contents[1], None)
        self.assertEqual(a.contents[2], True)
        self.assertEqual(a.contents[3], None)
        self.assertEqual(a.contents[4], 2.0)

    def test_remove(self):
        a = Column("", rows=5)
        a.add_item(0, True, size=2)
        a.add_item(4, True)
        a.remove_item(1)
        self.assertEqual(a.contents, [None, None, None, None, True])
        try: 
            a.remove_item(1)
        except BadIndex: pass
        a.remove_item(4)
        self.assertEqual(a.contents, [None, None, None, None, None])

    def test_label(self):
        a = Column("")
        self.assertEqual(a.getLabel(), "")
        a.setLabel("test")
        self.assertEqual(a.getLabel(), "test")


if __name__ == "__main__":
    unittest.main()
