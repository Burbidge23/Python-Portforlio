from settings import *
import sys
import random
from PIL import Image, ImageTk
from tkinter import Tk, Frame, Canvas, ALL, NW


class Board(Canvas):
    def __init__(self):
        super(Board, self).__init__(width=BOARDWIDTH, height=BOARDHEIGHT, background="blue", highlightthickness=1)

        self.initGame()

        self.pack()

    def initGame(self):
        """ initializes the game and all elements of it """

        self.inGame = True
        self.dots = 3
        self.score = 0

        # Variables for moving the snake
        self.moveX = DOT_SIZE
        self.moveY = 0

        # starting apple coordinates
        self.appleX = 100
        self.appleY = 190

        # Call Game methods
        self.loadImages()
        self.createObjects()
        self.locateApple()
        self.bind_all("<Key>", self.onKeyPressed)
        self.after(DELAY, self.onTimer)

    def onTimer(self):
        self.drawScore()
        self.checkCollisions()
        if self.inGame:
            self.checkAppleCollision()
            self.moveSnake()
            self.after(DELAY, self.onTimer)
        else:
            self.gameOver()

    def drawScore(self):
        score = self.find_withtag("score")
        self.itemconfigure(score, text="Score: {0}".format(self.score), tag="score", fill="white")

    def gameOver(self):
        self.delete(ALL)
        self.create_text(self.winfo_width() / 2, self.winfo_height() / 2,
                         text="Game Over with score {}".format(self.score), fill="white")

    def checkCollisions(self):
        bodyParts = self.find_withtag("body")
        head = self.find_withtag("head")
        x1, y1, x2, y2 = self.bbox(head)
        overlap = self.find_overlapping(x1, y1, x2, y2)

        for part in bodyParts:
            for lap in overlap:
                if lap == part:
                    self.inGame = False

        if x1 < 0:
            self.inGame = False

        if x1 > BOARDWIDTH - DOT_SIZE:
            self.inGame = False

        if y1 < 0:
            self.inGame = False

        if y1 > BOARDHEIGHT - DOT_SIZE:
            self.inGame = False

    def checkAppleCollision(self):
        apple = self.find_withtag("apple")
        head = self.find_withtag("head")
        x1, y1, x2, y2 = self.bbox(head)
        overlap = self.find_overlapping(x1, y1, x2, y2)
        for lap in overlap:
            if apple[0] == lap:
                self.score += 1
                x, y = self.coords(apple)
                self.create_image(x, y, image=self.body_part, anchor=NW,tag="body")
                self.locateApple()

    def loadImages(self):
        """ load images from a file"""
        try:
            self.img_body = Image.open("images/body.png")
            self.img_head = Image.open("images/head.png")
            self.img_apple = Image.open("images/apple.png")
            self.body_part = ImageTk.PhotoImage(self.img_body)
            self.head = ImageTk.PhotoImage(self.img_head)
            self.apple = ImageTk.PhotoImage(self.img_apple)

        except IOError as e:
            print(e)
            sys.exit(1)

    def createObjects(self):
        """ create the objects o n the canvas """

        self.create_text(30, 10, text="Score: {0}".format(self.score), tag="score", fill="white")
        self.create_image(self.appleX, self.appleY, image=self.apple, anchor=NW, tag="apple")
        self.create_image(50, 50, image=self.head, anchor=NW, tag="head")
        self.create_image(40, 50, image=self.body_part, anchor=NW, tag="body")
        self.create_image(30, 50, image=self.body_part, anchor=NW, tag="body")

    def moveSnake(self):
        bodyParts = self.find_withtag("body")
        head = self.find_withtag("head")

        length = bodyParts+head
        z = 0
        while z < len(length)-1:
            c1 = self.coords(length[z])
            c2 = self.coords(length[z+1])
            self.move(length[z], c2[0]-c1[0], c2[1]-c1[1])
            z += 1
        self.move(head, self.moveX,self.moveY)

    def locateApple(self):
        """ places the apple object on the canvas """
        apple = self.find_withtag("apple")
        self.delete(apple[0])
        r = random.randint(0, MAX_RANDOM_POS)
        self.appleX = r * DOT_SIZE
        r = random.randint(0, MAX_RANDOM_POS)
        self.appleY = r * DOT_SIZE
        self.create_image(self.appleX, self.appleY, image=self.apple, anchor=NW, tag="apple")

    def onKeyPressed(self, e):
        key = e.keysym

        LEFT_CURSOR_KEY = "Left"
        RIGHT_CURSOR_KEY = "Right"
        UP_CURSOR_KEY = "Up"
        DOWN_CURSOR_KEY = "Down"

        if key == LEFT_CURSOR_KEY and self.moveX <= 0:
            self.moveX = -DOT_SIZE
            self.moveY = 0
        if key == RIGHT_CURSOR_KEY and self.moveX >= 0:
            self.moveX = DOT_SIZE
            self.moveY = 0

        if key == UP_CURSOR_KEY and self.moveY <= 0:
            self.moveX = 0
            self.moveY = -DOT_SIZE
        if key == DOWN_CURSOR_KEY and self.moveY <= 0:
            self.moveX = 0
            self.moveY = DOT_SIZE
