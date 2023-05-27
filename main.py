import pygame as pg
from pygame.time import Clock

pg.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

WIDTH = 800
HEIGHT = 600

FLOOR = 500

screen= pg.display.set_mode((WIDTH, HEIGHT), vsync = 1)
pg.display.set_caption("Character movement")

clock = Clock()

class Player:
    x = 300.0
    y = 300.0
    vel_x = 5
    vel_y = 5
    speed = 1
    grounded = False
    walled = 0
    drag = 0.3
    
    RADIUS = 20

    def __init__(self):
        self.gravity = 0.5

        self.x += self.vel_x # FIXME: Redundant operation
        self.y += self.vel_y
        

    def update(self):
        """Executed every frame for the player
        """
        self.grounded = False
        
        self.accelerate(0, self.gravity)
        
        if self.vel_x > 10:
            self.vel_x = 10
        elif self.vel_x < -10:
            self.vel_x = -10
            
        if self.vel_y > 10:
            self.vel_y = 10
        elif self.vel_y < -10:
            self.vel_y = -10
        
        self.x += self.vel_x
        self.y += self.vel_y
        
        if self.x < self.RADIUS:
            self.x = self.RADIUS
            self.vel_x = 0
            self.walled = 1
        if self.x > WIDTH - self.RADIUS:
            self.x = WIDTH - self.RADIUS
            self.vel_x = 0
            self.walled = -1
        if self.y < self.RADIUS:
            self.y = self.RADIUS
            self.vel_y = 0
        if self.y > HEIGHT - self.RADIUS:
            self.y = HEIGHT - self.RADIUS
            self.vel_y = 0
            self.grounded = True
        
        if self.walled != 0:
            self.vel_y = 1
    
        if self.grounded:
            self.walled = 0
    
        if self.x - self.RADIUS < 0:
            self.vel_x = abs(self.vel_x)
        elif self.x + self.RADIUS > WIDTH:
            self.vel_x = -abs(self.vel_x)

        if self.y - self.RADIUS < 0:
            self.vel_y = abs(self.vel_y)
        elif self.y + self.RADIUS > HEIGHT:
            self.vel_y = -abs(self.vel_y)

    def jump(self):
        if not self.grounded: return
        self.vel_y = -15
        
    def jump_wall(self):
        if self.walled == 0: return
        self.vel_x = self.walled * 20
        self.vel_y = -10
        self.walled = 0

    def move(self, x: int|None=None, y: int|None =None):
        if x is not None:
            self.x += x
        if y is not None:
            self.y += y

    def accelerate(self, x=0.0, y=0.0):
        self.vel_x += x
        self.vel_y += y

    def draw(self):
        global screen
        pg.draw.circle(screen, WHITE, (self.x, self.y), self.RADIUS)
        
def sign(x: float) -> float:
    return -1 if x < 0 else (0 if x == 0 else 1)

ourPlayer = Player()

running = True

if running:
    pass

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                if ourPlayer.walled != 0:
                    ourPlayer.jump_wall()
                    
    keys = pg.key.get_pressed()

    if ourPlayer.walled == 0:
        if keys[pg.K_a]:
            ourPlayer.accelerate(-ourPlayer.speed)
        if keys[pg.K_d]:
            ourPlayer.accelerate(ourPlayer.speed)
    
    ourPlayer.accelerate(-sign(ourPlayer.vel_x) * ourPlayer.drag, 0)
        
    if keys[pg.K_SPACE]:
        ourPlayer.jump()
    
    screen.fill(BLACK)
    
    ourPlayer.update()
    ourPlayer.draw()
    
    pg.display.flip()
    clock.tick(60)
