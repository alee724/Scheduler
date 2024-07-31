import json
from tkinter.ttk import *
from tkinter import *
from customer import *
from column import *
from service import *
import sys

sys.path.insert(0, "../lib/scheduler/")


class CustomerFrame(Frame):
    def __init__(self, parent, customer):
        """
        Class representing the frame for a customer

        Will load in data from a Customer object if there is one or create a new customer and
        create a customer frame from customer data
        """
        Frame.__init__(self, parent)
        assert isinstance(customer, Customer)

        # basic attributes needed
        self.bind_name = list(self.bindtags())[0]
        self.expand = True
        self.parent = parent
        self.customer = customer

        # grid configuration
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_propagate(False)

        # Variables used to modify widgets if needed
        self.name = StringVar(value=self.customer.getName())
        self.services = StringVar()
        self.price = StringVar()

        # Widgets using the above variables 
        name_label = Label(
            self,
            textvariable=self.name,
            font=("Helvetica Mono", 10),
            anchor="w",
        )
        services_label = Label(
            self, textvariable=self.services, font=("Helvetica Mono", 10), anchor="nw"
        )
        price_label = Label(
            self, textvariable=self.price, font=("Helvetica Mono", 10), anchor="e"
        )

        # set the service and price string
        self.services_to_string()
        self.service_price_to_string()

        # ========== Grid Children Widgets
        name_label.grid(row=0, column=0, sticky="nw")
        services_label.grid(row=1, column=0, sticky="nsew")
        price_label.grid(row=2, column=0, sticky="sew")

        self.popup = Menu(self, tearoff=0)
        self.popup.add_command(label="Shrink/Expand")
        self.popup.add_command(label="Add Service")
        self.popup.add_command(label="Split")
        self.popup.add_separator()
        self.popup.add_command(label="Delete", command=lambda: self.destroy())

        # ========== Bindings and Bindtag ==========
        # binding for the widget to have some fixed size
        self.bind(
            "<Map>",
            lambda e: self.configure(
                width=self.winfo_width(), height=self.winfo_height()
            ),
        )

        # add binding for the menu to appear
        self.bind("<Button-2>", self.popup_command)

        # binding for dnd
        self.bind("<ButtonPress-1>", self.on_press)
        self.bind("<B1-Motion>", self.on_motion)
        self.bind("<ButtonRelease-1>", self.on_release)

        # transfer binding to parent
        name_label.bindtags(list(name_label.bindtags()) + [self.bind_name])
        services_label.bindtags(list(services_label.bindtags()) + [self.bind_name])
        price_label.bindtags(list(price_label.bindtags()) + [self.bind_name])

    def popup_command(self, e):
        """
        Command for creating the visiual popup widget
        """
        try:
            self.popup.tk_popup(e.x_root, e.y_root, 0)
        finally:
            self.popup.grab_release()

    def service_price_to_string(self):
        """
        Updates the total price of the services that the customer has
        """
        total_price = sum(
            list(map(lambda s: s.getPrice(), self.customer.getServices()))
        )
        self.price.set(str(total_price))

    def services_to_string(self):
        """
        Updates the string of services that a customer has to be aethetically pleasing
        """
        tup_lst = list(
            map(lambda s: (s.getAbbrev(), s.getPrice()), self.customer.getServices())
        )
        new_str = "\n".join(
            list(map(lambda t: f"{t[0]}{' '*(5-len(t[0]))}  {t[1]}", tup_lst))
        )
        self.services.set(new_str)

    def on_press(self, e):
        """
        When the widget is clicked, i.e. before being dragged
        """
        wid = e.widget
        data = self.grid_info()
        wid.initCol = data["column"]
        wid.initRow = data["row"]
        wid.rowspan = data["rowspan"]
        wid._start_x = e.x
        wid._start_y = e.y

    def on_motion(self, e):
        """
        When the widget is being dragged
        """
        wid = e.widget
        new_x = self.winfo_x() - wid._start_x + e.x
        new_y = self.winfo_y() - wid._start_y + e.y
        self.place(x=new_x, y=new_y)

    def on_release(self, e):
        """
        When the widget is released and needs to be grid in its new place
        """
        wid = e.widget
        x = self.winfo_x() + (self.winfo_width()//2)
        y = self.winfo_y() + 30
        grid_data = self.parent.grid_location(x, y)
        col = grid_data[0]
        row = grid_data[1]
        if True:  # replace True with a query to the sheet module
            self.grid(in_=self.parent, column=col, row=row, rowspan=wid.rowspan)
