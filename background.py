import pyxel


TILESIZE = 8
IMG = 0
FOREST_U = 16
FOREST_V = 16
    
    

class Background: 
    
    def __init__(self):
        # Player movement
        self.previous_player_x = 400
        
        # Forest
        self.forest_patches_x = [400, 200, 100]
        self.forest_w = TILESIZE * 4
        self.forest_parallax_factor = 0.3
    
    
    def update(self, player):
        # Calc change in player position
        delta_x = player.x - self.previous_player_x
        
        # Update layers based on parallax factor
        # self.forest_a_x -= delta_x * self.forest_parallax_factor
        for id, forest_x in enumerate(self.forest_patches_x):
            forest_x -= delta_x * self.forest_parallax_factor
            self.forest_patches_x[id] = forest_x
        
        # Update the previous player x position
        self.previous_player_x = player.x
        
    
    def draw(self):
        for forest_x in self.forest_patches_x:
            pyxel.blt(
                x = forest_x,
                y = TILESIZE * 2,
                img = IMG,
                u = FOREST_U,
                v = FOREST_V,
                w = self.forest_w,
                h = TILESIZE * 3,
                colkey = 0
            )

    
background = Background()