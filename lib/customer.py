from ctime import *
from service import *


class Customer:
    def __init__(self, first, last, services={}, phone="0000000000"):
        """
        Creates the customer class that contains the information regarding what services a customer
        wants, their name, and phone number

        @parameter first: string
        @parameter last: string
        @parameter services: a set of Service objects
        @parameter phone: a string of length 10
        """
        assert isinstance(first, str) and isinstance(last, str)
        assert len(phone) == 10
        for s in services:
            assert isinstance(s, Service)
        self.first = first
        self.last = last
        self.services = services
        self.phone = phone

        # sets time to default 0000 and then updates the time according to the services
        self.time = CTime()
        self.update_time()

    def update_time(self):
        """
        Helper function that modifies the time according to the current set of services
        """
        res = CTime()
        for s in self.services:
            res.add(s.getTime())
        self.time = res

    def add_service(self, service):
        """
        Adds a service to the set of services

        @parameter service: a Service object
        """
        assert isinstance(service, Service)
        set.add(self.services, service)
        self.update_time()

    def remove_service(self, service):
        """
        Removes [service] from the set of services
        """
        assert isinstance(service, Service)
        set.remove(self.services, service)
        self.update_time()

    # ========== Get and Set methods ==========

    def getName(self):
        """
        Returns the full name
        """
        return f"{self.first} {self.last}"

    def getFirst(self):
        """
        Returns the first name
        """
        return self.first

    def getLast(self):
        """
        Returns the last name
        """
        return self.last

    def getServices(self):
        """
        Returns a set of services
        """
        return self.services

    def getTime(self):
        """
        Returns the time
        """
        return self.time

    def setName(self, first=None, last=None):
        """
        Sets the first and last name to [first] and [last]

        @parameter first: string if provided else None
        @parameter last: string if provided else None
        """
        assert first == None or isinstance(first, str)
        assert last == None or isinstance(last, str)
        self.first = first if first != None else self.first
        self.last = last if last != None else self.last
