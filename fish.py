import pyxel
from water import water
from particles import generateSplash, generateBubble
from camera import camera
import math



IMG = 1
FISH_SPRITE = {
    "easy": { "u": 0, "v": 24, "w": 16, "h": 8 },
    "regular": { "u": 0, "v": 32, "w": 16, "h": 8 },
    "hard": { "u": 0, "v": 40, "w": 8, "h": 8 },
}



class Fish:
    def __init__(self, x, y, width=8, height=8, range=100, max_speed=10, acceleration=0.01, difficulty="easy", stop_y=50):
        self.start_x = x  # Position initiale x
        self.x = x
        self.y = y
        # self.width = width
        # self.height = height
        self.width = FISH_SPRITE[difficulty]["w"]
        self.height = FISH_SPRITE[difficulty]["h"]
        self.direction = 1  # 1 pour droite, -1 pour gauche
        self.range = range  # Plage de mouvement
        self.speed_x = 0  # Vitesse de déplacement en x
        self.speed_y = 0 # Vitesse de déplacement en y
        self.max_speed = max_speed  # Vitesse maximale
        self.acceleration = acceleration  # Taux d'accélération
        self.difficulty = difficulty
        self.stop_y = stop_y
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
                pyxel.play(2, 8)
                camera.rumble_v()
                self.state = "entering_water"
                generateSplash(self.x+self.width/2, water.y, 50, self.speed_y)
                generateBubble(self.x+self.width/2, water.y, 10, self.speed_y)
        
        if self.state == "entering_water":
            self.y += self.speed_y/3

            # Clamp la position y pour ne pas dépasser le point d'arrêt
            if self.y >= self.stop_y:
                self.y = self.stop_y
                self.speed_y = 0
                self.state = "water"
        
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
        # pyxel.rect(self.x, self.y, self.width, self.height, 11)
        pyxel.blt(
            x = self.x,
            y = self.y,
            img = IMG,
            u = FISH_SPRITE[self.difficulty]["u"],
            v = FISH_SPRITE[self.difficulty]["v"],
            w = FISH_SPRITE[self.difficulty]["w"] * self.direction,
            h = FISH_SPRITE[self.difficulty]["h"],
            colkey = 0
        )

fishes = []
