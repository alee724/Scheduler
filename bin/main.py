from tkinter import Tk
import tkinter.ttk as ttk
from tkinter.constants import *
from constants import *
from app import MainApp

if __name__ == "__main__":
    root = Tk()
    root.title("Scheduler")
    root.configure(background="red")
    root.state("zoomed")
    root.resizable(0, 0)

    style = ttk.Style()
    # autochange the font size of listed items in comboboxes
    root.option_add("*TCombobox*Listbox*Font", FONT)

    main = MainApp(root)
    main.pack(fill=BOTH, expand=True)

    root.mainloop()
