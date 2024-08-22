from constants import *
from tkinter import Frame, Label
import tkinter.ttk as ttk
from tkinter.constants import *
from customerFrame import *
from tkinter import Canvas, LabelFrame
from sheet import ScheduleSheet
import threading
import json


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
        self.bind("<Configure>", lambda e: [self.resize(e), self.unbind("<Configure>")])

        # binding for the mousewheel
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
        self.right.grid(column=index + 1, row=0, sticky="nse")
        Label(self.scroll_frame, text=name, font=E_FONT, anchor=CENTER).grid(
            column=index, row=0, sticky="nsew"
        )
        self.employees.append(name)
        self.update_idletasks()

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
                font=T_FONT,
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
        self.grid_propagate(False)
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

        # create vertical separators
        ttk.Separator(self, orient="vertical").grid(
            column=self.numCols, row=0, rowspan=self.numRows, sticky="nse"
        )
        ttk.Separator(self, orient="vertical").grid(
            column=self.numCols, row=0, rowspan=self.numRows, sticky="nsw"
        )

        # add hour lines if adding first column
        if self.numCols == 0:
            self.add_hourlines()

        # increment the number of columns
        self.numCols += 1

    def add_hourlines(self):
        """
        A helper method for adding horizontal separators for the grid representing hours
        """
        for i in range(self.numRows):
            if i != 0:
                s1 = ttk.Separator(self, orient="horizontal")
                s1.grid(column=0, row=i - 1, sticky="swe")
                self.bind_all(
                    "<<VerifyAddColumn>>",
                    lambda e, s1=s1, i=i: s1.grid(
                        column=0, row=i - 1, columnspan=self.numCols, sticky="swe"
                    ),
                    add="+",
                )
            s2 = ttk.Separator(self, orient="horizontal")
            s2.grid(column=0, row=i, sticky="new")
            self.bind_all(
                "<<VerifyAddColumn>>",
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

        # binding for the mousewheel event
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


class MainSheet(Frame):
    def __init__(self, parent, employees=[], json_dict=None):
        """
        Class for the frame that will contain two canvases, one being the canvas for employee names
        and the other canvas for the sheet containing the customers that will be served for that
        day

        @parameter employees: a list of names of employees
        """
        Frame.__init__(self, parent)
        for e in employees:
            assert isinstance(e, str)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # create the backend sheet variable that will be used to track any processes needed
        self.employees = employees
        self.verify = ScheduleSheet()

        numRows = (END_TIME - START_TIME) * 60 // 15

        # create the two scrollable canvases
        self.emp_canvas = EmployeeCanvas(self)
        self.sheet = SheetCanvas(self, numRows)

        # create the queue frame
        self.queue = Frame(self, borderwidth=0)
        ttk.Separator(self.queue, orient="vertical").pack(side=RIGHT, fill=Y)

        # grid the two different canvases in their appropriate location
        self.emp_canvas.grid(column=1, row=0, sticky="new")
        self.sheet.grid(row=1, column=1, sticky="nsew")

        # create the bindings for checking with the backend and allowing certain processes to continue
        self.bind_all("<<VerifyAddCustomer>>", self.queue_customer)
        self.bind_all("<<VerifyMoveCustomer>>", self.move_customer)
        # TODO, figure out why the error is raised
        self.bind_all("<<VerifyDestroyCustomer>>", self.destroy_customer)
        self.bind_all("<<VerifyServed>>", self.served_customer)
        self.bind_all("<<VerifyAddColumn>>", self.add_employee)

        # set the new protocol for when the window is being closed
        self.winfo_toplevel().protocol("WM_DELETE_WINDOW", self.save_json_sheet)

        # create binding for the canvases for resizing and setting the scrollregions
        self.bind_all(
            "<<VerifyAddColumn>>",
            lambda e: [
                self.emp_canvas.resize(),
                self.sheet.resize(),
                self.emp_canvas.configure(scrollregion=self.emp_canvas.bbox("all")),
                self.sheet.configure(scrollregion=self.sheet.bbox("all")),
            ],
            add="+",
        )

        # ========== Logic for loading in data ==========
        if json_dict == None:
            self.after(
                0, lambda: threading.Thread(target=self.add_employee_list()).start()
            )
        else:
            self.after(
                0, lambda: threading.Thread(target=self.load_json_sheet(json_dict)).start()
            )

    def load_json_sheet(self, json_dict):
        """
        Helper method for loading in the data from a json dictionary
        """
        index = 0
        for col in json_dict["columns"]:
            self.add_employee(name=col["label"])
            for cust in col["items"]:
                row_ind = cust[0]
                rowspan = cust[2]
                c = Customer.fromJSON(cust[1])
                cf = CustomerFrame(self, c)
                cf.grid(
                    in_=self.sheet.sheet, column=index, row=row_ind, rowspan=rowspan, sticky="nsew"
                )
            index += 1

        # set the verify variable to the json_dict 
        self.verify.fromJSON(json_dict["columns"])

        # fix the screen
        self.event_generate("<<VerifyAddColumn>>")
        self.update_idletasks()

    def save_json_sheet(self):
        """
        A helper function describing the new protocol to be taken when the widow is being closed
        """
        with open(DAY_PATH, "w") as file:
            json.dump(self.verify.toJSON(), file)
        self.winfo_toplevel().destroy()

    def add_employee_list(self):
        # add any employees if any
        for e in self.employees:
            self.add_employee(name=e)

        # fix the screen
        self.event_generate("<<VerifyAddColumn>>")
        self.update_idletasks()

    def served_customer(self, e):
        """
        Helper method for changing the state of a customer's served attribute to true or false
        """
        wid = e.widget
        data = wid.grid_info()
        state = self.verify.serve_customer(data["column"], data["row"])
        if state:
            wid.configure(background="green")
        else:
            wid.configure(background="red")

    def destroy_customer(self, e):
        """
        Helper method to check the viability to destroy a customer at some location
        """
        wid = e.widget
        g_data = wid.grid_info()

        try:
            # if the widget is in the queue
            wid.pack_info()
            wid.destroy()
            self.verify.queue -= 1
            if self.verify.queue == 0:
                self.queue.grid_forget()
        except:
            # else when it is grid in the sheet
            if self.verify.remove_customer(g_data["column"], g_data["row"]):
                wid.destroy()

    def move_customer(self, e):
        """
        Helper method for verifying whether a customer can be moved to a specific grid in the sheet
        """
        widget = e.widget

        x = (
            widget.winfo_x()
            - self.queue.winfo_width()
            - TIME_W
            + (widget.winfo_width() // 2)
        )
        y = widget.winfo_y() - ROW_H + C_BUFF_TOP
        grid_data = self.sheet.sheet.grid_location(x, y)
        finalCol = grid_data[0]
        finalRow = grid_data[1]

        # if the widget is queued and not yet added to the sheet
        if widget.packed == True:
            # check with the backend
            if self.verify.add_customer(finalCol, finalRow, widget.c_data):
                # grid the customer to the sheet
                widget.grid(
                    in_=self.sheet.sheet,
                    column=finalCol,
                    row=finalRow,
                    rowspan=widget.rowspan,
                    sticky="nsew",
                )
                self.verify.queue -= 1
                if self.verify.queue == 0:
                    self.queue.grid_forget()
                widget.packed = False
            else:
                # pack back to queue
                widget.pack(in_=self.queue, fill=X)
        # when the widget is already in the sheet and is being moved
        else:
            # check with backend
            if self.verify.move_customer(
                widget.initCol, widget.initRow, finalCol, finalRow
            ):
                # grid to new location
                widget.grid(
                    in_=self.sheet.sheet,
                    column=finalCol,
                    row=finalRow,
                    rowspan=widget.rowspan,
                    sticky="nsew",
                )
            else:
                # grid back in original place
                widget.grid(
                    in_=self.sheet.sheet,
                    column=widget.initCol,
                    row=widget.initRow,
                    rowspan=widget.rowspan,
                    sticky="nsew",
                )
        widget.update_idletasks()

    def queue_customer(self, e):
        """
        Helper method for retrieving data from the event widget and queuing a customer frame
        """
        customer = e.widget.c_data
        if customer != None:
            if self.verify.queue == 0:
                self.queue.configure(width=200)
                # generate the <<VerifyAddColumn>> event to fix the scroll region for the canvas
                self.event_generate("<<VerifyAddColumn>>")
            cust_obj = Customer.fromJSON(customer)
            cf = CustomerFrame(self, cust_obj)
            cf.pack(in_=self.queue)
            cf.packed = True
            cf.c_data = cust_obj
            cf.rowspan = self.verify.time_to_length(cust_obj.getTime())

            self.verify.queue += 1
            if self.verify.queue == 1:
                # grid the queue frame
                self.queue.grid(column=0, row=0, rowspan=2, sticky="nsw")

    def add_employee(self, event=None, name=None):
        """
        Helper method that adds a new employee column to the sheet by getting the label from the
        event widget that triggered the <<VerifyAddColumn>> event
        """
        if event != None:
            wid = event.widget
            if wid != self:
                name = wid.employee
                # reset the variable to None so that there won't be any duplicates when adjusting canvas sizes and such
                wid.employee = None
        if name != None and self.verify.add_column(name):
            self.emp_canvas.add_employee(name)
            self.sheet.add_column()

    def remove_employee(self, e):
        """
        Helper method that removes an employee column if the sheet passes the check in the backend
        """
        wid = e.widget
        name = wid.employee
        if self.verify.remove_column(name):
            self.emp_canvas.remove_employee(name)
