import pyxel
from enum import Enum
from random import randrange



import pyxel
from enum import Enum
from random import randrange



# App level constants
TILE_SIZE = 8
SCREEN_HEIGHT = 160
SCREEN_WIDTH = 240

# Module level constants
Y = TILE_SIZE * 4



# Fishing status
class FishingStatus(Enum):
    ONGOING = 'ongoing'
    SUCCESS = 'success'
    FAILURE = 'failure'
    ABORT = 'abort'



# Fishing mini-game patterns (12 slots inside the current frame)
### Easy
E_01 = [
    ['slow', 1],
    ['medium', 2],
    ['fast', 6],
    ['medium', 2],
    ['slow', 1]
]
E_02 = [
    ['slow', 1],
    ['medium', 4],
    ['fast', 5],
    ['medium', 1],
    ['slow', 1]
]
E_03 = [
    ['slow', 1],
    ['medium', 1],
    ['fast', 5],
    ['medium', 4],
    ['slow', 1]
]

### Regular
R_01 = [
    ['slow', 2],
    ['medium', 2],
    ['fast', 4],
    ['medium', 2],
    ['slow', 2]
]
R_02 = [
    ['slow', 1],
    ['medium', 1],
    ['fast', 4],
    ['medium', 3],
    ['slow', 3]
]
R_03 = [
    ['slow', 3],
    ['medium', 3],
    ['fast', 4],
    ['medium', 1],
    ['slow', 1]
]

### Hard
H_01 = [
    ['slow', 3],
    ['medium', 1],
    ['fast', 1],
    ['medium', 2],
    ['fast', 2],
    ['medium', 1],
    ['slow', 2]
]
H_02 = [
    ['slow', 2],
    ['medium', 1],
    ['fast', 2],
    ['medium', 2],
    ['fast', 1],
    ['medium', 1],
    ['slow', 3]
]
H_03 = [
    ['slow', 1],
    ['medium', 1],
    ['fast', 2],
    ['medium', 1],
    ['slow', 3],
    ['medium', 1],
    ['fast', 1],
    ['medium', 1],
    ['slow', 1]
]



# Store fishing mini-game patterns and speeds by difficulty
PATTERNS = {
    'easy': {
        'speeds': { 'slow': -2, 'medium': 1, 'fast': 3 },
        'patterns': [E_01, E_02, E_03]
    },
    'regular': {
        'speeds': { 'slow': -2, 'medium': 1, 'fast': 3 },
        'patterns': [R_01, R_02, R_03]
    },
    'hard': {
        'speeds': { 'slow': -2, 'medium': 1, 'fast': 3 },
        'patterns': [H_01, H_02, H_03]
    }
}



class Frame:
    def __init__(self, viewport, camera_x, camera_y):
        
        # Frame dimensions
        self.size = TILE_SIZE * 12
        self.xmin = camera_x + viewport[0] / 2 - self.size / 2
        self.xmax = self.xmin + self.size
        self.y = camera_y + 4 * TILE_SIZE
    
    
    def draw(self):
        # Orange line
        pyxel.rectb(
            x = self.xmin,
            y = self.y,
            w = self.size,
            h = TILE_SIZE,
            col = 9
        )
    
    
    def draw_bg(self):
        # Background line
        pyxel.rect(
            x = self.xmin - 10,
            y = self.y - 13,
            w = self.size + 20,
            h = TILE_SIZE + 20,
            col = 4
        )
        
        # Orange border
        pyxel.rectb(
            x = self.xmin - 10,
            y = self.y - 13,
            w = self.size + 20,
            h = TILE_SIZE + 20,
            col = 9
        )


class FishCursor:
    def __init__(self, frame):
        
        # Related objects
        self.frame = frame
        
        # Cursor dimensions
        self.size = TILE_SIZE
        self.x = frame.xmin + TILE_SIZE * 4
        self.y = frame.y
        
        # Cursor movement
        self.velocity = 0
        self.acceleration = 0.1
        self.deceleration = 0.2
        self.max_velocity = 6.0
        self.bounce = 0.6
    
    
    def move(self):
        # Accelerate to right when SPACE is pressed
        if pyxel.btn(pyxel.KEY_SPACE) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_A):
            
            # If speed < max, accelerate
            if self.velocity < self.max_velocity:
                self.velocity += self.deceleration
            
        # Accelerate to left when key is released
        else:
            
            # If speed < max, accelerate
            if self.velocity > -self.max_velocity:
                self.velocity -= self.acceleration
        
        # Calculate next position
        target_position = self.x + self.velocity
        
        # If we hit the sides, bounce
        if target_position >= self.frame.xmax - self.size - 1:
            self.velocity *= -self.bounce
        elif target_position <= self.frame.xmin + 1:
            self.velocity *= -self.bounce
        else:
            self.x = target_position
        
    
    
    def draw(self):
        pyxel.blt(
            x = self.x,
            y = self.y,
            img = 1,
            u = 0,
            v = 16,
            w = self.size,
            h = TILE_SIZE,
            colkey = 0
        )



