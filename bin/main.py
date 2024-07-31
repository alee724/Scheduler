import sys

sys.path.insert(0, "../lib/scheduler/")
from service import *
from customer import *
from tkinter import *
from customerFrame import *

s1 = Service("P", 18, CTime(0, 30))
s2 = Service("M", 20, CTime(0, 30))
s3 = Service("W", 40, CTime(0, 15))
s4 = Service("E", 50, CTime(1, 10))
s5 = Service("L", 30, CTime(1, 0))
c1 = Customer("a", "l", services=[s1, s2, s3])
c2 = Customer("b", "l", services=[s2, s4, s5])


if __name__ == "__main__":
    root = Tk()
    root.attributes("-fullscreen", True)
    root.title("Scheduler")
    root.configure(background="red")

    root.grid_columnconfigure(list(range(0, 5)), weight=1, uniform="col")
    root.grid_rowconfigure(list(range(5)), weight=1, uniform="row")
    # root.grid_columnconfigure(0, weight=0)

    test = Frame(root)

    cf1 = CustomerFrame(root, customer=c1)
    cf1.grid(row=0, column=0, sticky="nsew")
    cf2 = CustomerFrame(root, customer=c2)
    cf2.grid(row=1, column=1, sticky="nsew")

    root.mainloop()
