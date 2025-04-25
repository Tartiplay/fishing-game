import pyxel

class Camera:

    def __init__(self):
        # Effects variables
        self.rumble_force = 0
        self.rumble_reduction = 0
        self.fx_duration = 0

    def init(self, x, y, viewport=[240, 160], limits=[0, 0, 480, 320]):
        self.x, self.y = None, None
        self.screen_width, self.screen_height = viewport
        self.set_position(x, y)
        self.state = 0

        # Limits
        self.min_x, self.min_y, self.max_x, self.max_y = limits

    def set_position(self, x, y):
        self.x, self.y = x, y

    def get_position(self):
        return (self.x, self.y)
    
    def center_to(self, x, y):
        self.x = x - self.screen_width // 2
        self.y = y - self.screen_height // 2

    def center_to_object(self, obj):
        self.center_to(obj.x + obj.width // 2, obj.y + obj.height // 2)
    
    def move(self, x, y):
        self.x += x
        self.y += y
    
    def rumble(self, duration=30, force=5):
        self.fx_duration = duration
        self.rumble_force = force
        self.rumble_reduction = force / duration

    def rumble_v(self, duration=30, force=5):
        self.state = "rumble_v"
        self.rumble(duration, force)

    def rumble_h(self, duration=30, force=5):
        self.state = "rumble_h"
        self.rumble(duration, force)

    def update(self):
        # Limit camera position to the defined area
        self.x = max(self.min_x, min(self.x, self.max_x-self.screen_width))
        self.y = max(self.min_y, min(self.y, self.max_y-self.screen_height))

        # Update camera position
        pyxel.camera(self.x, self.y)

        # Rumble vertical effect
        if self.state == "rumble_v":
            if self.fx_duration > 0:
                if self.fx_duration % 2 == 0:
                    pyxel.camera(self.x, self.y + self.rumble_force)
                else:
                    pyxel.camera(self.x, self.y - self.rumble_force)
                self.rumble_force -= self.rumble_reduction
                self.fx_duration -= 1
            else:
                self.state = None

        # Rumble horizontal effect
        if self.state == "rumble_h":
            if self.fx_duration > 0:
                if self.fx_duration % 2 == 0:
                    pyxel.camera(self.x + self.rumble_force, self.y)
                else:
                    pyxel.camera(self.x - self.rumble_force, self.y)
                self.rumble_force -= self.rumble_reduction
                self.fx_duration -= 1
            else:
                self.state = None
        
camera = Camera()