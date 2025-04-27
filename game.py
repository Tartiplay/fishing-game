import pyxel
from camera import camera, VIEWPORT
from water import water
from background import background
from fish import Fish
from particles import particles, generateSplash
from player import player, Bobber
from hamecon import Hamecon
from minigame import FishingMiniGame, FishingStatus

def test_collision(obj1, obj2):
    return (obj1.x < obj2.x + obj2.width and
            obj1.x + obj1.width > obj2.x and
            obj1.y < obj2.y + obj2.height and
            obj1.y + obj1.height > obj2.y)

class Game:
    def __init__(self):
        pyxel.init(240, 160)
        camera.init(0, 0, limits=[0, 0, 320, 240])
        pyxel.load("game.pyxres")
        water.init(80, 480)
        player.init(160, 50)
        self.bobber = []
        self.objects = []
        #self.objects.append(Fish(50, -20, 16, 8))
        #self.objects.append(Fish(100, -40, range=200, max_speed=2))
        self.launch_forces = ["L", "M", "H"]
        self.launch_force = 0
        self.launch_count = 0
        self.fishing = False
        self.catched_fish = []
        self.Fish_catched = 0

        tile_fish_easy = (1, 0)
        tile_fish_regular = (2, 0)
        tile_fish_hard = (3, 0)

        # Create fishes
        for x in range(0, 40):
            for y in range(0, 31):
                tile = pyxel.tilemaps[0].pget(x, y)
                pyxel.tilemaps[0].pset(x, y, (0, 1))
                fish_range = pyxel.rndi(50, 200)
                if (x*8 + fish_range) > camera.max_x:
                    fish_range = camera.max_x - x*8
                if tile == tile_fish_easy:
                    self.objects.append(Fish(x*8, -(y*8), range=fish_range, max_speed=1, difficulty="easy", stop_y=y*8))
                if tile == tile_fish_regular:
                    self.objects.append(Fish(x*8, -(y*8), range=fish_range, max_speed=1.5, difficulty="regular", stop_y=y*8))
                if tile == tile_fish_hard:
                    self.objects.append(Fish(x*8, -(y*8), range=fish_range, max_speed=2, difficulty="hard", stop_y=y*8))
        self.Nb_fish = len(self.objects)
        pyxel.playm(0, loop=True)
        pyxel.run(self.update, self.draw)

    def update(self):
        # Rain
        if pyxel.frame_count % 10 == 0:
            for x in range(0, camera.max_x, 8):
                generateSplash(x, -20, 2, 1)
        
        # Only move player or bobber when we are not fishing
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
            if len(self.bobber) < 1: player.move_left()
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
            if len(self.bobber) < 1: player.move_right()

        if pyxel.btn(pyxel.KEY_SPACE) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_A):
            if len(self.bobber) < 1:
                self.launch_count += 1
                if self.launch_count % 15 == 0:
                    self.launch_force = (self.launch_force + 1) % 3

        if pyxel.btnr(pyxel.KEY_SPACE) or pyxel.btnr(pyxel.GAMEPAD1_BUTTON_A):
            if self.launch_count > 0:
                self.bobber.append(Bobber(player.x + (0 if player.direction == -1 else player.width), player.y, player.direction, self.launch_force+1))
                self.launch_count = 0
                self.launch_force = 0
            else:
                if len(self.bobber) >= 1 and self.bobber[0].hamecon.y <= self.bobber[0].y:
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
                pyxel.play(2, 7)
                camera.rumble_v()
                self.objects.remove(obj)
            else:
                # test collision with hamecon and fish
                if len(self.bobber) > 0 and test_collision(self.bobber[0].hamecon, obj) and obj.state == "water" and self.fishing == False:
                    obj.state = "catched"
                    self.catched_fish.append(obj)
       
        # Update particles
        for particle in particles:
            particle.update()
            if particle.state == "deleted":
                particles.remove(particle)


        # Update camera position
        if self.fishing:
            pass
        elif len(self.bobber) > 0 and self.bobber[0].state in ["launched","retrieving"]:
            camera.center_to_object(self.bobber[0])
        elif len(self.bobber) > 0 and self.bobber[0].state == "immerged":
            camera.center_to_object(self.bobber[0].hamecon)
        else:
            camera.center_to_object(player)
        camera.update()
        
        # =============================================================================
        # TMP: Press F to start fishing
        if not self.fishing and len(self.catched_fish) > 0:
            
            # Create fishing minigame
            self.fishing = FishingMiniGame(
                viewport = VIEWPORT, camera_x = camera.x, camera_y = camera.y,
                distance = 300, difficulty = self.catched_fish[0].difficulty
            )
            
            # If we are fishing, run the minigame until we reach success of failure
        elif self.fishing:

            # Block hamecon
            self.bobber[0].hamecon.state = "catch"
           
            # Run minigame
            self.fishing.update()
            
            # Do something on success
            if self.fishing.status == FishingStatus.SUCCESS:
                self.message = "Well done, you caught the fish"
                self.fishing = False
                self.catched_fish[0].state = "deleted"
                self.bobber[0].hamecon.state = "balancing"
                self.Fish_catched +=1
                self.catched_fish.pop()
            
            # Do something on failure
            elif self.fishing.status == FishingStatus.FAILURE:
                self.message = "The fish is gone with your bait"
                self.fishing = False
                self.catched_fish[0].state = "deleted"
                self.bobber[0].hamecon.state = "balancing"
                self.catched_fish.pop()
            
            # Do something on abort fishing
            # elif self.fishing.status == FishingStatus.ABORT:
            #     self.message = "You let the fish go with your bait"
            #     self.fishing = False
            #     self.catched_fish[0].state = "deleted"
            #     self.bobber[0].hamecon.state = "balancing"
            #     self.catched_fish.pop()
                
        # --- UPDATE BACKGROUND ---
        background.update(player)
        

    def draw(self):
        pyxel.cls(0)

        # Draw background
        pyxel.bltm(0, 0, 0, 0, 0, 480, 320)
        background.draw()
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
        
        #Draw hook
        if len(self.bobber) > 0:
            if self.bobber[0].state == "immerged":
                if self.bobber[0].hamecon:
                    self.bobber[0].hamecon.draw()
                    pyxel.line(self.bobber[0].x,self.bobber[0].y,self.bobber[0].hamecon.x,self.bobber[0].hamecon.y,7)
            
        # Draw fishing minigame
        if self.fishing:
            self.fishing.draw()

        # Draw UI
        if self.launch_count > 0:
            pyxel.circ(player.x+player.width/2+1, player.y - 10, 5, 7)
            pyxel.circb(player.x+player.width/2+1, player.y - 10, 5, [11, 9, 8][self.launch_force])
            pyxel.text(player.x+player.width/2, player.y - 12, self.launch_forces[self.launch_force], [11, 9, 8][self.launch_force])
        
        #Draw count fish
        pyxel.text(camera.x, camera.y, str(self.Fish_catched) + " / " + str(self.Nb_fish) + " Fishes caught", 10)

        if len(self.objects) == 0:
            pyxel.text(camera.x, camera.y + 10, "You've caught %s fishes. Are you proud ?!"%self.Fish_catched, 10)

Game()