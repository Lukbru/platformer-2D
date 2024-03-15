import pygame, sys
from Settings import *
from level import Level

pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('2D_platformer_slime')
clock = pygame.time.Clock()
level = Level(level_map,screen)
background_music = pygame.mixer.Sound('..\graphics\music\Lvl1s.mp3')
background_music.set_volume(0.2)
background_music.play(loops = -1)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                level.create_block(event.pos)


    screen.fill('black')
    level.run()

    pygame.display.update()
    clock.tick(60)