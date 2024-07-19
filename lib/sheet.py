from column import *
from ctime import *


class NonemptyColumnException(Exception):
    pass


class Grid:
    def __init__(self, cols=1, numRows=1):
        """
        Creates a Grid class with a at least one default column with some positive number of rows

        @parameter cols: positive integer
        @parameter numRows: positive integer
        """
        myAssert(isinstance(cols, int) and isinstance(numRows, int), BadArgument)
        myAssert(cols > 0 and numRows > 0, BadArgument)

        self.columns = []
        self.length = 0
        self.numRows = numRows
        self.add_column("")

    def add_column(self, label):
        """
        Modifies the list by using the list.append method to add a Column to the grid

        @parameter label: a string
        """
        myAssert(isinstance(label, str), BadArgument)
        list.append(self.columns, Column(label, self.numRows))
        self.length += 1

    def remove_column(self, index):
        """
        Modifies the list by removing a Column from the list using the list.pop method
        The column MUST be empty in order for it to be removed

        @parameter index: integer where index <= length of self.columns
        """
        myAssert(isinstance(index, int), BadArgument)
        myAssert(index <= len(self.columns), BadIndex)
        if self.columns[index].getNumItems() == 0:
            list.pop(self.columns, index)
            self.length -= 1
        else:
            raise NonemptyColumnException

    # ========== Set and Get methods ==========
    def getColumn(self, index):
        """
        Gets the column at index
        """
        myAssert(isinstance(index, int), BadArgument)
        myAssert(index < self.length, BadIndex)
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
    def __init__(self, start_time=8, end_time=20, interval=15):
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
        super().__init__(numRows=(end_time - start_time) * 60 // 15)
        myAssert(
            isinstance(start_time, int)
            and isinstance(end_time, int)
            and isinstance(interval, int)
            and end_time > start_time,
            BadArgument,
        )
        myAssert(
            interval > 0 and ((end_time - start_time) * 60) % interval == 0, BadArgument
        )
        self.start = CTime(hour=start_time)
        self.end = CTime(hour=end_time)
        self.interval = interval

    def toJSON(self):
        column_json_list = []
        for c in self.columns:
            list.append(column_json_list, c.toJSON())
        json = {
            "start": self.start.toJSON(),
            "end": self.end.toJSON(),
            "interval": self.interval,
            "columns": column_json_list,
        }
        return json

    def time_to_length(self, time):
        """
        Helper method to convert a CTime object into index length where each unit length is of
        self.interval minutes
        """
        myAssert(isinstance(time, CTime), BadArgument)
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
        myAssert(isinstance(col, int) and isinstance(row, int), BadArgument)
        myAssert(col >= 0 and row >= 0, BadArgument)
        myAssert(col <= self.length, BadIndex)
        column = self.getColumn(col)
        column.add_item(row, customer, self.time_to_length(customer.getTime()))

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
        myAssert(isinstance(icol, int) and isinstance(fcol, int), BadArgument)
        myAssert(isinstance(irow, int) and isinstance(frow, int), BadArgument)
        i_column = self.getColumn(icol)
        f_column = self.getColumn(fcol)
        customer = i_column.getItem(irow)
        if customer != None:
            try:
                f_column.add_item(
                    frow, customer, self.time_to_length(customer.getTime())
                )
                i_column.remove_item(irow)
            except BadArgument:
                raise CustomerOverlap
        else:
            raise BadIndex

    def remove_customer(self, col, row):
        """
        Modifies the sheet by removing a customer at some column and row

        @parameter col: integer
        @parameter row: integer
        """
        myAssert(isinstance(col, int) and isinstance(row, int), BadArgument)
        myAssert(col <= self.length, BadIndex)
        column = self.getColumn(col)
        customer = column.getItem(row)
        if customer != None:
            column.remove_item(row)

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
