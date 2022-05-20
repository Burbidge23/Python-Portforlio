from tkinter import *
from tkinter.ttk import *


class Application(Frame):
    title = "New GUI"

    expression = ""


    def __init__(self):
        super(Application, self).__init__()
        self.initUI()

    def initUI(self):
        self.master.title(Application.title)
        self.style = Style()
        self.pack(fill=BOTH, expand=1)

        self.equation = StringVar()

        self.txtbx = Entry(self, textvariable=self.equation)
        self.txtbx.grid(row=0, column=1, columnspan=4)

        self.sevenbttn = Button(self, text="7", command=lambda: self.press(7))
        self.sevenbttn.grid(row=1, column=1)
        self.eightbttn = Button(self, text="8", command=lambda: self.press(8))
        self.eightbttn.grid(row=1, column=2)
        self.ninebttn = Button(self, text="9", command=lambda: self.press(9))
        self.ninebttn.grid(row=1, column=3)
        self.fourbttn = Button(self, text="4", command=lambda: self.press(4))
        self.fourbttn.grid(row=2, column=1)
        self.fivebttn = Button(self, text="5", command=lambda: self.press(5))
        self.fivebttn.grid(row=2, column=2)
        self.sixbttn = Button(self, text="6", command=lambda: self.press(6))
        self.sixbttn.grid(row=2, column=3)
        self.onebttn = Button(self, text="1", command=lambda: self.press(1))
        self.onebttn.grid(row=3, column=1)
        self.twobttn = Button(self, text="2", command=lambda: self.press(2))
        self.twobttn.grid(row=3, column=2)
        self.threebttn = Button(self, text="3", command=lambda: self.press(3))
        self.threebttn.grid(row=3, column=3)
        self.zerobttn = Button(self, text="0", command=lambda: self.press(0))
        self.zerobttn.grid(row=4, column=1)

        self.entrbttn = Button(self, text="Enter", command= self.equalpress)
        self.entrbttn.grid(row=4, column=3)

        self.minusbttn = Button(self, text="-",command=lambda: self.press("-"))
        self.minusbttn.grid(row=1, column=4)

        self.plusbttn = Button(self, text = "+",command=lambda: self.press("+"))
        self.plusbttn.grid(row=2, column=4)

        self.dividebttn = Button(self, text="/",command=lambda: self.press("/"))
        self.dividebttn.grid(row=3, column=4)

        self.multbttn = Button(self, text="x",command=lambda: self.press("*"))
        self.multbttn.grid(row=4, column=4)

        self.clearbttn = Button(self, text="Clear",command= self.clear)
        self.clearbttn.grid(row=5,column=3)

        self.decibttn = Button(self, text=".",command=lambda: self.press("."))
        self.decibttn.grid(row=4,column=2)

    def __change_Title__(title):
        Application.title = title

    def press(self, num):
        Application.expression = Application.expression + str(num)
        self.equation.set(Application.expression)

    def clear(self):
        Application.expression = ""
        self.equation.set("")

    def equalpress(self):
        try:
            total = str(eval(Application.expression))

            self.equation.set(total)
            Application.expression = ""
        except:

            self.equation.set(" error ")
            Application.expression = ""


