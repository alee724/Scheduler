"""
Alvin Lee

An intermediary module that takes in string arguments and converts them as needed as inputs
to arguments for sheet.py if needed
"""

import json
from ctime import *
from service import *
from customer import *
from sheet import *
import sys

sys.path.insert(0, "scheduler/")


class QueueError(Exception):
    pass


service_path = "../data/services.json"
customer_path = "../data/customers.json"


class Inter:
    def __init__(self, json_dict=None):
        """
        Class for more easily handling data between the front and back end, hopefully
        """
        self.sheet = ScheduleSheet(json_dict=json_dict)
        self.queue = []
        with open(service_path) as file:
            self.services = list(map(lambda s: Service.fromJSON(s), json.load(file)))
        with open(customer_path) as file:
            self.customers = list(map(lambda s: Customer.fromJSON(s), json.load(file)))

    def update_services(self):
        """
        Updates the list of services
        """
        s_lst = list.map(lambda s: Service.toJSON(s), self.services)
        with open(service_path) as file:
            json.dump(s_lst, file)

    def update_customers(self):
        """
        Updates the list of customers
        """
        c_lst = list.map(lambda c: Customer.toJSON(c), self.customers)
        with open(customer_path) as file:
            json.dump(c_lst, file)

    def add_column(self, label):
        """
        Uses the ScheduleSheet.add_column method
        """
        self.sheet.add_column(label)

    def remove_column(self, index):
        """
        Uses the ScheduleSheet.remove_column method
        """
        self.sheet.remove_column(index)

    def queue_customer(self, first, last, services, phone, default):
        """
        Creates a customer from string arguments and adds them to a queue
        """
        s_set = set(filter(lambda s: s.getName() in services, self.services))
        c = Customer(first, last, s_set, phone)
        if phone not in list(map(lambda c: c.getPhone(), self.customers)):
            self.customers.append(c)
            self.update_customers()
        self.queue.append(c)

    def add_customer(self, col, row, customer):
        """
        Adds a customer from the queue
        """
        try:
            self.queue.remove(customer)
            self.sheet.add_customer(col, row, customer)
        except ValueError:
            raise QueueError

    def move_customer(self, icol, irow, fcol, frow):
        """
        Uses the ScheduleSheet.move_customer method
        """
        self.sheet.move_customer(icol, irow, fcol, frow)

    def set_customer_services(self, col, row, services):
        """
        Uses the ScheduleSheet.set_customer_services method
        """
        for s in services:
            assert s in self.services
        self.sheet.set_customer_services(col, row, set(services))

    def add_service(self, name, price, time, abb):
        """
        Takes in string
        """
        t = CTime(int(time[0]), int(time[1]))
        s = Service(name, int(price), t, abb)
        self.services.append(s)
        self.update_services()
