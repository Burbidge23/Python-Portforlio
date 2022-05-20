import random
from tkinter import *
from tkinter.ttk import *
import time


class Application(Frame):

    def titleset(self):
        title = "CPS"
        Application.title = title

    def __init__(self):
        super(Application, self).__init__()
        self.titleset()
        self.clicks = []
        self.cps = '   0  '
        self.initUI()

    def initUI(self):
        self.master.title(Application.title)
        self.style = Style()
        self.pack(fill=BOTH, expand=1)

        self.clickbttn = Button(self, text="Click Me!", command=self.click)
        self.clickbttn.grid(row=2, column=0)

        self.cps_label = Label(self, text=str(self.cps), width=15)
        self.cps_label.grid(row=1, column=0)

    def click(self):
        now = time.time()
        self.clicks.append(time.time())

        start_time = now - 1

        while self.clicks and self.clicks[0] < start_time:
            self.clicks.pop(0)

        if len(self.clicks) > 1:
            self.cps = len(self.clicks) / (self.clicks[-1] - self.clicks[0])
            self.cps = round(self.cps, 2)
            self.cps = "{:.2f}".format(self.cps).zfill(5)
            self.cps_label.config(text=str(self.cps))
        else:
            self.cps = '  <1 '
            self.cps_label.config(text=str(self.cps))


