from tkinter.ttk import *
from tkinter import *
from ctime import *
from customer import *
from service import *
from customerFrame import *
import sys

sys.path.insert(0, "../lib/scheduler/")

COLUMN_W = 200
ROW_H = 30
TIME_W = 50


class EmployeeCanvas(Canvas):
    def __init__(self, parent):
        """
        Class for the employee labels

        @parameter employees: is the list of employee names that is empty by default
        """
        Canvas.__init__(self, parent, highlightthickness=0, background="blue")
        self.employees = []

        # create the scrollable frame
        self.scroll_frame = Frame(self)

        # create buffers
        Frame(self.scroll_frame, relief="flat", borderwidth=1, width=TIME_W).grid(
            column=0, row=0, sticky="wns"
        )
        self.right = Frame(
            self.scroll_frame, relief="flat", borderwidth=1, width=TIME_W
        )
        self.right.grid(column=1, row=0, sticky="nse")

        self.scrollframe_id = self.create_window(
            (0, 0), window=self.scroll_frame, anchor="nw"
        )

        # binding for resizing the width of the frame to canvas width
        self.bind("<<AddEmployee>>", self.resize)
        self.bind("<Configure>", lambda e: [self.resize(e), self.unbind("<Configure>")])

        # bindings for scrolling
        self.bind(
            "<<AddEmployee>>",
            lambda e: self.configure(scrollregion=self.bbox("all")),
            add="+",
        )
        self.bind_all(
            "<MouseWheel>",
            lambda e: self.xview_scroll(-1 * (e.delta), "units")
            if e.state == 1
            else None,
            add="+",
        )

    def resize(self, *args):
        """
        Helper method that will be triggered by an event for resizing the frame
        """
        current = self.winfo_width()
        possible = (COLUMN_W * len(self.employees)) + 100
        if possible > current:
            self.itemconfigure(self.scrollframe_id, width=possible)
        else:
            self.itemconfigure(self.scrollframe_id, width=current)
        self.configure(height=self.scroll_frame.winfo_height())

    def add_employee(self, name):
        """
        Adds an Employee label to the list if it doesn't already exist
        """
        assert isinstance(name, str)
        assert name not in self.employees
        index = len(self.employees) + 1
        self.scroll_frame.grid_columnconfigure(
            index, weight=1, uniform="emp_cols", minsize=COLUMN_W
        )
        Label(
            self.scroll_frame, text=name, font=("Helvetoica", 24), anchor=CENTER
        ).grid(column=index, row=0, sticky="nsew")
        self.employees.append(name)
        self.right.grid(column=index + 1, row=0, sticky="nse")
        self.event_generate("<<AddEmployee>>")

    def remove_employee(self, name):
        """
        Removes an employee label and from the list if it exists
        """
        assert isinstance(name, str)
        assert name in self.employees
        self.employees.remove(name)
        for w in self.scroll_frame.winfo_children():
            if w.cgets("text") == name:
                w.destroy()
                break


