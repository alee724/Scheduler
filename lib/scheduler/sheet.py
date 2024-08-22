"""
Alvin Lee

This module utilizes all the other modules in the scheduler/ directory and creates a spreadsheet
that keeps track of where customers are, which employees have which customer, etc.
"""

from column import *
from ctime import *
import json
from customer import *
from ctime import *


class NonemptyColumnException(Exception):
    pass


class Grid:
    def __init__(self, cols=0, numRows=1):
        """
        Creates a Grid class with a at least one default column with some positive number of rows

        @parameter cols: positive integer
        @parameter numRows: positive integer
        """
        assert isinstance(cols, int)
        assert isinstance(numRows, int)
        assert cols >= 0 and numRows > 0

        self.columns = []
        self.length = 0
        self.numRows = numRows

    def add_column(self, label):
        """
        Modifies the list by using the list.append method to add a Column to the grid

        Returns True if the column can be added else False

        @parameter label: a string
        """
        assert isinstance(label, str)
        for col in self.columns:
            if col.label == label:
                return False
        list.append(self.columns, Column(label, self.numRows))
        self.length += 1
        return True

    def remove_column(self, label):
        """
        Modifies the list by removing a Column from the list using the list.pop method
        The column MUST be empty in order for it to be removed

        Returns True if the column can and is now removed, else returns False

        @parameter label: the string label on the column
        """
        assert isinstance(index, int)
        assert index <= len(self.columns)
        for col in self.columns:
            if col.label == label:
                if col.getNumItems() == 0:
                    list.pop(self.columns, index)
                    self.length -= 1
                    return True
                else:
                    return False
        else:
            raise NonemptyColumnException
            return False

    # ========== Set and Get methods ==========
    def getColumn(self, index):
        """
        Gets the column at index
        """
        assert isinstance(index, int)
        assert index < self.length
        return self.columns[index]

    def getLength(self):
        """
        Gets the total number of columns
        """
        return self.length

    def getNumRows(self):
        """
        Gets the number of rows
        """
        return self.numRows


class CustomerOverlap(Exception):
    pass


