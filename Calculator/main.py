from tkinter import *
from tkinter.ttk import *
from application import *
from settings import *


def main():
   root = Tk()
   root.geometry(str.format("{}x{}+{}+{}", WIDTH, HEIGHT, starting_x, starting_y))
   Application.__change_Title__(title)
   app = Application()
   root.mainloop()





main()