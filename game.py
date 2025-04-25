import pyxel
from camera import camera
from water import water
from fish import Fish
from particles import particles
from player import player, Bobber

class Game:
    def __init__(self):
        pyxel.init(240, 160)
        camera.init(0, 0)
        pyxel.load("game.pyxres")
        water.init(80, 480)
        player.init(440, 80-16)
        self.bobber = []
        self.objects = []
        self.objects.append(Fish(50, -20, 16, 8))
        self.objects.append(Fish(100, -40, range=200, max_speed=2))
        self.launch_forces = ["L", "M", "H"]
        self.launch_force = 0
        self.launch_count = 0
        pyxel.run(self.update, self.draw)
#
    def update(self):
        # Controls
        if pyxel.btn(pyxel.KEY_UP):
            pass
        if pyxel.btn(pyxel.KEY_DOWN):
            pass
        if pyxel.btn(pyxel.KEY_LEFT):
            if len(self.bobber) < 1: player.move_left()
        if pyxel.btn(pyxel.KEY_RIGHT):
            if len(self.bobber) < 1: player.move_right()

        if pyxel.btn(pyxel.KEY_SPACE):
            if len(self.bobber) < 1:
                self.launch_count += 1
                if self.launch_count % 10 == 0:
                    self.launch_force = (self.launch_force + 1) % 3

        if pyxel.btnr(pyxel.KEY_SPACE):
            if self.launch_count > 0:
                self.bobber.append(Bobber(player.x + (0 if player.direction == -1 else player.width), player.y, player.direction, self.launch_force+1))
                self.launch_count = 0
                self.launch_force = 0
            else:
                if len(self.bobber) >= 1:
                    self.bobber[0].state = "retrieving"

        player.update()

        for bobber in self.bobber:
            bobber.update()
            if bobber.state == "deleted":
                self.bobber.remove(bobber)

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
        camera.center_to_object(player)
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
        player.draw()

        # Draw bobber
        for bobber in self.bobber:
            pyxel.line(player.x + (0 if player.direction == -1 else player.width), player.y+5, bobber.x, bobber.y,7)
            bobber.draw()

        # Draw UI
        if self.launch_count > 0:
            pyxel.text(player.x+player.width/2, player.y - 10, self.launch_forces[self.launch_force], [11, 9, 8][self.launch_force])

Game()