class ScheduleSheet(Grid):
    def __init__(self, start_time=8, end_time=20, interval=15, json_dict=None):
        """
        Creates a ScheduleSheet class that has an initial start and end time with some integer
        minute intervals between them

        @parameter numRows: integer number of rows in the sheet
        @parameter start_time: integer representation of the starting hour, less than end_time
        @parameter end_time: integer representation of the ending hour, greater than start_time
        @parameter interval: integer interval between start and end times, should equally divide
                             the time between start and end times an integer number of times

        e.g.
        start_time = 0, end_time = 1, interval = 15 is allowed as 60minutes is evenly divided
        by 15 minutes

        start_time = 0, end_time = 1, interval = 13 is not allowed
        """
        if json_dict == None:
            super().__init__(numRows=(end_time - start_time) * 60 // 15)
            assert isinstance(start_time, int)
            assert isinstance(interval, int)
            assert isinstance(end_time, int)
            assert end_time > start_time
            assert interval > 0
            assert ((end_time - start_time) * 60) % interval == 0

            self.start = CTime(hour=start_time)
            self.end = CTime(hour=end_time)
            self.interval = interval
        else:  # what should occur when there is a json attached
            dictionary = json.loads(json_dict)
            super().__init__(
                numRows=(dictionary["end"] - dictionary["start"]) * 60 // 15
            )
            self.start = CTime(hour=dictionary["start"])
            self.end = CTime(hour=dictionary["end"])
            self.interval = dictionary["interval"]
            self.fromJSON(dictionary["columns"])

        # create a variable for queueing customers although it will not be saved
        self.queue = 0

    def toJSON(self):
        """
        Converts the schedule sheet to a json script
        """
        column_json_list = []
        for c in self.columns:
            list.append(column_json_list, c.toJSON())
        json_dict = {
            "start": self.start.getHour(),
            "end": self.end.getHour(),
            "interval": self.interval,
            "columns": column_json_list,
        }
        return json_dict

    def fromJSON(self, column_lst):
        columns = []
        for col in column_lst:
            list.append(columns, Column.fromJSON(col, self.numRows))
        self.columns = columns
        self.length = len(self.columns)

    def time_to_length(self, time):
        """
        Helper method to convert a CTime object into index length where each unit length is of
        self.interval minutes
        """
        assert isinstance(time, CTime)
        min = time.asMinutes()
        len = min // self.interval
        rem = (min % self.interval) / self.interval
        return len + round(rem)

    def add_customer(self, col, row, customer):
        """
        Modifies the sheet by adding [customer] to the [index] column where the customer takes up
        some [time_span] amount of time

        @parameter col: non-negative integer
        @parameter row: non-negative integer
        @parameter customer: the customer to be added to the schedule
        """
        try:
            assert isinstance(col, int)
            assert isinstance(row, int)
            assert col >= 0 and row >= 0
            assert col <= self.length
        except:
            return False
        column = self.getColumn(col)
        column.add_item(row, customer, self.time_to_length(customer.getTime()))
        return True

    def serve_customer(self, col, row):
        """
        Helper method for changing the state of a customer's served attribute from False to True
        """
        column = self.getColumn(col)
        customer = column.get_item(row)
        customer.served = not customer.served
        return customer.served

    def move_customer(self, icol, irow, fcol, frow):
        """
        Modifies the sheet by moving a customer in column [icol] located at approximately [irow]
        to column [fcol] at time [frow].

        If there is no customer at the specified location then a BadIndex Exception is raised
        If there is an overlap then a CustomerOverlap Exception is raised

        @parameter icol: integer
        @parameter fcol: integer
        @parameter irow: integer
        @parameter frow: integer
        """
        try:
            assert isinstance(icol, int)
            assert isinstance(irow, int)
            assert isinstance(fcol, int)
            assert isinstance(frow, int)
        except:
            raise BadArgument
            return False
        i_column = self.getColumn(icol)
        f_column = self.getColumn(fcol)
        customer = i_column.getItem(irow)
        if customer != None:
            try:
                i_column.remove_item(irow)
                f_column.add_item(
                    frow, customer, self.time_to_length(customer.getTime())
                )
                return True
            except:
                i_column.add_item(
                    irow, customer, self.time_to_length(customer.getTime())
                )
                raise CustomerOverlap
                return False
        else:
            raise BadIndex
        return False

    def remove_customer(self, col, row):
        """
        Modifies the sheet by removing a customer at some column and row

        @parameter col: integer
        @parameter row: integer
        """
        assert isinstance(col, int)
        assert isinstance(row, int)
        assert col <= self.length
        column = self.getColumn(col)
        customer = column.getItem(row)
        if customer != None:
            column.remove_item(row)
            return True
        return False

    def split_customer(self, col, row, services):
        """
        Modifies a customer at some col and row and creates a new customer with the same attributes
        such that the old customer transfers one or more services to the new customer

        @parameter col: int representing the column index
        @parameter row: int representing the row index
        @parameter services: the set of services that are to be transferred to the new customer

        Requires that the input set of services is a proper subset the customer set of services
        """
        assert isinstance(col, int)
        assert isinstance(row, int)
        assert isinstance(services, list)
        assert col <= self.length

        column = self.getColumn(col)
        customer = column.getItem(row)
        if customer != None:
            assert 0 < len(services) < len(customer.getServices())
            for s in services:
                assert s in customer.getServices()
            for s in services:
                customer.remove_service(s)
            ind = column.get_index(row)
            column.remove_item(ind)
            new_customer = Customer(
                customer.getFirst(), customer.getLast(), services, customer.getPhone()
            )
            new_size = self.time_to_length(customer.getTime())
            column.add_item(ind, customer, new_size)
            self.add_customer(col, ind + new_size, new_customer)

    def set_customer_services(self, col, row, services=None):
        """
        Uses the Customer.setServices method to replace the set of services for a customer

        @parameter col: int representing the column index
        @parameter row: int representing the row index
        @parameter services: the set of services that will replace the current set of services
                             for a customer at col, row
        """
        if services == None:
            pass
        else:
            assert isinstance(col, int)
            assert isinstance(row, int)
            assert isinstance(services, list)

            for s in services:
                assert isinstance(s, Service)
            column = self.getColumn(col)
            customer = column.getItem(row)
            ind = column.get_index(row)
            self.remove_customer(col, row)
            try:
                self.add_customer(
                    col,
                    ind,
                    Customer(
                        customer.getFirst(),
                        customer.getLast(),
                        services,
                        customer.getPhone(),
                    ),
                )
            except BadArgument:
                self.add_customer(col, ind, customer)

    def toString(self):
        """
        Converts the grid into a visible representation
        """
        tmp = list(map(lambda x: x.contents, self.columns))
        transposed = list(zip(*tmp))
        for row in transposed:
            string = ""
            for item in row:
                if item == None:
                    string += "-"
                elif item == 0:
                    string += "0"
                else:
                    string += "c"
            print(f"{string}")

    # ========== Get and Set methods ==========
    def getInterval(self):
        """
        Gets the interval
        """
        return self.interval

    def getStart(self):
        """
        Gets the start time
        """
        return self.start

    def getEnd(self):
        """
        Gets the end time
        """
        return self.end

    def setColumnName(self, ind, name):
        """
        Sets the column at index ind to a new name
        """
        col = self.getColumn(ind)
        col.setLabel(name)
