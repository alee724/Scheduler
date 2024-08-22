from initial import *
from tkinter import Frame, Label, Button, Toplevel, messagebox
import tkinter.ttk as ttk
from customer import *
import json

SRT_KEYS = ("Nail Care", "Foot Care", "Lash", "Spa", "Waxing", "Massage", "None")


class ViewFrame(Frame):
    def __init__(self, parent):
        """
        The view frame for displaying a list of objects and being able to search through the
        displayed objects

        Does not initialize the contents of the list box as there is likely to be an overlap when
        inherited
        """
        Frame.__init__(self, parent)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.view_list = []
        self.parent = parent

        # create the search bar
        self.searchVar = StringVar()
        self.search_entry = Entry(self, textvariable=self.searchVar, font=FONT)

        # create the list box for viewing the services
        self.lb = Listbox(
            self,
            selectmode=SINGLE,
            width=LB_WIDTH,
            exportselection=False,
            font=FONT,
        )

        # create the delete button
        self.delete_button = Button(
            self,
            text="Delete",
            font=FONT,
            command=lambda: self.delete(self.lb.get(self.lb.curselection()[0])),
        )

        # grid the two widgets, bind the list box griding to a visibility event
        self.search_entry.grid(row=0, column=0, sticky="ew")
        self.delete_button.grid(column=0, row=2, sticky="e")

        # create binding for variable or widgets
        self.lb.bind(
            "<MouseWheel>",
            lambda e: self.lb.yview_scroll(-1 * (e.delta), "units")
            if e.state == 0
            else None,
        )
        self.searchVar.trace("w", self.search)
        self.bind("<Unmap>", lambda e: [self.searchVar.set(""), self.lb.grid_forget()])
        self.bind(
            "<Map>",
            lambda e: [
                self.update_idletasks(),
                self.search(),
                self.lb.grid(column=0, row=1, sticky="nsew"),
            ],
        )

    def toString(self, string):
        """
        Helper method to be overwritten by children classes if needed
        """
        return str(string)

    def search(self, *args):
        """
        Helper method for inputting items when searching in the entry widget

        May need to be overwritten by children classes
        """
        self.lb.delete(0, END)
        if self.searchVar.get() == "":
            for s in self.view_list:
                self.lb.insert(END, self.toString(s))
        else:
            inp = self.searchVar.get().lower()
            for s in self.view_list:
                if inp in self.toString(s).lower():
                    self.lb.insert(END, self.toString(s))

    def delete(self, string):
        """
        The helper method for deleting a select entry from the list box
        """
        for s in self.view_list:
            if self.toString(s) == string:
                self.view_list.remove(s)
                self.search()
                break


class ServiceView(ViewFrame):
    """
    The view frame for services
    """

    def __init__(self, parent, services):
        super().__init__(parent)
        self.view_list = services

        # initialize the listbox
        self.search()

    def toString(self, string):
        """
        Override the inherited toString method
        """
        return Service.toString(string)

    def search(self, *args):
        """
        Helper method for inputting items when searching in the entry widget

        May need to be overwritten by children classes
        """
        self.lb.delete(0, END)
        if self.searchVar.get() == "":
            for s in self.view_list:
                self.lb.insert(END, self.toString(s))
        else:
            inp = self.searchVar.get().lower()
            for s in self.view_list:
                if inp in s.getName().lower() or inp in s.getAbbrev().lower():
                    self.lb.insert(END, self.toString(s))

    def delete(self, string):
        """
        Inherit the delete method and update the list of services
        """
        super().delete(string)
        self.event_generate("<<UpdateService>>")