class Pattern:
    def __init__(self, frame, cursor, difficulty):
        
        # Frame dimensions
        self.frame = frame
        
        # Related cursor
        self.cursor = cursor
        
        # Pattern to use
        self.pattern_difficulty = difficulty        
        self.pattern = self.pick_a_pattern(difficulty)
        
        # Speed
        self.speed = 1
    
    
    def pattern_color(self, type):
        if type == 'slow': 
            return 8
        elif type == 'medium':
            return 10
        elif type == 'fast':
            return 11
        else:
            return 0
    
    
    def pick_a_pattern(self, difficulty):
        # Get number of patterns available
        n_patterns = len(PATTERNS[difficulty]['patterns'])
        
        # Get random pattern between 0 and max number of patterns available
        pattern = randrange(0, n_patterns)       
        return pattern


    def update(self):
        # ===== Get speed at which we close the distance to the surface: =====
        # Get cursor center position
        cursor_center = self.cursor.x + (self.cursor.size / 2)
        
        # Get cursor speed from pattern
        pattern = PATTERNS[self.pattern_difficulty]['patterns'][self.pattern]
        
        # Find cursor position
        xmin = self.frame.xmin
        
        # Speed found?
        speed_found = False
        
        for p in pattern:
            if not speed_found:
                width = p[1] * TILE_SIZE
                xmax = xmin + width
                
                # Is the cursor between xmin and xmax?
                if cursor_center >= xmin and cursor_center < xmax:
                    speed_smf = p[0]
                    speed = PATTERNS[self.pattern_difficulty]['speeds'][speed_smf]
                    self.speed = speed
                    speed_found = True
                
                else:
                    xmin += width
    
    
    def draw(self):
        
        # Retrieve pattern to draw
        pattern = PATTERNS[self.pattern_difficulty]['patterns'][self.pattern]
        x = self.frame.xmin
        
        # Draw pattern sections
        for p in pattern:
            type = p[0]
            width = p[1] * TILE_SIZE
            
            pyxel.rect(
                x = x,
                y = self.frame.y,
                w = width,
                h = TILE_SIZE,
                col = self.pattern_color(type)
            )
            
            x += width

        
        
class FishingMiniGame:
    def __init__(self, viewport, camera_x, camera_y, distance = 300, difficulty = "easy"):
                
        # Related objects
        self.frame = Frame(viewport, camera_x, camera_y)
        self.cursor = FishCursor(frame = self.frame)
        self.pattern = Pattern(
            frame = self.frame,
            cursor = self.cursor,
            difficulty = difficulty
            )
        
        # Dimensions
        self.width = self.frame.size
        
        # Distance bar progress
        self.distance_max = distance
        self.distance_current = 40
        self.distance_speed = 1
        
        # Fishing mini-game events
        self.status = FishingStatus.ONGOING
    
    
    def update(self):
        
        # If fishing is ongoing, animate cursor
        self.cursor.move()
        
        # Get speed from pattern
        self.pattern.update()
        
        # Get current distance cursor speed
        self.distance_speed = self.pattern.speed
        # print(f"Speed: {self.pattern.speed} || Speed px: {self.distance_speed}")
        
        # Close distance to the surface
        self.distance_current += self.distance_speed
        
        # Handle success and failure
        if self.status == FishingStatus.ONGOING:
            if self.distance_current >= self.distance_max: # SUCCESS
                self.status = FishingStatus.SUCCESS
                
            elif self.distance_current < 0: # FAILURE
                self.status = FishingStatus.FAILURE
            
            # elif pyxel.btnp(pyxel.KEY_BACKSPACE): # ABORT
            #     self.status = FishingStatus.ABORT

    
    def draw(self):
        
        # Draw frame bg
        self.frame.draw_bg()
               
        # Draw pattern
        self.pattern.draw()
        
        # Draw frame
        self.frame.draw()
        
        # If fishing is ongoing, animate cursor
        self.cursor.draw()
        
        # Draw distance bar - frame
        pyxel.rect(
            x = self.frame.xmin,
            y = self.frame.y - 7,
            w = self.frame.size,
            h = 4,
            col = 4
        )
                
        pyxel.rectb(
            x = self.frame.xmin,
            y = self.frame.y - 7,
            w = self.frame.size,
            h = 4,
            col = 11
        )
        
        # Draw distance bar - fill
        current_width = int(self.distance_current * self.width / self.distance_max)
        if current_width <= self.width:
            width = current_width
        else:
            width = self.width
        
        pyxel.rect(
            x = self.frame.xmin,
            y = self.frame.y - 7,
            w = width,
            h = 4,
            col = 11
        )