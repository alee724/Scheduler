import sys

sys.path.insert(0, "../lib/scheduler/")
from sheetFrame import *
from tkinter import *
from customer import *
from service import *

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

    style = Style(root)
    style.theme_use("default")

    main_sheet = MainSheet(root, ["test"])
    main_sheet.pack(fill=BOTH, expand=True)


    root.mainloop()