class ServiceAdd(Frame):
    def __init__(self, parent, services):
        Frame.__init__(self, parent)
        self.grid_columnconfigure(1, weight=1)
        self.parent = parent
        self.services = services

        # create the service labels
        Label(self, text="Name", font=FONT, anchor="w").grid(
            column=0, row=0, sticky="nw"
        )
        Label(self, text="Price", font=FONT, anchor="w").grid(
            column=0, row=1, sticky="nw"
        )
        Label(self, text="Hours", font=FONT, anchor="w").grid(
            column=0, row=2, sticky="nw"
        )
        Label(self, text="Minutes", font=FONT, anchor="w").grid(
            column=0, row=3, sticky="nw"
        )
        Label(self, text="Abbreviation", font=FONT, anchor="w").grid(
            column=0, row=4, sticky="nw"
        )

        # create appropriate entry widgets for the labels
        self.nameVar = StringVar()
        self.name = Entry(self, textvariable=self.nameVar)
        self.price = Entry(
            self,
            validate="all",
            validatecommand=(self.register(lambda s: s.isdigit()), "%S"),
        )
        self.hours = Entry(
            self,
            validate="all",
            validatecommand=(self.register(lambda s: s.isdigit()), "%S"),
        )
        self.minutes = Entry(
            self,
            validate="all",
            validatecommand=(self.register(lambda s: s.isdigit()), "%S"),
        )
        self.abbreviation = Entry(self)

        # grid the entry widgets
        self.name.grid(column=1, row=0, sticky="new")
        self.price.grid(column=1, row=1, sticky="new")
        self.hours.grid(column=1, row=2, sticky="new")
        self.minutes.grid(column=1, row=3, sticky="new")
        self.abbreviation.grid(column=1, row=4, sticky="new")

        # create label and combobox for categorizing the services
        Label(self, text="Category", font=FONT).grid(column=0, row=5, sticky="nw")

        self.category = StringVar()
        cb = ttk.Combobox(self, textvariable=self.category)
        cb["values"] = SRT_KEYS

        cb.grid(column=1, row=5, sticky="new")

        # create a small list box for viewing and easily selecting services to modify
        self.lb = Listbox(
            self,
            selectmode=SINGLE,
            width=LB_WIDTH,
            exportselection=False,
            font=FONT,
            height=5,
        )
        self.lb.grid(column=0, columnspan=2, row=6, sticky="nsew")

        # create relevant buttons
        create_update = Button(
            self, text="Create/Update", font=FONT, command=self.create_service
        )
        create_update.grid(column=0, row=7, sticky="w")
        cancel = Button(
            self,
            text="Cancel",
            font=FONT,
            command=lambda: self.winfo_toplevel().destroy(),
        )
        cancel.grid(column=1, row=7, sticky="e")

        # create bindings
        self.lb.bind("<<ListboxSelect>>", self.fill)
        self.nameVar.trace("w", self.search)
        self.lb.bind(
            "<MouseWheel>",
            lambda e: self.lb.yview_scroll(-1 * (e.delta), "units")
            if e.state == 0
            else None,
        )
        self.bind("<Unmap>", self.empty)
        self.bind_all("<Return>", self.create_service)

        # initialize the listbox
        self.search()

    def empty(self, *args):
        """
        Empties the entries and makes them blank
        """
        self.nameVar.set("")

        self.price.delete(0, END)
        self.hours.delete(0, END)
        self.minutes.delete(0, END)
        self.abbreviation.delete(0, END)

    def fill(self, e):
        """
        Fills in the entries according to the selection from the list box
        """
        string = self.lb.get(e.widget.curselection()[0]).split(", ")
        self.empty()

        time = string[2].split(":")

        self.nameVar.set(string[0])
        self.price.insert(0, string[1].lstrip("$"))
        self.hours.insert(0, time[0].lstrip("0"))
        self.minutes.insert(0, time[1].lstrip("0"))
        self.abbreviation.insert(0, string[3])
        self.category.set(string[4])

    def search(self, *args):
        """
        Helper method for inputting items when searching in the entry widget
        """
        self.lb.delete(0, END)
        if self.nameVar.get() == "":
            for s in self.services:
                self.lb.insert(END, s.toString())
        else:
            inp = self.nameVar.get().strip().lower()
            for s in self.services:
                if inp in s.getName().lower() or inp in s.getAbbrev().lower():
                    self.lb.insert(END, s.toString())

    def check(self):
        """
        Helper method that check whether the entries contain valid entries
        """
        try:
            assert "" not in [
                self.name.get(),
                self.price.get(),
                self.abbreviation.get(),
            ]
            assert self.hours.get() != "" or self.minutes.get() != ""
            assert self.price.get().isdigit()
            if self.hours.get() != "":
                assert self.hours.get().isdigit()
            if self.minutes.get() != "":
                assert self.minutes.get().isdigit()
            return True
        except:
            messagebox.showerror(
                self,
                message=f"""
                    Invalid arguments have been provided. Please check that a name, price, and
                    abbreviation have been provided, and that at least one entry of hour or minutes
                    have been filled with a non-zero positive number.
                    """,
            )
            return False

    def create_service(self, *args):
        """
        Creates or replaces a service in the list of services
        """
        if self.check():
            h, m = (
                self.hours.get().strip().lstrip("0"),
                self.minutes.get().strip().lstrip("0"),
            )

            h = 0 if h == "" else int(h)
            m = 0 if m == "" else int(m)
            t = CTime(h, m)

            category = self.category.get().strip()
            if category not in SRT_KEYS:
                category = "None"

            s = Service(
                self.name.get().strip(),
                int(self.price.get().strip()),
                t,
                self.abbreviation.get().strip(),
                category,
            )
            if s not in self.services:
                self.services.append(s)
            else:
                self.services.remove(s)
                self.services.append(s)

            self.event_generate("<<UpdateService>>")
            self.search()


