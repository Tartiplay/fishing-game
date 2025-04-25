import pyxel
from camera import camera
from water import water
from fish import Fish
from particles import particles

class Game:
    def __init__(self):
        pyxel.init(240, 160)
        camera.init(0, 0)
        pyxel.load("fishing.pyxres")
        water.init(80, 480)
        self.objects = []
        self.objects.append(Fish(50, -20, 16, 8))
        self.objects.append(Fish(100, -40, range=200, max_speed=2))
        pyxel.run(self.update, self.draw)
#
    def update(self):
        # Controls
        if pyxel.btn(pyxel.KEY_UP):
            camera.move(0, -1)
        if pyxel.btn(pyxel.KEY_DOWN):
            camera.move(0, 1)
        if pyxel.btn(pyxel.KEY_LEFT):
            camera.move(-1, 0)
        if pyxel.btn(pyxel.KEY_RIGHT):
            camera.move(1, 0)
        if pyxel.btnp(pyxel.KEY_Q):
            camera.rumble_v(20, 5)
        if pyxel.btnp(pyxel.KEY_A):
            camera.rumble_h(10, 15)

        if pyxel.btnp(pyxel.KEY_D):
            self.objects[0].state = "deleted"
        
        # Update objects
        for obj in self.objects:
            obj.update()
            if obj.state == "deleted":
                self.objects.remove(obj)
       
        # Update particles
        for particle in particles:
            particle.update()
            if particle.state == "deleted":
                particles.remove(particle)


        # Update camera position
        camera.update()

    def draw(self):
        pyxel.cls(0)

        # Draw background
        pyxel.bltm(0, 0, 0, 0, 0, 480, 320)
        water.draw()

        # Draw objects
        for obj in self.objects: obj.draw()

        # Draw particles
        for particle in particles:
            particle.draw()

Game()