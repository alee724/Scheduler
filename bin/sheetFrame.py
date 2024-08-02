from tkinter.ttk import *
from tkinter import *
from ctime import *
from customer import *
from service import *
from customerFrame import *
import sys

sys.path.insert(0, "../lib/scheduler/")


class TimeCanvas(Canvas):
    def __init__(self, parent, start, end, interval, time_height, name_height):
        """
        Class creating a scrollable canvas of time labels

        @parameter start: a CTime object
        @parameter end: a CTime object
        @parameter interval: integer representing the amount of minutes between time labels
        @parameter time_height: the integer height of each row in the sheet
        @parameter name_height: the integer height of the name labels of employees
        """
        Canvas.__init__(self, parent, highlightthickness=0, background="red")
        assert isinstance(start, CTime)
        assert isinstance(end, CTime)

        # ========== Creation of Scrolling Frame ==========
        scroll_frame = Frame(self)

        # buffer frame above the time labels
        Frame(
            scroll_frame,
            height=(name_height - (time_height // 2)),
            relief="flat",
            borderwidth=1,
        ).pack(fill=X)

        # the actual time labels
        while start != end:
            LabelFrame(
                scroll_frame,
                text=start.toString(),
                font=("Helvetica", 16),
                relief="flat",
                labelanchor="e",
                height=time_height,
                width=45,
            ).pack(fill=BOTH, expand=True, padx=(0, 3))
            start.add_time(minute=interval)

        # add the buffer frame below the time labels
        Frame(
            scroll_frame, height=(time_height // 2), relief="flat", borderwidth=1
        ).pack(fill=X)

        # ========== Adding to Canvas and Bindings ==========
        # add the scroll frame to the canvas and add bindings for scrolling
        self.create_window((0, 0), window=scroll_frame, anchor="nw")
        self.bind(
            "<Configure>",
            lambda e, sf=scroll_frame: [
                self.configure(scrollregion=self.bbox("all")),
                self.configure(width=sf.winfo_width()),
            ],
        )
        self.bind_all(
            "<MouseWheel>",
            lambda e: self.yview_scroll(-1 * (e.delta), "units")
            # scroll only when detecting mouse movement in the y direction
            if e.state == 0
            else None,
            add="+",
        )


class EmployeeCanvas(Canvas):
    def __init__(self, parent):
        """
        Class for the employee labels

        @parameter employees: is the list of employee names that is empty by default
        """
        Canvas.__init__(self, parent, highlightthickness=0, background="blue")
        self.employees = []

        # create the scrollable frame
        self.scroll_frame = Frame(self, relief="groove", borderwidth=1)

        sf_id = self.create_window(
            (0, 0), window=self.scroll_frame, anchor="nw")

        # bindings for scrolling
        self.bind(
            "<Configure>",
            lambda e, sf=self.scroll_frame: [
                self.configure(scrollregion=self.bbox("all")),
                self.configure(height=sf.winfo_height()),
            ],
        )
        self.bind_all(
            "<MouseWheel>",
            lambda e: self.xview_scroll(-1 * (e.delta), "units")
            # scroll only when detecting mouse movement in the x direction
            if e.state == 1
            else None,
            add="+",
        )

        # binding for resizing the width of the frame to canvas width
        self.bind(
            "<Configure>",
            lambda e, sf_id=sf_id: self.itemconfigure(
                sf_id, width=self.winfo_width()),
            add="+",
        )

    def add_employee(self, name):
        """
        Adds an Employee label to the list if it doesn't already exist
        """
        assert isinstance(name, str)
        assert name not in self.employees
        self.employees.append(name)
        Label(
            self.scroll_frame, text=name, font=("Helvetoica", 24), anchor=CENTER
        ).pack(side=LEFT, fill=BOTH, expand=True)

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


class SheetFrame(Frame):
    def __init__(self, parent, rows):
        """
        A class representing the grid in which we will assign customers to cells for a visual
        representation

        @parameter rows: is the number of rows in the sheet
        """
        Frame.__init__(self, parent)
        self.numCols = 0
        self.numRows = rows

        # grid Configure
        self.grid_rowconfigure(list(range(rows)), weight=1,
                               uniform="rows", minsize=30)

    def add_column(self):
        """
        Adds a column to the grid by adding a column_configuration
        """
        self.grid_columnconfigure(self.numCols, weight=1, uniform="cols")
        if self.numCols != 0:
            Separator(self, orient="vertical").grid(
                column=self.numCols - 1, row=0, rowspan=self.numRows, sticky="nse"
            )
        Separator(self, orient="vertical").grid(
            column=self.numCols, row=0, rowspan=self.numRows, sticky="nsw"
        )
        if self.numCols == 0:
            self.add_hourlines()
        self.numCols += 1

    def add_hourlines(self):
        """
        A helper method for adding horizontal separators for the grid representing hours
        """
        for i in range(self.numRows):
            if i != 0:
                s1 = Separator(self, orient="horizontal")
                s1.grid(column=0, row=i - 1, sticky="swe")
                self.bind(
                    "<Configure>",
                    lambda e, s1=s1, i=i: s1.grid(
                        column=0, row=i - 1, rowspan=self.numRows, sticky="swe"
                    ),
                    add="+",
                )
            s2 = Separator(self, orient="horizontal")
            s2.grid(column=0, row=i, sticky="new")
            self.bind(
                "<Configure>",
                lambda e, s2=s2, i=i: s2.grid(
                    column=0, row=i, rowspan=self.numRows, sticky="new"
                ),
                add="+",
            )


class SheetCanvas(Canvas):
    def __init__(self, parent, rows):
        """
        Class representing the canvas containing the sheet of customers and being able to add
        customers, remove them, and modify them
        """
        Canvas.__init__(self, parent, highlightthickness=0,
                        background="purple")

        # create the scrollable frame
        self.scroll_frame = SheetFrame(self, rows)
        sf_id = self.create_window(
            (0, 0), window=self.scroll_frame, anchor="nw")

        # binding to make scrollable
        self.bind(
            "<Configure>", lambda e: self.configure(
                scrollregion=self.bbox("all"))
        )
        self.bind_all(
            "<MouseWheel>",
            lambda e: self.yview_scroll(-1 * (e.delta), "units")
            if e.state == 0
            else self.xview_scroll(-1 * (e.delta), "units"),
            add="+",
        )

        # binding for resizing the width of the frame to canvas width
        self.bind(
            "<Configure>",
            lambda e, sf_id=sf_id: self.itemconfigure(
                sf_id, width=self.winfo_width()),
            add="+",
        )

    def add_column(self):
        self.scroll_frame.add_column()


class MainSheet(Frame):
    label_height = 36
    row_height = 30
    start = 8
    end = 20
    interval = 15

    def __init__(self, parent, employees=[]):
        """
        Class for the frame that will contain all the canvases created for viewing employees,
        the customers, and the time, each with varying scroll features
        """
        Frame.__init__(self, parent)
        for e in employees:
            assert isinstance(e, str)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        numRows = (20 - 8) * 60 // 15

        # create the three scrollable canvases
        self.emp_canvas = EmployeeCanvas(self)
        time = TimeCanvas(
            self,
            CTime(hour=self.start),
            CTime(hour=self.end),
            self.interval,
            self.row_height,
            self.label_height,
        )
        self.sheet = SheetCanvas(self, numRows)

        # add any employees if any
        for e in employees:
            self.add_employee(e)

        # grid the three different canvases in their appropriate location
        self.emp_canvas.grid(column=1, row=0, sticky="new")
        time.grid(column=0, row=0, rowspan=2, sticky="nsw")
        self.sheet.grid(row=1, column=1, sticky="nsew")

        self.bind_all(
            "<KeyPress-a>",
            lambda e: [
                print(1),
                self.add_employee(str(len(self.emp_canvas.employees))),
            ],
        )

        self.bind_all("<KeyPress-g>", lambda e: print(self.sheet.scroll_frame.winfo_height()))

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