class ServicePop(Toplevel):
    def __init__(self, parent):
        """
        A popup window for making/modifying services
        """
        Toplevel.__init__(self, parent)
        self.title("Services")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        with open(S_PATH, "r") as file:
            self.services = list(map(lambda s: Service.fromJSON(s), json.load(file)))
            for s in self.services:
                assert isinstance(s, Service)

        # create the notebook for keeping tabs
        self.note = ttk.Notebook(self)
        self.note.grid(column=0, row=0, sticky="nsew")

        # add the two tabs for adding/modifying services and deleting/viewing services
        self.note.add(ServiceAdd(self.note, self.services), text="Add")
        self.note.add(ServiceView(self.note, self.services), text="Delete")

        # binding for updating services
        self.bind_all("<<UpdateService>>", self.update_services)

        # place the widget so that is is centered along the x but only slightly padded in the y
        self.update_idletasks()
        x = (self.winfo_vrootwidth() // 2) - (self.winfo_width() // 2)
        self.geometry(f"+{x}+100")

    def update_services(self, e):
        """
        Updates the list of services
        """
        s_lst = list(map(lambda s: Service.toJSON(s), self.services))
        with open(S_PATH, "w") as file:
            json.dump(s_lst, file)


class EmployeeView(ViewFrame):
    def __init__(self, parent, employees):
        """
        The view frame for employees where you can add and remove employees
        """
        super().__init__(parent)
        self.view_list = employees

        # create a variable for storing the data needed to be sent over a virtual event
        self.employee = None

        # adds a button to the left side to add employees
        add_button = Button(self, text="Add", font=FONT, command=self.add_employee)
        add_button.grid(column=0, row=2, sticky="w")

        # adds a button for adding to the sheet itself
        sheet_button = Button(
            self,
            text="Add Column",
            font=FONT,
            command=self.add_column,
        )
        sheet_button.grid(column=0, row=2, sticky="w", padx=(70, 0))
        self.search()

    def search(self, *args):
        """
        Override the parent class search method to include the resetting of the employee variable
        when searching to None
        """
        super().search()
        self.employee = None

    def add_column(self):
        """
        A helper method for creating a employee on the sheet, does this by binding the employee
        label string to the widget and sent over through a virtual event
        """
        try:
            index = self.lb.curselection()[0]
            string = self.lb.get(index).strip()
            self.employee = string
            self.event_generate("<<VerifyAddColumn>>")
        except:
            None

    def update_employees(self):
        """
        Updates the json file where a list of employees are stored
        """
        with open(E_PATH, "w") as file:
            json.dump(self.view_list, file)

    def add_employee(self, *args):
        """
        Adds en employee to the list if not already existing
        """
        employee = self.searchVar.get().strip()
        if employee in self.view_list:
            messagebox.showwarning(
                self,
                message=f"The employee {
                    employee} is already in the list of employees",
            )
        elif employee == "":
            messagebox.showwarning(
                self, message=f"The employee entry must not be empty"
            )
        else:
            self.view_list.append(employee)
            self.search()
            self.update_employees()

    def delete(self, string):
        """
        Inherit the delete method and update the list of employees
        """
        super().delete(string)
        self.update_employees()


