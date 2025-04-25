import pyxel
import math
from water import water
from particles import generateSplash
from camera import camera

class Player:
    IMG = 1
    U = 0
    V = 0
    DX = 1

    def __init__(self):
        pass

    def init(self, x, y):
        self.x = x
        self.y = y
        self.width = 16
        self.height = 16
        self.direction = 1

    def move_left(self):
        self.x -= self.DX
        if self.x < camera.min_x: self.x = camera.min_x
        self.direction = -1
    
    def move_right(self):
        self.x += self.DX
        if self.x > camera.max_x - self.width: self.x = camera.max_x - self.width
        self.direction = 1

    def update(self):
        self.y = self.y + math.sin(pyxel.frame_count/10)/5

    def draw(self):
        if self.direction == 1:
            pyxel.blt(self.x,
            self.y,
            self.IMG,
            self.U,
            self.V,
            -self.width,
            self.height, colkey=0)
        else:
            pyxel.blt(self.x,
            self.y,
            self.IMG,
            self.U,
            self.V,
            self.width,
            self.height, colkey=0)

player = Player()

class Bobber:
    IMG = 0
    U = 32
    V = 0
    WIDTH = 8
    HEIGHT = 8
    DX = 1
    lancer = 0

    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.original_direction = direction
        self.state = "launched"
        self.dither = 0

    def update(self):
        if self.state == "launched":
            self.dither += 0.2
            self.x += (self.direction)
            self.y += 1
            if (self.direction == 1 and self.x > camera.max_x) or (self.direction == -1 and self.x < camera.min_x): self.direction = -self.direction
            if self.y > water.y:
                self.dither = 1
                self.state = "immerged"
                self.y = water.y
                generateSplash(self.x, water.y, 30, 3)
        if self.state == "immerged":
            self.y = self.y + math.sin(pyxel.frame_count/10)/5
        if self.state == "retrieving":
            self.dither -= 0.1
            self.x += -self.original_direction
            self.y -= 1
            generateSplash(self.x, self.y, 1, 1)
            if self.x > player.x and self.x < player.x + player.width:
                self.state = "deleted"


    
    def move_left(self):
        if self.state == "immerged" :
            self.x -= self.DX
    
    def move_right(self):
        if self.active == "immerged" :
            self.x += self.DX

    def draw(self):
        pyxel.dither(self.dither)
        pyxel.circ(self.x, self.y, 3, 7)
        pyxel.dither(1)