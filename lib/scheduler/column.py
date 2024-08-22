"""
Alvin Lee
July 17, 2024

This module is responsible for managing what items can be placed and what items can not due to
size restrictions or overlaps
"""

from customer import *


class Lst:
    def __init__(self, length, placeholder):
        """
        Initializes a custom list class of some length with the contents being filled with a
        placeholder

        @parameter length: the integer length of the list
        @parameter placeholder: the default contents of the list
        """
        assert length >= 0
        self.length = length
        tmp = []
        for i in range(length):
            list.append(tmp, placeholder)
        self.contents = tmp

    def check(self):
        """
        Checks if the length of the list exceeds initialized length

        If yes, raises an IrregularLength exception
        """
        if len(self.contents) > self.length:
            raise IrregularLength


class BadArgument(Exception):
    """
    Exception for when a bad argument was given causing an error
    """

    pass


class BadIndex(BadArgument):
    """
    Exception for a faulty index when accessing a list
    """


pass


class Column(Lst):
    def __init__(self, label, rows=1):
        """
        Initializes a column using the Lst parent class

        @parameter label: a string label given to the column
        @parameter rows: is the integer number of rows that the column should contain
        """
        assert isinstance(label, str)
        super().__init__(rows, None)
        self.label = label
        self.num_items = 0

    def toJSON(self):
        """
        Returns a json file representation for a column
        """
        item_json_list = []
        if self.num_items != 0:
            for i in range(len(self.contents)):
                if self.contents[i] in [None, 0]:
                    continue
                else:
                    list.append(
                        item_json_list,
                        (i, self.contents[i].toJSON(), self.contents[i].size),
                    )
        json = {
            "label": self.label,
            "items": item_json_list,
        }
        return json

    def fromJSON(self, numRows=1):
        """
        Returns a Column object from a json
        """
        if isinstance(self, str):
            import json

            self = json.loads(self)
        col = Column(self["label"], rows=numRows)
        for item in self["items"]:
            col.add_item(item[0], Customer.fromJSON(item[1]), item[2])
        return col

    def get_item(self, index):
        """
        Helper method that gets the item at some index
        """
        assert isinstance(index, int)
        ind = self.get_index(index)
        return self.contents[ind]

    def add_item(self, index, item, size=1):
        """
        Modifies self.contents by adding an item of some size to the list

        Raises a BadArgument exception if there is an overlap between existing items and the
        newly added one

        @parameter index: an integer
        @parameter item: the item to be added to the list at some index
        @parameter size: the positive integer that is the length of item to be inserted to the list
        """
        assert size > 0
        assert index < len(self.contents)
        assert len(self.contents) - size >= index
        for i in range(index, index + size):
            if self.contents[i] != None:
                raise BadArgument
        self.contents[index] = item
        # this is here for testing reasons and we can't attach attributes to ints, bools, etc.
        if isinstance(item, Customer):
            item.size = size
        for i in range(index + 1, index + size):
            self.contents[i] = 0
        self.check()
        self.num_items += 1

    def get_index(self, index):
        """
        A helper function that will obtain the poition of the item at some index.
        Assumes the item exists
        """
        while self.contents[index] == 0:
            index -= 1
        return index

    def remove_item(self, index):
        """
        Removes an item specified at an index and raises an exception if there is no item
        at the specified index

        @parameter index: a integer
        """
        assert isinstance(index, int)
        assert index <= len(self.contents)

        # remove the item first
        if self.contents[index] not in [None, 0]:
            self.contents[index] = None
        elif self.contents[index] != None:
            index = self.get_index(index)
            self.contents[index] = None
        else:
            raise BadIndex

        # remove placeholders
        index += 1
        if len(self.contents) > index:
            for i in range(index, len(self.contents)):
                if self.contents[i] == 0:
                    self.contents[i] = None
                else:
                    break
        self.check()
        self.num_items -= 1

    # ========== Set and Get methods ==========

    def setLabel(self, new_name):
        """
        Sets the current label to a new label
        """
        assert isinstance(new_name, str)
        self.label = new_name

    def getLabel(self):
        """
        Gets the label
        """
        return self.label

    def getItem(self, index):
        """
        Gets the item located approximately at index
        """
        if self.contents[index] != None:
            item_index = self.get_index(index)
            return self.contents[item_index]
        return None

    def getNumItems(self):
        """
        Returns the number of items in the column
        """
        return self.num_items
