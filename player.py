import pyxel
import math

class Player:
    IMG = 1
    U = 0
    V = 0
    DX = 1

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 16
        self.height = 16

    def move_left(self):
        self.x -= self.DX
    
    def move_right(self):
        self.x += self.DX

    def update(self):
        pass

    def draw(self):
        y = self.y + math.sin(pyxel.frame_count/10)
        pyxel.blt(self.x,
        y,
        self.IMG,
        self.U,
        self.V,
        self.width,
        self.height, colkey=0)