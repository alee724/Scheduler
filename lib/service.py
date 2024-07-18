from ctime import *


class Service:
    def __init__(self, name, price, time_span, abb=""):
        """
        Creates a class for services containing all the necessary information for the scheduler

        @parameter name: string
        @parameter price: non-negative integer
        @parameter time_span: a CTime object
        @parameter abb: optional string argument that represents the abbreviation for the name
        """
        assert (
            isinstance(name, str)
            and isinstance(price, int)
            and isinstance(time_span, CTime)
            and isinstance(abb, str)
        )
        assert price >= 0
        self.name = name
        self.price = price
        self.time = time_span
        self.abbrev = abb

    # ========== Get and Set methods ==========
    def getName(self):
        """
        Returns the name
        """
        return self.name

    def getPrice(self):
        """
        Returns the price
        """
        return self.price

    def getTime(self):
        """
        Returns the time
        """
        return self.time

    def getAbbrev(self):
        """
        Returns the abbreviation
        """
        return self.abbrev

    def setName(self, new):
        """
        Sets the name as [new]
        """
        assert isinstance(new, str)
        self.name = new

    def setPrice(self, new):
        """
        Sets the price to [new]
        """
        assert isinstance(new, int) and new >= 0
        self.price = new

    def setTime(self, hour, minute):
        """
        Sets the time to a new [hour] and [minute]
        """
        self.time.setTime(hour, minute)

    def setAbbrev(self, new):
        """
        Sets the abbrevitaion to new
        """
        self.abbrev = new
