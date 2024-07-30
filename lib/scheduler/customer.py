"""
Alvin Lee

This module is responsible for what data a customer would need and how to obtain that data and
manipulate it if needed
"""

from ctime import *
from service import *


class Customer:
    def __init__(self, first, last, services=[], phone="0000000000", served=False):
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
            assert services.count(s) == 1
        self.first = first
        self.last = last
        self.services = services
        self.phone = phone
        self.served = served

        # sets time to default 0000 and then updates the time according to the services
        self.time = CTime()
        self.update_time()

    def __eq__(self, o):
        """
        Two customers are equal if and only if their name and number are the same
        """
        try:
            assert isinstance(o, Customer)
        except AssertionError:
            return False
        if self.first == o.first and self.last == o.last and self.phone == o.phone:
            return True
        return False

    def toJSON(self):
        services_json_list = []
        for s in self.services:
            list.append(services_json_list, s.toJSON())
        json = {
            "first": self.first,
            "last": self.last,
            "services": services_json_list,
            "phone": self.phone,
            "served": self.served,
        }
        return json

    def fromJSON(self):
        if isinstance(self, str):
            import json

            self = json.loads(self)
        services = []
        for s in self["services"]:
            services.append(Service.fromJSON(s))
        return Customer(
            self["first"], self["last"], services, self["phone"], self["served"]
        )

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
        try:
            assert self.services.count(service) == 0
            list.append(self.services, service)
            self.update_time()
        except AssertionError:
            pass

    def remove_service(self, service):
        """
        Removes [service] from the set of services
        """
        assert isinstance(service, Service)
        list.remove(self.services, service)
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

    def getPhone(self):
        """
        Returns the phone number
        """
        return self.phone

    def getServed(self):
        """
        Returns whether the customer has been served or not
        """
        return self.served

    def setServed(self, new):
        """
        Sets a new boolean value for served
        """
        assert isinstance(new, bool)
        self.served = new

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
