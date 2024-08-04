import sys

sys.path.insert(0, "../lib/scheduler/")
from service import *
from customer import *
from tkinter import *
from sheetFrame import *

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

    main = MainSheet(root)
    main.pack(fill=BOTH, expand=True)

    root.mainloop()

# root = Tk()
#
# root.attributes("-fullscreen", True)
#
# canvas = Canvas(root, background="red", highlightthickness=0)
# canvas.pack(fill=BOTH, expand=True)
#
#
# f1 = Frame(canvas, relief="groove", borderwidth=1, width=2000, height=100)
# f1.pack_propagate(False)
# Label(f1, text="test").pack(side=LEFT)
# Label(f1, text="test").pack(side=RIGHT)

# text_id = canvas.create_window((0, 0), window=f1, anchor="nw")
#
# # canvas.configure(scrollregion=canvas.bbox("all"))
# canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
# canvas.bind_all(
#     "<MouseWheel>",
#     lambda e: canvas.yview_scroll(-1 * (e.delta), "units")
#     if e.state == 0
#     else canvas.xview_scroll(-1 * (e.delta), "units"),
# )
# root.mainloop()
