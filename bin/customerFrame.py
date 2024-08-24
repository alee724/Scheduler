from initial import *
from constants import *
from tkinter import Frame, Label, StringVar, Toplevel, Menu
from tkinter.constants import *
import tkinter.ttk as ttk
from customer import *


class CustomerDetails(Frame):
    def __init__(self, parent, customer):
        """
        A class representing the pop up frame that will appear to display a more detailed view
        of a customer's needs
        """
        Frame.__init__(self, parent, width=200, height=100, padx=1, pady=1)
        assert isinstance(customer, Customer)
        if customer.getServed():
            self.configure(background="green")
        else:
            self.configure(background="red")

        # basic attributes needed
        self.bind_name = list(self.bindtags())[0]
        self.expand = True
        self.parent = parent
        self.customer = customer
        self.packed = False
        self.rowspan = 1

        # grid configuration
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_propagate(False)

        # Variables used to modify widgets if needed
        self.name = StringVar(value=self.customer.getName())
        self.services = StringVar()
        self.price = StringVar()

        # Widgets using the above variables
        self.name_label = Label(
            self,
            textvariable=self.name,
            font=FONT,
            anchor="w",
        )
        self.services_label = Label(
            self, textvariable=self.services, font=FONT, anchor="nw"
        )
        self.price_label = Label(self, textvariable=self.price, font=FONT, anchor="e")

        # ========== Grid Children Widgets
        self.name_label.grid(row=0, column=0, sticky="nw")
        self.services_label.grid(row=1, column=0, sticky="nsew")
        self.price_label.grid(row=2, column=0, sticky="sew")


class CustomerDetailsPop(Toplevel):
    def __init__(self, parent, customer):
        """
        A toplevel pop up window that will display the customer data in greater detail
        """
        Toplevel.__init__(self, parent)
        self.grid_rowconfigure(1, weight=1)

        Label(self, text=f"{customer.getName()}", font=FONT).grid(
            row=0, column=0, columnspan=2, sticky="nsew"
        )
        ttk.Separator(self, orient="horizontal").grid(
            column=0, columnspan=2, row=0, sticky="sew"
        )

        # Add a list view of services with their name and price
        services = customer.getServices()
        s_text = "\n".join(list(map(lambda s: s.getName(), services)))
        p_list = list(map(lambda s: s.getPrice(), services))
        p_text = "\n".join(list(map(lambda s: str(s.getPrice()), services)))
        Label(self, text=s_text, font=FONT, justify=LEFT).grid(
            column=0, row=1, sticky="nsw"
        )
        Label(self, text=p_text, font=FONT, justify=LEFT).grid(
            column=1, row=1, sticky="nsw"
        )
        ttk.Separator(self, orient="horizontal").grid(
            column=0, row=1, columnspan=2, sticky="swe"
        )

        # get the approximate total time it will take to do all the services
        t_list = list(map(lambda s: s.getTime(), services))
        t_time = CTime(0, 0)
        for t in t_list:
            t_time.add(t)

        # add the total price and total approximate time it will take
        Label(self, text=f"Total Price: {sum(p_list)}", anchor="w", font=FONT).grid(
            column=0, row=2, sticky="nw", padx=(0, 5)
        )
        Label(
            self, text=f"Total Time: {t_time.toString()}", anchor="e", font=FONT
        ).grid(column=1, row=2, sticky="ne")


class CustomerFrame(CustomerDetails):
    def __init__(self, parent, customer):
        """
        Class representing the frame for a customer

        Will load in data from a Customer object if there is one or create a new customer and
        create a customer frame from customer data

        The parent MUST be at least the base frame for the sheet or higher in the hierarchy,
        may just set the parent as root if anything
        """
        super().__init__(parent, customer)

        # set the service and price string
        self.services_to_string()
        self.service_price_to_string()

        # create the pop up menu once right clicking
        self.popup = Menu(self, tearoff=0)
        self.popup.add_command(
            label="details", command=lambda: CustomerDetailsPop(self, self.customer)
        )
        self.popup.add_separator()
        self.popup.add_command(label="Shrink/Expand")
        self.popup.add_command(label="Add Service")
        self.popup.add_command(label="Split")
        self.popup.add_separator()
        self.popup.add_command(
            label="Served", command=lambda: self.event_generate("<<VerifyServed>>")
        )
        self.popup.add_command(
            label="Delete",
            command=lambda: self.event_generate("<<VerifyDestroyCustomer>>"),
        )

        # ========== Bindings and Bindtag ==========
        # binding for the widget to have some fixed size
        self.bind(
            "<Map>",
            lambda e: self.configure(
                width=self.winfo_width(), height=self.winfo_height()
            ),
        )

        # add binding for the menu to appear
        self.bind("<Button-2>", lambda e: self.popup.tk_popup(e.x_root, e.y_root, 0))

        # binding for dnd
        self.bind("<ButtonPress-1>", self.on_press)
        self.bind("<B1-Motion>", self.on_motion)
        self.bind("<ButtonRelease-1>", self.on_release)

        # transfer binding to parent
        self.name_label.bindtags(list(self.name_label.bindtags()) + [self.bind_name])
        self.services_label.bindtags(
            list(self.services_label.bindtags()) + [self.bind_name]
        )
        self.price_label.bindtags(list(self.price_label.bindtags()) + [self.bind_name])

    def get_details(self):
        """
        Helper method for opening a toplevel window that displays the customer information in more
        detail
        """
        tl = Toplevel(self)
        CustomerFrame(tl, self.customer)

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
        if data != {}:
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
        self.event_generate("<<VerifyMoveCustomer>>")
