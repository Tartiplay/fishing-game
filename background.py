import pyxel


TILESIZE = 8
IMG = 0
HILL_U = 16
HILL_V = 16
    
    

class Background: 
    
    def __init__(self):
        # Player movement
        self.previous_player_x = 400
        
        # Forest
        self.hill_patches_x = [0, 40, 70, 100, 140, 200, 300, 340, 400]
        self.hill_w = TILESIZE * 4
        self.hill_parallax_factor = 0.3
    
    
    def update(self, player):
        # Calc change in player position
        delta_x = player.x - self.previous_player_x
        
        # Update layers based on parallax factor
        for id, hill_x in enumerate(self.hill_patches_x):
            hill_x -= delta_x * self.hill_parallax_factor
            self.hill_patches_x[id] = hill_x
        
        # Update the previous player x position
        self.previous_player_x = player.x
        
    
    def draw(self):
        for hill_x in self.hill_patches_x:
            pyxel.blt(
                x = hill_x,
                y = TILESIZE * 2,
                img = IMG,
                u = HILL_U,
                v = HILL_V,
                w = self.hill_w,
                h = TILESIZE * 3,
                colkey = 0
            )

    
background = Background()