class ScheduleColumn(Frame):
    def __init__(self, parent, day, employees, checked):
        """
        A class for creating a column with the label of a day at the top and a row of
        check boxes with employees

        Automatically updates the list of employees in the schedule
        """
        Frame.__init__(self, parent)
        self.checked = checked
        self.parent = parent

        self.grid_columnconfigure(list(range(1, 7)), weight=1, uniform="sch_row")

        # create labels at the top of each column
        Label(
            self,
            text=day.capitalize(),
            font=FONT,
            width=9,
            relief="groove",
            borderwidth=1,
        ).grid(column=0, row=0, sticky="nsew")

        # create the appropriate check buttons
        row = 1
        for e in employees:
            v = IntVar()
            c = Checkbutton(self, text=e, variable=v)
            c.select() if e in self.checked else c.deselect()
            c.bind(
                "<ButtonPress-1>",
                lambda e, v=v, emp=e: [
                    self.checked.append(emp)
                    if v.get() == 0
                    else self.checked.remove(emp),
                    self.event_generate("<<UpdateSchedule>>"),
                ],
            )
            c.grid(column=0, row=row, sticky="nsw")
            row += 1


class EmployeeSchedule(Frame):
    def __init__(self, parent, employees):
        """
        The frame that will display the schedule for employees and will update the schedule
        """
        Frame.__init__(self, parent)
        self.employees = employees
        self.keys = [
            "sunday",
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
        ]
        self.base_frame = Frame(self)
        with open(SCH_PATH, "r") as file:
            self.sch_dict = json.load(file)
        self.check()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.add_columns()

        # binding for making the widgets visible once swapping tabs
        self.bind("<Map>", lambda e: [self.update_idletasks(), self.add_columns()])
        self.bind_all("<<UpdateSchedule>>", self.update_schedule)

    def add_columns(self):
        """
        Helper method for adding columns to the frame
        """
        if self.base_frame.winfo_exists():
            self.base_frame.destroy()
        self.base_frame = Frame(self)
        self.base_frame.grid_columnconfigure(
            list(range(7)), weight=1, uniform="sch_col"
        )

        # add the columns of the day with check buttons for employees
        col_ind = 0
        for d in self.keys:
            col = ScheduleColumn(self.base_frame, d, self.employees, self.sch_dict[d])
            col.grid(column=col_ind, row=0, sticky="nswe")
            col_ind += 1
        self.base_frame.grid(column=0, row=0, sticky="nsew")

    def check(self):
        """
        Helper method that check for the existence of an employee and remove from the schedule
        if false
        """
        for k in self.keys:
            for e in self.sch_dict[k]:
                if e not in self.employees:
                    self.sch_dict[k].remove(e)

    def update_schedule(self, e):
        """
        Updates the json containing the list of employees
        """
        with open(SCH_PATH, "w") as file:
            json.dump(self.sch_dict, file)


