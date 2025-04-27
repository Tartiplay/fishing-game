import pyxel
from camera import camera
import math
from water import water

class Hamecon:
    IMG = 1
    U = 32
    V = 0
    WIDTH = 8
    HEIGHT = 8
    DX = 1
    lancer = 0

    def __init__(self, bobberX, bobberY):
        self.x = bobberX
        self.y = bobberY
        self.en_peche = 0
        self.range_canne = 60
        self.vitesse_hamecon = 2
        self.cible_x = 0
        self.cible_y = 0
        self.width = self.WIDTH
        self.height = self.HEIGHT
        self.depth_limit = camera.max_y - self.height
        self.max_x = camera.max_x - self.width
        self.min_x = camera.min_x
        self.state = "balancing"

    def update(self, bobberX, bobberY):
        if self.state == "balancing":
            self.x = bobberX
            self.dep_hamecon(bobberY)
            self.x = self.x + ((self.y - water.y)/10)*math.sin(pyxel.frame_count/20)
    
    def move_left(self):
        self.x -= self.DX
    
    def move_right(self):
        self.x += self.DX

         

    def dep_hamecon(self, bobberY):
         #Déplacement du hamecon
         #Descente du hamecon
         if self.state == "balancing":
            if self.y < self.depth_limit :
                # if pyxel.btn(pyxel.KEY_DOWN):
                #     self.y += self.vitesse_hamecon
                self.y += 0.5
            #Remontée du hamecon limité à la hauteur du bouchon       
            if self.y > bobberY :
                if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
                    self.y -= self.vitesse_hamecon

    def draw(self):
        pyxel.blt(
            x = self.x,
            y = self.y,
            img = self.IMG,
            u = self.U,
            v = self.V,
            w = self.WIDTH,
            h = self.HEIGHT,
            colkey = 0
        )