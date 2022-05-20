import sys
import random
from PIL import Image, ImageTk
from tkinter import Tk, Frame, Canvas, ALL, NW
from board import *


class Snake(Frame):
    def __init__(self):
        super(Snake, self).__init__()
        self.master.title("Snake")
        self.board = Board()
        self.pack()

def main():
    root = Tk()
    nib = Snake()
    root.mainloop()

main()