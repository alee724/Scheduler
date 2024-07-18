from column import *
from ctime import *


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
        self.length = cols
        self.numRows = numRows
        self.add_column("")

    def add_column(self, label):
        """
        Modifies the list by using the list.append method to add a Column to the grid

        @parameter label: a string
        """
        myAssert(isinstance(label, str), BadArgument)
        list.append(self.columns, Column(label, self.numRows))

    def remove_column(self, index):
        """
        Modifies the list by removing a Column from the list using the list.pop method

        @parameter index: integer where index <= length of self.columns
        """
        myAssert(isinstance(index, int), BadArgument)
        myAssert(index <= len(self.columns), BadIndex)
        list.pop(self.columns, index)

    # ========== Set and Get methods ==========
    def getColumn(self, index):
        """
        Gets the column
        """
        myAssert(isinstance(index, int), BadArgument)
        myAssert(index <= len(self.columns), BadIndex)
        return self.columns[index]


class ScheduleSheet(Grid):
    def __init__(self, numRows, start_time=8, end_time=20, interval=15):
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
        super().__init__(self, numRows=numRows)
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

    class CustomerOverlap(Exception):
        pass

    def time_to_length(self, time):
        """
        Helper method to convert a CTime object into index length where each unit length is of
        self.interval minutes
        """
        myAssert(isinstance(time, CTime), BadArgument)
        min = time.asMinutes()
        len = min // self.interval
        rem = min % self.interval
        return len + round(rem)

    def add_customer(self, col, customer, insert_time, time_span):
        """
        Modifies the sheet by adding [customer] to the [index] column where the customer takes up
        some [time_span] amount of time

        @parameter col: integer
        @parameter customer: the customer to be added to the schedule
        @insert_time: CTime object representing the time at which the customer has an appointment
        @parameter time_span: CTime object representing the amount of time the cusomter would
                              spend to receive services
        """
        myAssert(isinstance(col, int) and isinstance(time_span, CTime), BadArgument)
        col = self.getColumn(col)
        length = time_to_length(time_span)
        start = time_to_length(insert_time)
        col.add_item(start, customer, length)

    def move_customer(self, icol, fcol, itime, ftime):
        """
        Modifies the sheet by moving a customer in column [icol] located at approximately [itime]
        to column [fcol] at time [ftime]. If there is no customer at the specified location then
        nothing happens

        @parameter icol: integer
        @parameter fcol: integer
        @parameter itime: CTime object
        @parameter ftime: CTime object
        """
        myAssert(isinstance(icol, int) and isinstance(fcol, int), BadArgument)
        myAssert(isinstance(itime, CTime) and isinstance(ftime, CTime), BadArgument)
        i_column = self.getColumn(icol)
        f_column = self.getColumn(fcol)
        i_row = time_to_length(itime)
        f_row = time_to_length(ftime)
        customer = i_column.getItem(i_row)
        if customer != None:
            try:
                # yea I have to make it such that you can get the size from the customr obj
                f_column.add_item(f_row, customer)
                i_column.remove_item(i_row)
            except BadArgument:
                raise CustomerOverlap


