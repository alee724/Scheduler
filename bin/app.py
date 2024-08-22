from tkinter import Frame, Label, Button, StringVar
import tkinter.ttk as ttk
from popUp import CustomerPop, EmployeePop, ServicePop
from datetime import timedelta, date
from tkcalendar import Calendar
from sheetFrame import MainSheet
from constants import *
import json


class CalendarFrame(Frame):
    def __init__(self, parent):
        """
        Class for the frame that will contain the calendar
        """
        Frame.__init__(
            self,
            parent.winfo_toplevel(),
            width=400,
            height=300,
            relief="solid",
            borderwidth=2,
            background="dark gray",
        )
        self.parent = parent
        self.date = date.today()
        self.dateVar = StringVar()

        # configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # use a style for the calendar
        style = ttk.Style(self)
        style.theme_use("clam")

        # create the calendar
        self.cal = Calendar(
            self,
            font=("Helvetica", 16),
            borderwidthint=1,
            selectmode="day",
            date_pattern="mm-dd-yyyy",
            firstweekday="sunday",
            showweeknumbers=False,
        )
        self.cal.grid(column=0, row=0, sticky="nsew")

        # calendar buttons
        select_button = Button(self, text="Select", font=FONT, command=self.set_date)
        select_button.grid(column=0, row=1, sticky="w")
        cancel_button = Button(
            self, text="Cancel", font=FONT, command=lambda: self.place_forget()
        )
        cancel_button.grid(column=0, row=1, sticky="e")

        # set the initial date in the string variable to today
        self.toToday()

    def toToday(self):
        """
        Helper function that sets the date to today
        """
        today = date.today()
        self.change_to(today.day, today.month, today.year)

    def change_by(self, day=0, week=0):
        """
        Changes the date by some amount of days or weeks
        """
        self.date += timedelta(days=day, weeks=week)
        self.dateVar.set(self.date.strftime("%A: %m-%d-%y"))

    def change_to(self, day, month, year):
        """
        Changes the date to some day, month, and year
        """
        self.date = date(day=day, month=month, year=year)
        self.dateVar.set(self.date.strftime("%A: %m-%d-%y"))

    def set_date(self):
        """
        Helper method that responds to the select button of the calendar

        Sets the string variable to the selected date and changes the self.date to the select date
        """
        string = self.cal.get_date()
        mdy = list(map(lambda x: int(x), string.split("-")))
        self.change_to(mdy[1], mdy[0], mdy[2])

    def get_date(self):
        """
        A simple helper method that will return the date
        """
        return self.date


class DateFrame(Frame):
    def __init__(self, parent):
        """
        The Frame that will contain the buttons required to change the date, open a calendar
        and return a string representation of the current date or date that was changed to
        """
        Frame.__init__(self, parent)
        self.parent = parent
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # create the calendar
        self.calendar = CalendarFrame(self)

        # create buttons for changing the date by either one day or two weeks or to some date
        self.left_week = Button(
            self, text="<<", font=FONT, command=lambda: self.calendar.change_by(week=-1)
        )
        self.left_day = Button(
            self, text="<", font=FONT, command=lambda: self.calendar.change_by(day=(-1))
        )

        self.calendar_button = Button(
            self, text="Date", font=FONT, width=MID_WIDTH, command=self.place_calendar
        )

        self.right_day = Button(
            self, text=">", font=FONT, command=lambda: self.calendar.change_by(day=1)
        )
        self.right_week = Button(
            self, text=">>", font=FONT, command=lambda: self.calendar.change_by(week=1)
        )

        # grid the button widgets
        self.left_week.grid(column=0, row=0, sticky="ens")
        self.left_day.grid(column=1, row=0, sticky="ens")

        self.calendar_button.grid(row=0, column=2, sticky="ns")

        self.right_day.grid(column=3, row=0, sticky="wns")
        self.right_week.grid(column=4, row=0, sticky="wns")

    def get_date(self):
        """
        Helper method that gets the date
        """
        return self.calendar.get_date()

    def place_calendar(self):
        """
        Helper method for placing the calendar at the appropriate spot:

        right below the calendar button, nicely centered
        """
        if self.calendar.place_info() == {}:
            x = (self.parent.winfo_width() // 2) - (self.calendar.winfo_reqwidth() // 2)
            y = self.winfo_y() + self.winfo_height() + 1
            self.calendar.place(x=x, y=y)
            self.calendar.update_idletasks()
        else:
            self.calendar.place_forget()


class MainApp(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # create a variable such that there can only be one popup at a time
        self.pop = Frame(self)

        # create buttons for the customers, services, and employees
        c_button = Button(
            self, text="Customers", font=FONT, width=10, command=self.customer_pop
        )
        e_button = Button(
            self, text="Employees", font=FONT, width=10, command=self.employee_pop
        )
        s_button = Button(
            self, text="Services", font=FONT, width=10, command=self.service_pop
        )

        # create the calendar buttons
        calendar_frame = DateFrame(self)
        today_button = Button(
            self,
            text="Today",
            width=MID_WIDTH,
            font=FONT,
            command=calendar_frame.calendar.toToday,
        )

        # create a pointer to the string variable of the calendar date
        self.dateVar = calendar_frame.calendar.dateVar

        # grid the buttons
        c_button.grid(column=0, row=0, sticky="w")
        e_button.grid(column=0, row=0, sticky="e")
        s_button.grid(column=0, row=1, sticky="e")

        today_button.grid(column=0, row=0, sticky="ns")
        calendar_frame.grid(column=0, row=1, sticky="ns")

        # create a label for the day and the date
        Label(self, textvariable=self.dateVar, font=FONT).grid(
            column=0, row=2, sticky="new"
        )
        ttk.Separator(self, orient="horizontal").grid(column=0, row=2, sticky="new")
        ttk.Separator(self, orient="horizontal").grid(column=0, row=2, sticky="sew")

        # create the scheduling sheet
        day = date.strftime(calendar_frame.get_date(), "%A").lower()
        with open(SCH_PATH, "r") as file:
            try:
                employees = json.load(file)[day]
            except:
                employees = None
        # TODO note the possible arg for employees
        sheet = MainSheet(self, employees)
        # TODO: is the below needed?
        self.bind_all("<Visibility>", lambda e: self.update_idletasks())

        # grid the sheet
        sheet.grid(column=0, row=3, sticky="nsew", padx=4)

    def customer_pop(self):
        """
        Helper method for creating a customer popup
        """
        self.pop.destroy()
        self.pop = CustomerPop(self)

    def employee_pop(self):
        """
        Helper method for creating a employee popup
        """
        self.pop.destroy()
        self.pop = EmployeePop(self)

    def service_pop(self):
        """
        Helper method for creating a service popup
        """
        self.pop.destroy()
        self.pop = ServicePop(self)
