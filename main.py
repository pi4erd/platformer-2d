import pygame as pg
from enum import Enum
from pygame.time import Clock
from math import sin, radians

from colors import *

pg.init()

WIDTH = 1280
HEIGHT = 720

FLOOR = 500

screen= pg.display.set_mode((WIDTH, HEIGHT), vsync = 1)
pg.display.set_caption("Character movement")

clock = Clock()

def lerp(x1: float, y1: float, k: float) -> float: # really map though
    return (y1 - x1) * k + x1

class Camera:
    x=0.0
    y=0.0
    zoom = 0.9 # TODO: Implement zoom
    
    def __init__(self):
        pass
        
    def follow(self, x, y, k: float):
        self.x = lerp(self.x, x, k)
        self.y = lerp(self.y, y, k)
            
camera = Camera()

class Collision(Enum):
    TOP = 1
    BOTTOM = 2
    LEFT = 4
    RIGHT = 8

    def get_collision(result, collision) -> bool:
        return result | collision.value != 0

class Platform:
    def __init__(self, x: float, y: float, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
    
    def check_left(self, x, y):
        return x > self.x

    def check_right(self, x, y):
        return x < self.x + self.w
    
    def check_top(self, x, y):
        return y > self.y

    def check_bottom(self, x, y):
        return y < self.y + self.h
    
    def check_inside(self, x, y, r):
        top = self.check_bottom(x, y - r)
        bottom = self.check_top(x, y + r)
        left = self.check_left(x + r, y)
        right = self.check_right(x - r, y)
        
        return top and bottom and left and right

    def draw(self):
        global screen, camera
        local_x = self.x - (camera.x - WIDTH / 2)
        local_y = self.y - (camera.y - HEIGHT / 2)
        pg.draw.rect(screen, WHITE, pg.Rect(local_x, local_y, self.w, self.h))

platforms: list[Platform] = [Platform(200, 400, 100, 100), Platform(400, 400, 100, 100)]

class Player:
    ######### Properties
    x = 300.0
    y = 300.0
    vel_x = 0.0
    vel_y = 0.0
    speed = 1
    grounded = False
    walled = 0
    drag = 0.3
    #########
    
    ######### Constants
    RADIUS = 20
    #########
    
    def __init__(self): # On player initialize
        self.gravity = 0.5        

    def update(self): # Update player's state
        """Executed every frame for the player
        """
        self.grounded = False
        
        self.accelerate(0, self.gravity) # Accelerate using gravity
        
        if self.vel_x > 10: # Limit X to (-10, 10)
            self.vel_x = 10
        elif self.vel_x < -10:
            self.vel_x = -10
            
        if self.vel_y > 10:
            self.vel_y = 10
        elif self.vel_y < -10:
            self.vel_y = -10
            
        self.x += self.vel_x
        self.y += self.vel_y
        
        self.collide()
        
        if self.walled != 0: # If sticks to wall, limit velocity to 1
            self.vel_y = 1 if self.vel_y > 1 else self.vel_y
    
        if self.grounded:
            self.walled = 0
    
    def collide(self):
        for plat in platforms:
            if self.walled != 0:
                right = plat.check_inside(self.x + self.RADIUS + 0.1, self.y, 0)
                left = plat.check_inside(self.x - self.RADIUS - 0.1, self.y, 0)
                top = plat.check_inside(self.x, self.y - self.RADIUS - 0.1, 0)
                bottom = plat.check_inside(self.x, self.y + self.RADIUS + 0.1, 0)
                
                if (not right) and (not left): # FIXME: Multi-platform interaction is impossible
                    self.walled = 0
                if self.walled:
                    break
                
        for plat in platforms:
            check = plat.check_inside(self.x, self.y, self.RADIUS)
            if not check:
                break
        
            # FIXME: Walled continues to slide the player down
            if plat.y > self.y: # Is higher than platform
                self.y = plat.y - self.RADIUS
                self.vel_y = 0
                self.grounded = True
            elif plat.y + plat.h < self.y: # Is lower than platform
                self.y = plat.y + plat.h + self.RADIUS
                self.vel_y = 0
            elif plat.x > self.x: # Is left of platform
                self.x = plat.x - self.RADIUS
                self.vel_x = 0
                self.walled = -1
            elif plat.x + plat.w < self.x: # Is right of platform
                self.x = plat.x + plat.w + self.RADIUS
                self.vel_x = 0
                self.walled = 1

        self.check_borders()
    
    def check_borders(self):
        if self.x < self.RADIUS: # Check if left wall
            self.x = self.RADIUS
            self.vel_x = 0
            self.walled = 1
        if self.x > WIDTH - self.RADIUS: # Check if right wall
            self.x = WIDTH - self.RADIUS
            self.vel_x = 0
            self.walled = -1
        if self.y < self.RADIUS: # Check if top wall
            self.y = self.RADIUS
            self.vel_y = 0
        if self.y > HEIGHT - self.RADIUS: # Check if bottom wall
            self.y = HEIGHT - self.RADIUS
            self.vel_y = 0
            self.grounded = True
    
    def jump(self): # Jump
        if not self.grounded: return
        self.vel_y = -15
        
    def jump_wall(self): # Wall jump function
        if self.walled == 0: return
        self.vel_x = self.walled * 20
        self.vel_y = -10
        self.walled = 0
        self.walled_border = 0

    def move(self, x: int|None=None, y: int|None =None): # Move player w/o affecting his velocity
        if x is not None:
            self.x += x
        if y is not None:
            self.y += y

    def accelerate(self, x=0.0, y=0.0): # Accelerate player
        self.vel_x += x
        self.vel_y += y

    def draw(self): # Draw our player
        global screen, camera
        local_x = self.x - (camera.x - WIDTH / 2)
        local_y = self.y - (camera.y - HEIGHT / 2)
        pg.draw.circle(screen, WHITE, (local_x, local_y), self.RADIUS)
        
def sign(x: float) -> float: # Get sign of a number
    # XXX: Needs a builtin function for efficiency
    return -1 if x < 0 else (0 if x == 0 else 1)

ourPlayer = Player() # Create our player

running = True

while running: # TODO: Move while into a separate function
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            # Wall jump
            if event.key == pg.K_SPACE:
                if ourPlayer.walled != 0:
                    ourPlayer.jump_wall()
            if event.key == pg.K_PLUS or event.key == pg.K_KP_PLUS:
                zoom_in = True
            elif event.key == pg.K_MINUS or event.key == pg.K_KP_MINUS:
                zoom_out = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_PLUS or event.key == pg.K_KP_PLUS:
                zoom_in = False
            elif event.key == pg.K_MINUS or event.key == pg.K_KP_MINUS:
                zoom_out = False
    keys = pg.key.get_pressed() # Check if keys pressed
    
    if ourPlayer.walled == 0: # If doesn't stick to wall
        if keys[pg.K_a]: # Move left
            ourPlayer.accelerate(-ourPlayer.speed)
        if keys[pg.K_d]: # Move right
            ourPlayer.accelerate(ourPlayer.speed)
    
    # Add additional drag to stop moving continuously w/o pressing the button
    ourPlayer.accelerate(-sign(ourPlayer.vel_x) * ourPlayer.drag, 0) # FIXME: Drag creates fantom movement bug
    
    # Just jump
    if keys[pg.K_SPACE]:
        ourPlayer.jump()
        
    # Update our player
    camera.follow(ourPlayer.x, ourPlayer.y - 100, 0.1)
    ourPlayer.update()
    
    screen.fill(BLACK) # Set background
    
    ourPlayer.draw() # Draw player
    for plat in platforms:
        plat.draw()
        
    pg.display.flip() # Render all changes
    
    clock.tick(60) # Set framerate limit to 60 fps (may change in the future)
