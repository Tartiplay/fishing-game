import pyxel
from water import water
from particles import generateSplash, generateBubble

class Fish:
    def __init__(self, x, y, width=8, height=8, range=100, max_speed=10, acceleration=0.01, difficulty="easy"):
        self.start_x = x  # Position initiale x
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.direction = 1  # 1 pour droite, -1 pour gauche
        self.range = range  # Plage de mouvement
        self.speed_x = 0  # Vitesse de déplacement en x
        self.speed_y = 0 # Vitesse de déplacement en y
        self.max_speed = max_speed  # Vitesse maximale
        self.acceleration = acceleration  # Taux d'accélération
        self.difficulty = difficulty
        if self.y < water.y:
            self.state = "air"
        else:
            self.state = "water"

    def update(self):
        # Si le poisson est en l'air, le faire tomber
        if self.state == "air":
            self.speed_y += 0.1
            self.y += self.speed_y
            if self.y >= water.y:
                self.state = "entering_water"
                generateSplash(self.x+self.width/2, water.y, 50, self.speed_y)
                generateBubble(self.x+self.width/2, water.y, 10, self.speed_y)
        
        if self.state == "entering_water":
            self.speed_y -= 0.2
            self.y += self.speed_y
            if self.speed_y <= 0:
                self.state = "water"
                self.speed_y = 0
        
        if self.state == "water":
            # Position des bornes
            left_limit, right_limit = self.start_x, self.start_x + self.range - self.width + 1

            # Distance restante avant les bornes
            distance_to_right, distance_to_left = right_limit - self.x, self.x - left_limit

            # Calcul de la distance nécessaire pour s'arrêter (formule du MRUA) et ajuster la vitesse
            stopping_distance = (self.speed_x ** 2) / (2 * self.acceleration)
            if (self.direction == 1 and distance_to_right <= stopping_distance) or (self.direction == -1 and distance_to_left <= stopping_distance):
                self.speed_x = max(0, self.speed_x - self.acceleration)
            else:
                self.speed_x = min(self.max_speed, self.speed_x + self.acceleration)

            # Inversion de la direction si on atteint une borne
            if self.speed_x == 0:
                self.direction *= -1

            # Màj de la position
            self.x += self.speed_x * self.direction

            # Clamp au cas où on dépasse les bornes
            self.x = max(left_limit, min(right_limit, self.x))

            # Génération de bulles
            if pyxel.frame_count % pyxel.rndi(100,200) == 0:
                generateBubble(self.x if self.direction == -1 else self.x + self.width, self.y + self.height/2, pyxel.rndi(1,3), 1)
        
        if self.state == "deleted":
            generateBubble(self.x+self.width/2, self.y+self.height/2, 100, 1)

    def draw(self):
        pyxel.rect(self.x, self.y, self.width, self.height, 11)  # Couleur 11 (jaune)

fishes = []
