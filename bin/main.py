import sys

sys.path.insert(0, "../lib/scheduler/")
from app import *
from sheetFrame import *
from customer import *
from service import *
from popUp import *


s1 = Service("P", 18, CTime(0, 30))
s2 = Service("M", 20, CTime(0, 30))
s3 = Service("W", 40, CTime(0, 15))
s4 = Service("E", 50, CTime(1, 10))
s5 = Service("L", 30, CTime(1, 0))
sl = [s1, s2, s3, s4, s5]
sl = list(map(lambda s: Service.toJSON(s), sl))

c1 = Customer("a", "l", [s1, s2, s3], "1234567890")
c2 = Customer("b", "l", [s1, s2], "0987654321")
c3 = Customer("c", "l", [s1])
cl = [c1, c2, c3]


if __name__ == "__main__":
    root = Tk()
    root.title("Scheduler")
    root.configure(background="red")
    # root.attributes("-fullscreen", True)
    CustomerPop(root)
    # ServicePop(root)

    root.mainloop()
