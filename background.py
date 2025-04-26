import pyxel
from camera import camera


TILESIZE = 8
IMG = 0
HILL_U = 16
HILL_V = 16
MOUNTAIN_U = 48
MOUNTAIN_V = 16
    
    

class Background: 
    
    def __init__(self):
        # Player movement
        self.previous_camera_x = 400
        
        # Hills
        self.hills_patches_x = [
            -100, -86, -30, -20, 0, 40, 70, 140, 200, 300, 340, 400
            ]
        self.hills_w = TILESIZE * 4
        self.hills_parallax_factor = 0.6
        
        # Mountains
        self.mountains_x = [80, 420, 100, 340]
        self.mountains_w = TILESIZE * 4
        self.moutain_parallax_factor = 0.3
    
    
    def update(self, player):
        # Calc change in player position
        delta_x = camera.x - self.previous_camera_x
        
        # Update layers based on parallax factor
        for i, hill_x in enumerate(self.hills_patches_x):
            hill_x -= delta_x * self.hills_parallax_factor
            self.hills_patches_x[i] = hill_x
        
        for i, mountain_x in enumerate(self.mountains_x):
            mountain_x -= delta_x * self.moutain_parallax_factor
            self.mountains_x[i] = mountain_x
        
        # Update the previous player x position
        self.previous_camera_x = camera.x
        
    
    def draw(self):
        for moutain_x in self.mountains_x:
            pyxel.blt(
                x = moutain_x,
                y = TILESIZE * 2,
                img = IMG,
                u = MOUNTAIN_U,
                v = MOUNTAIN_V,
                w = self.mountains_w,
                h = TILESIZE * 3,
                colkey = 0
            )
            
        for hill_x in self.hills_patches_x:
            pyxel.blt(
                x = hill_x,
                y = TILESIZE * 2,
                img = IMG,
                u = HILL_U,
                v = HILL_V,
                w = self.hills_w,
                h = TILESIZE * 3,
                colkey = 0
            )

    
background = Background()