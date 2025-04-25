import pyxel
import camera
import math

class Water:

    def __init__(self):
        self.u = 16
        self.tile_width = 16
        self.x = -self.tile_width
        self.height = 40
        
    def init(self, y, width):
        self.y = y
        self.width = width+self.tile_width
        # pyxel.images[1].load(0, 0, "resources/water_surface.png")

    def draw(self):
        for y in range(self.u, self.u + self.height):
            for x in range(self.x, self.width, self.tile_width):
                pyxel.blt(math.sin(y/3+(pyxel.frame_count/10))+x, self.y-self.height+y-self.u, 0, 0, y, self.tile_width, 1)

water = Water()
