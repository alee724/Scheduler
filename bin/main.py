from tkinter import Tk
from tkinter.constants import *
from app import MainApp

if __name__ == "__main__":
    root = Tk()
    root.title("Scheduler")
    root.configure(background="red")
    root.state("zoomed")
    root.resizable(0, 0)

    main = MainApp(root)
    main.pack(fill=BOTH, expand=True)

    root.mainloop()
