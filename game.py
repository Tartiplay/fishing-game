import pyxel
from camera import camera
from water import water
from fish import Fish
from particles import particles
from player import Player

class Game:
    def __init__(self):
        pyxel.init(240, 160)
        camera.init(0, 0)
        pyxel.load("game.pyxres")
        water.init(80, 480)
        self.player = Player(240, 80-16)
        self.objects = []
        self.objects.append(Fish(50, -20, 16, 8))
        self.objects.append(Fish(100, -40, range=200, max_speed=2))
        pyxel.run(self.update, self.draw)
#
    def update(self):
        # Controls
        if pyxel.btn(pyxel.KEY_UP):
            pass
        if pyxel.btn(pyxel.KEY_DOWN):
            pass
        if pyxel.btn(pyxel.KEY_LEFT):
            self.player.move_left()
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.player.move_right()

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
        camera.center_to_object(self.player)
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

        # Draw player
        self.player.draw()

Game()