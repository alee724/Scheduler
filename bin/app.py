from sheetFrame import * 
from tkinter import *
import tkinter.ttk as ttk
from datetime import *

from tkcalendar import Calendar

FONT = ("Helvetica", 16)

# The following two widths are specifically for labels as their size go by character length
SIDE_WIDTH = 10
MID_WIDTH = 5


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
        select_button = Button(self, text="Select",
                               font=FONT, command=self.set_date)
        select_button.grid(column=0, row=1, sticky="w")
        cancel_button = Button(
            self, text="Cancel", font=FONT, command=lambda: self.place_forget()
        )
        cancel_button.grid(column=0, row=1, sticky="e")

        self.dateVar.trace("w", lambda *args: print(self.dateVar.get()))

    def change_by(self, day=0, week=0):
        """
        Changes the date by some amount of days or weeks
        """
        self.date += timedelta(days=day, weeks=week)
        self.dateVar.set(self.date.strftime("%m-%d-%y"))

    def change_to(self, day, month, year):
        """
        Changes the date to some day, month, and year
        """
        self.date = date(day=day, month=month, year=year)
        self.dateVar.set(self.date.strftime("%m-%d-%y"))

    def set_date(self):
        """
        Helper method that responds to the select button of the calendar

        Sets the string variable to the selected date and changes the self.date to the select date
        """
        string = self.cal.get_date()
        mdy = list(map(lambda x: int(x), string.split("-")))
        self.change_to(mdy[1], mdy[0], mdy[2])


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
            self,
            text="<<",
            font=FONT,
            command=lambda: self.calendar.change_by(week=-14),
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
            self, text=">>", font=FONT, command=lambda: self.calendar.change_by(week=14)
        )

        # grid the button widgets
        self.left_week.grid(column=0, row=0, sticky="ens")
        self.left_day.grid(column=1, row=0, sticky="ens")

        self.calendar_button.grid(row=0, column=2, sticky="ns")

        self.right_week.grid(column=3, row=0, sticky="wns")
        self.right_day.grid(column=4, row=0, sticky="wns")

    def place_calendar(self):
        """
        Helper method for placing the calendar at the appropriate spot:

        right below the calendar button, nicely centered
        """
        if self.calendar.place_info() == {}:
            x = (self.parent.winfo_width() // 2) - \
                (self.calendar.winfo_reqwidth() // 2)
            y = self.winfo_y() + self.winfo_height() + 1
            self.calendar.place(x=x, y=y)
            self.calendar.update_idletasks()
        else:
            self.calendar.place_forget()


class MainApp(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # create buttons for the customers, services, and employees
        c_button = Button(self, text="Customers",
                          font=FONT, width=10, command=None)
        e_button = Button(self, text="Employees",
                          font=FONT, width=10, command=None)
        s_button = Button(self, text="Services", font=FONT,
                          width=10, command=None)

         # create the calendar buttons
        calendar_frame = DateFrame(self)
        today_button = Button(
            self, text="Today", width=MID_WIDTH, font=FONT, command=None
        )

        # grid the buttons
        c_button.grid(column=0, row=0, sticky="w")
        e_button.grid(column=0, row=0, sticky="e")
        s_button.grid(column=0, row=1, sticky="e")

        calendar_frame.grid(column=0, row=1, sticky="ns")
        today_button.grid(column=0, row=0, sticky="ns")

        # create the scheduling sheet
        sheet = MainSheet(self) # note the possible arg for employees 

        # grid the sheet 
        sheet.grid(column=0, row=2, sticky="nsew")