class TimeFrame(Frame):
    def __init__(self, parent, start, end, interval):
        """
        Class for a frame that will display the time for the spreadsheet
        """
        assert isinstance(start, CTime)
        assert isinstance(end, CTime)
        assert end.asMinutes() > start.asMinutes()
        assert (end.asMinutes() - start.asMinutes()) % interval == 0
        Frame.__init__(self, parent)

        # insert buffer frame at the top
        Frame(self, borderwidth=1, relief="flat", height=ROW_H // 2).pack(fill=X)

        start.add_time(minute=interval)
        # add the time labels to the base frame
        while start != end:
            LabelFrame(
                self,
                text=start.toString(),
                height=ROW_H,
                width=TIME_W,
                relief="flat",
                font=("Helvetica", 18),
                labelanchor="e",
            ).pack(padx=(0, 1))
            start.add_time(minute=interval)

        # add the buffer frame at the end
        Frame(self, borderwidth=1, relief="flat", height=ROW_H // 2).pack(fill=X)


class SheetFrame(Frame):
    def __init__(self, parent, rows):
        """
        A class representing the grid in which we will assign customers to cells for a visual
        representation

        @parameter rows: is the number of rows in the sheet
        """
        Frame.__init__(self, parent, relief="flat", borderwidth=1)
        self.numCols = 0
        self.numRows = rows

        # grid Configure
        self.grid_rowconfigure(
            list(range(rows)), weight=1, uniform="rows", minsize=ROW_H
        )

    def add_column(self):
        """
        Adds a column to the grid by adding a column_configuration
        """
        self.grid_columnconfigure(
            self.numCols, weight=1, uniform="cols", minsize=COLUMN_W
        )

        # create certical separators
        Separator(self, orient="vertical").grid(
            column=self.numCols, row=0, rowspan=self.numRows, sticky="nse"
        )
        Separator(self, orient="vertical").grid(
            column=self.numCols, row=0, rowspan=self.numRows, sticky="nsw"
        )

        # add hour lines if adding first column
        if self.numCols == 0:
            self.add_hourlines()

        # increment the number of columns
        self.numCols += 1
        self.event_generate("<<AddColumn>>")

    def add_hourlines(self):
        """
        A helper method for adding horizontal separators for the grid representing hours
        """
        for i in range(self.numRows):
            if i != 0:
                s1 = Separator(self, orient="horizontal")
                s1.grid(column=0, row=i - 1, sticky="swe")
                self.bind(
                    "<<AddColumn>>",
                    lambda e, s1=s1, i=i: s1.grid(
                        column=0, row=i - 1, columnspan=self.numCols, sticky="swe"
                    ),
                    add="+",
                )
            s2 = Separator(self, orient="horizontal")
            s2.grid(column=0, row=i, sticky="new")
            self.bind(
                "<<AddColumn>>",
                lambda e, s2=s2, i=i: s2.grid(
                    column=0, row=i, columnspan=self.numCols, sticky="new"
                ),
                add="+",
            )


class SheetCanvas(Canvas):
    start = 8
    end = 20
    interval = 15

    def __init__(self, parent, rows):
        """
        Class representing the canvas containing the sheet of customers and being able to add
        customers, remove them, and modify them
        """
        Canvas.__init__(self, parent, highlightthickness=0, background="purple")
        self.numRows = rows

        # create the scrollable frame
        scroll_frame = Frame(self)
        scroll_frame.grid_columnconfigure(1, weight=1)

        left_time = TimeFrame(
            scroll_frame,
            CTime(self.start),
            CTime(self.end),
            self.interval,
        )
        self.sheet = SheetFrame(scroll_frame, rows)
        right_time = TimeFrame(
            scroll_frame,
            CTime(self.start),
            CTime(self.end),
            self.interval,
        )

        # grid the frames to the scroll frame
        left_time.grid(column=0, row=0, sticky="nsw")
        self.sheet.grid(column=1, row=0, sticky="nsew")
        right_time.grid(column=2, row=0, sticky="nse")

        # create the window in the canvas
        self.scrollframe_id = self.create_window(
            (0, 0), window=scroll_frame, anchor="nw"
        )

        # binding for resizing the width of the frame to canvas width
        self.bind("<<AddColumn>>", self.resize)

        # binding to make scrollable
        self.bind(
            "<<AddColumn>>",
            lambda e: self.configure(scrollregion=self.bbox("all")),
            add="+",
        )
        self.bind_all(
            "<MouseWheel>",
            lambda e: self.yview_scroll(-1 * (e.delta), "units")
            if e.state == 0
            else self.xview_scroll(-1 * (e.delta), "units"),
            add="+",
        )

    def resize(self, *args):
        """
        Helper method that will modify the size of the scrollable frame as needed
        """
        current_w = self.winfo_width()
        possible_w = (self.sheet.numCols * COLUMN_W) + (2 * TIME_W)
        if current_w < possible_w:
            self.itemconfigure(self.scrollframe_id, width=possible_w)
        else:
            self.itemconfigure(self.scrollframe_id, width=current_w)

        current_h = self.winfo_height()
        possible_h = self.numRows * ROW_H
        if current_h < possible_h:
            self.itemconfigure(self.scrollframe_id, height=possible_h)

    def add_column(self):
        """
        Simple method that calls on SheetFrame.add_column to add a column to the sheet frame in
        the canvas
        """
        self.sheet.add_column()
        self.event_generate("<<AddColumn>>")


class MainSheet(Frame):
    def __init__(self, parent, employees=[]):
        """
        Class for the frame that will contain two canvases, one being the canvas for employee names
        and the other canvas for the sheet containing the customers that will be served for that
        day

        @parameter employees: a list of names of employees
        """
        Frame.__init__(self, parent)
        for e in employees:
            assert isinstance(e, str)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        numRows = (20 - 8) * 60 // 15

        # create the three scrollable canvases
        self.emp_canvas = EmployeeCanvas(self)
        self.sheet = SheetCanvas(self, numRows)

        # add any employees if any
        for e in employees:
            self.add_employee(e)

        # grid the two different canvases in their appropriate location
        self.emp_canvas.grid(column=0, row=0, sticky="new")
        self.sheet.grid(row=1, column=0, sticky="nsew")

        self.bind_all(
            "<KeyPress-a>",
            lambda e: [
                self.add_employee(str(len(self.emp_canvas.employees))),
            ],
        )

    def add_employee(self, name):
        """
        Adds an employee column to the sheet frame in the sheet canvas and a new label in the
        employee frame in the employee canvas

        @parameter name: str
        """
        self.emp_canvas.add_employee(name)
        self.sheet.add_column()

    def remove_employee(self, name):
        """
        Removes an employee column if and only if the employee column is empty

        Uses the backend to check
        """
        if True:  # add check from backend
            self.emp_canvas.remove_employee(name)
