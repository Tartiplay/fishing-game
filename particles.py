import pyxel
from water import water

particles = []

class Particle:

    def __init__(self, x, y, vx, vy, color):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.state = "alive"

    def update(self):
        pass

    def draw(self):
        pass

class Splash(Particle):

    def __init__(self, x, y, speed):
        vy = (-speed/3)+pyxel.rndf(-1, 1)
        vx = pyxel.rndf(-1, 1)
        super().__init__(x, y, vx, vy, [1,5,6,12][pyxel.rndi(0,3)])

    def update(self):
        self.vy += 0.1
        self.x += self.vx
        self.y += self.vy
        if self.y > water.y:
            self.state = "deleted"

    def draw(self):
        pyxel.pset(int(self.x), int(self.y), self.color)

def generateSplash(x, y, number, speed):
    for i in range(number):
        particles.append(Splash(x, y, speed))

class Bubble(Particle):

    def __init__(self, x, y, speed):
        vy = (speed/3)+pyxel.rndf(-1, 1)
        vx = pyxel.rndf(-1, 1)
        self.r = 0
        super().__init__(x, y, vx, vy, [1,5,6,12][pyxel.rndi(0,3)])

    def update(self):
        if self.r < 5 and pyxel.frame_count % 2 == 0:
            self.r += 0.1
        self.vy -= 0.075
        self.x += self.vx
        self.y += self.vy
        if self.y < water.y:
            self.state = "deleted"

    def draw(self):
        pyxel.circb(int(self.x), int(self.y), self.r, self.color)

def generateBubble(x, y, number, speed):
    for i in range(number):
        particles.append(Bubble(x, y, speed))