import pygame as pg

pg.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

WIDTH = 800
HEIGHT = 600

screen= pg.display.set_mode((WIDTH, HEIGHT), vsync = 1)
pg.display.set_caption("Character movement")

class Player:
    x = 300
    y = 300
    speed = 1

ourPlayer = Player()

running = True

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    keys = pg.key.get_pressed()
    if keys[pg.K_a]:
        ourPlayer.x -= ourPlayer.speed
    if keys[pg.K_d]:
        ourPlayer.x += ourPlayer.speed
    if keys[pg.K_SPACE]:
        print("Player jumped!!!!!!!!!")
    
    screen.fill(BLACK)
    
    pg.draw.circle(screen, WHITE, (ourPlayer.x, ourPlayer.y), 20)
    pg.display.flip()
    
    pg.display.update()
