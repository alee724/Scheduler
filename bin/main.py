import sys

sys.path.insert(0, "../lib/scheduler/")
from popUp import *
from service import *
from customer import *
from sheetFrame import *
from app import *


if __name__ == "__main__":
    root = Tk()
    root.title("Scheduler")
    root.configure(background="red")
    # root.attributes("-fullscreen", True)

    s = EmployeePop(root)

    root.mainloop()