class EmployeePop(Toplevel):
    def __init__(self, parent):
        """
        A popup window for creating and deleting employees
        """
        Toplevel.__init__(self, parent)
        self.title("Employees")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # import the existing employees stored in data
        with open(E_PATH, "r") as file:
            self.employees = json.load(file)
            for e in self.employees:
                assert isinstance(e, str)

        # create the notebook for swapping tabs
        self.note = ttk.Notebook(self)
        self.note.grid(column=0, row=0, sticky="nsew")

        # add the two tabs for adding/deleting employees and assigning employees to weekdays here
        self.note.add(EmployeeView(self.note, self.employees), text="Add")
        self.note.add(EmployeeSchedule(self.note, self.employees), text="Schedule")

        # place the widget so that is is centered along the x but only slightly padded in the y
        self.update_idletasks()
        x = (self.winfo_vrootwidth() // 2) - (self.winfo_width() // 2)
        self.geometry(f"+{x}+100")


class ServiceColumn(Frame):
    def __init__(self, parent, services, checked):
        """
        A frame that will contain a list of services with check buttons
        """
        Frame.__init__(self, parent)
        self.checked = checked
        self.services = list(map(lambda s: Service.fromJSON(s), services))

        self.grid_columnconfigure(0, weight=1)

        # create the rows of check buttons for display
        row_ind = 0
        for s in self.services:
            v = IntVar()
            c = Checkbutton(self, text=s.getName(), font=FONT, variable=v, anchor="w")
            c.grid(column=0, row=row_ind, sticky="new")
            c.select() if s in self.checked else c.deselect()
            c.bind(
                "<ButtonPress-1>",
                lambda e, v=v, s=s: self.checked.append(s)
                if v.get() == 0
                else self.checked.remove(s),
            )
            row_ind += 1


class CollapseServices(Frame):
    def __init__(self, parent, label, services, checked):
        """
        A frame that will contain a list of check boxes with a label at the top that can collapse
        and expand
        """
        Frame.__init__(self, parent)
        self.grid_rowconfigure(0, weight=1)

        # create the label for the collapseable frame
        l = Label(self, text=label, font=FONT, anchor="w", width=len(label) + 5)
        l.pack_propagate(False)
        l.grid(column=0, row=0, sticky="nw")

        # create the button that will initiate collapse and expansion of the inner widgets
        self.button_sign = StringVar()
        self.button_sign.set("+")
        Button(
            l,
            textvariable=self.button_sign,
            font=FONT,
            command=self.expand_collapse,
            width=1,
        ).pack(side="right")

        # create the inner frame that will collapse and expand
        self.exp_frame = ServiceColumn(self, services, checked)

    def expand_collapse(self):
        """
        Helper function for expanding and collapsing the inner frame
        """
        if self.exp_frame.grid_info() == {}:
            self.exp_frame.grid(column=0, columnspan=2, row=1, sticky="nsew")
            self.exp_frame.update_idletasks()
            self.button_sign.set("-")
        else:
            self.exp_frame.grid_forget()
            self.button_sign.set("+")


class CreateCustomer(Frame):
    def __init__(self, parent, customers):
        Frame.__init__(self, parent)
        self.grid_columnconfigure([1, 3], weight=1, uniform="cust_make")

        # create a customer variable for sending the customer data via event generation
        self.c_data = None

        # create a list of customers to keep track of who is recorded in data
        self.customers = customers

        # create label widgets for the name and phone
        Label(self, text="Name", font=FONT).grid(column=0, row=0, sticky="nw")
        Label(self, text="Phone", font=FONT).grid(column=2, row=0, sticky="nw")

        # create the entry widgets for the name and phone
        self.name = StringVar()
        Entry(self, textvariable=self.name, font=FONT, width=10).grid(
            column=1, row=0, sticky="new"
        )

        self.phone = StringVar()
        Entry(
            self,
            textvariable=self.phone,
            font=FONT,
            width=10,
            validate="all",
            validatecommand=(self.register(lambda s: s.isdigit()), "%S"),
        ).grid(column=3, row=0, sticky="new")

        # create the button for adding a customer to the queue
        queue = Button(self, text="Queue", font=FONT, command=self.queue_customer)
        queue.grid(column=0, columnspan=2, row=3, sticky="nw")

        # initialize the sorted services
        self.checked = []
        self.check_services()

        # create the buffer frame so that it can be deleted
        self.bf = Frame(self)
        self.initialize()

    def initialize(self):
        """
        A helper method for creating the columns of services and reinitializing them if need be
        """
        self.bf.destroy()

        # create a buffer frame that will contain all the collapseable widgets
        self.bf = Frame(self)
        self.bf.grid_rowconfigure(0, weight=1)
        self.bf.grid(column=0, columnspan=4, row=2, sticky="nsew")

        # add the collapseable frames to the buffer frame
        col_ind = 0
        for key in SRT_KEYS:
            if key != "None":
                cs = CollapseServices(
                    self.bf, key, self.sorted_services[key], self.checked
                )
                cs.grid(column=col_ind, row=0, sticky="new")
                col_ind += 1

        # separator for aesthetics
        ttk.Separator(self.bf, orient="horizontal").grid(
            column=0, columnspan=len(SRT_KEYS) - 1, row=1, sticky="we", pady=(4, 0)
        )

        # create a non collapseable list of check buttons for the services categorized None
        row_ind = 2
        col_ind = 0
        for s in list(map(lambda s: Service.fromJSON(s), self.sorted_services["None"])):
            v = IntVar()
            c = Checkbutton(
                self.bf, text=s.getName(), font=FONT, variable=v, anchor="w"
            )
            c.grid(column=col_ind, row=row_ind, sticky="new")
            c.select() if s in self.checked else c.deselect()
            c.bind(
                "<ButtonPress-1>",
                lambda e, v=v, s=s: self.checked.append(s)
                if v.get() == 0
                else self.checked.remove(s),
            )
            col_ind += 1
            if col_ind == len(SRT_KEYS) - 1:
                col_ind = 0
                row_ind += 1

    def check_services(self):
        """
        Helper function for reinitializing the sorted lists of services
        """
        # create the dictionary that will contain the sorted lists of services
        self.sorted_services = {}

        # add the services to a dictionary sorted by their category
        for k in SRT_KEYS:
            self.sorted_services[k] = []

        with open(S_PATH, "r") as file:
            services = json.load(file)
            for s in services:
                self.sorted_services[s["sorted"]].append(s)

    def queue_customer(self):
        """
        A helper method that will take the data to create a customer object, convert it into a
        json string and sent the data over to where the binding is
        """
        assert len(self.checked) > 0
        name = "n/a" if self.name.get() == "" else self.name.get().strip()
        name = name.split(" ")
        first = name[0]
        last = "" if len(name) == 1 else name[-1]
        phone = self.phone.get()
        if len(phone) > 0 and len(phone) != 10:
            messagebox.showwarning(
                self,
                message=f"""
                    The length of the phone number is {len(phone)}. The phone number must of length 10.

                    i.e. 0123456789
                    """,
            )
            pass
        else:
            phone = "0000000000"
            c = Customer(first, last, phone, self.checked)
            # raise event to send data to the verify sheet
            self.c_data = c.toJSON()
            self.event_generate("<<VerifyAddCustomer>>")

            # add the customer to the list of customers and update the list in data
            if c not in self.customers:
                self.customers.append(c)
                self.event_generate("<<UpdateCustomers>>")


class CustomerView(ViewFrame):
    def __init__(self, parent, customers):
        """
        Class for viewing and modifying customers as needed
        """
        super().__init__(parent)
        self.view_list = customers

        # Override the search area with labels and entries for customers
        self.search_entry.destroy()
        self.nameVar = StringVar()
        self.phoneVar = StringVar()

        # regrid delete button
        self.delete_button.grid(column=3, row=2, sticky="ne")

        # create the labels and the entry widgets
        self.grid_columnconfigure([1, 3], weight=1, uniform="cust_view")
        self.grid_columnconfigure(0, weight=0)
        Label(self, text="Name", font=FONT).grid(column=0, row=0, sticky="nw")
        Label(self, text="Phone", font=FONT).grid(column=2, row=0, sticky="nw")

        Entry(self, textvariable=self.nameVar, font=FONT).grid(
            column=1, row=0, sticky="nsew"
        )

        Entry(
            self,
            textvariable=self.phoneVar,
            font=FONT,
            validate="all",
            validatecommand=(self.register(lambda s: s.isdigit()), "%S"),
        ).grid(column=3, row=0, sticky="nsew")

        # create an add/modify button
        Button(self, text="Add/Modify", font=FONT, command=self.create_customer).grid(
            column=0, columnspan=2, row=2, sticky="nw"
        )

        # create traces for the sting variables
        self.nameVar.trace("w", self.search)
        self.phoneVar.trace("w", lambda *args: self.search(phone=True))

        # create binding for selecting an item in the list box
        self.lb.bind("<<ListboxSelect>>", self.fill)

        # rebind the map event to properly grid the list boz where it is needed
        self.bind(
            "<Map>",
            lambda e: [
                self.update_idletasks(),
                self.search(),
                self.lb.grid(column=0, columnspan=4, row=1, sticky="nsew"),
            ],
        )

    def delete(self, string):
        """
        Inherit the delete method and update the list of customers
        """
        super().destroy(string)
        self.event_generate("<<UpdateCustomers>>")

    def fill(self, e):
        """
        Helper method for filling in the entries in response to a selection in the list box
        """
        string = self.lb.get(e.widget.curselection()[0]).split(", ")

        self.nameVar.set(string[0])
        self.phoneVar.set(string[1])

    def create_customer(self):
        """
        Helper method for taking in string inputs to make/modify a customer in the list of
        customers that can be viewed

        NOTE: NOT for making a customer frame
        """
        # get the customer data
        full = self.nameVar.get().strip()
        name = full.split(" ")
        last = name[1] if len(name) > 1 else ""
        phone = self.phoneVar.get().strip()

        if len(full) <= 0:
            messagebox.showwarning(
                self,
                message=f"""
                    The length of the name is {len(full)}. The name entry must have at least one valid character

                    i.e. "A"
                    """,
            )

        if len(phone) > 0 and len(phone) != 10:
            messagebox.showwarning(
                self,
                message=f"""
                    The length of the phone number is {len(phone)}. The phone number must of length 10.

                    i.e. 0123456789
                    """,
            )
        else:
            c = Customer(name[0], last, phone)

            # validate the customer
            if c in self.view_list:
                self.view_list.remove(c)
            self.view_list.append(c)
            self.search()

            # raise event to update the list of customers
            self.event_generate("<<UpdateCustomers>>")

    def toString(self, customer):
        """
        Override the ViewFrame toString method to suit customers
        """
        return Customer.toString(customer)

    def search(self, *args, phone=False):
        """
        Helper method for inputting items when searching in the entry widget

        Overwritten to better suit customers
        """
        self.lb.delete(0, END)
        if self.nameVar.get() == "" and self.phoneVar.get() == "":
            for c in self.view_list:
                self.lb.insert(END, self.toString(c))
        else:
            for c in self.view_list:
                if phone and self.phoneVar.get().strip() in c.getPhone():
                    self.lb.insert(0, self.toString(c))
                elif self.nameVar.get().strip().lower() in c.getName().lower():
                    self.lb.insert(END, self.toString(c))


class CustomerPop(Toplevel):
    def __init__(self, parent):
        """
        The pop up frame for the customer, will have two tabs similar to services:
        One for adding a customer to the sheet and one for viewing/modifying any customers

        The adding frame will have a combobox for the name/number of the customer ONLY and
        will fill out the data accordingly

        Need to send a json of the customer through events as event_generate does not properly
        handle the data field
        """
        super().__init__(parent)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # import the list of customers
        with open(C_PATH, "r") as file:
            self.customers = list(map(lambda e: Customer.fromJSON(e), json.load(file)))

        # create the notebook
        self.note = ttk.Notebook(self)
        self.note.grid(column=0, row=0, sticky="nsew")

        # add the two tabs to the notebook
        self.note.add(CreateCustomer(self.note, self.customers), text="Add")
        self.note.add(CustomerView(self.note, self.customers), text="Modify")

        # create the binding for automatically updating the list of customers
        self.bind_all("<<UpdateCustomers>>", self.update_customers)

        # place the widget so that is is centered along the x but only slightly padded in the y
        self.update_idletasks()
        x = (self.winfo_vrootwidth() // 2) - (self.winfo_width() // 2)
        self.geometry(f"+{x}+100")

    def update_customers(self, e):
        """
        Helper methods for updating the list of customers in data
        """
        with open(C_PATH, "w") as file:
            c_json = list(map(lambda c: c.toJSON(), self.customers))
            json.dump(c_json, file)
