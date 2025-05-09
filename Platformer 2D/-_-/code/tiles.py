import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,size):
        super().__init__()
        self.image = pygame.image.load('../graphics/block/tile.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)

    def update(self,x_shift):
        self.rect.x += x_shift

class DissapearBlock(pygame.sprite.Sprite):
    def __init__(self,pos,size):
        super().__init__()
        self.image = pygame.image.load('../graphics/block/move_tile.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.timer = 0

    def update(self,x_shift):
        self.rect.x += x_shift
        self.timer += 1
        if self.timer >= 2 * 60:
            self.kill()

class MovingBlock(pygame.sprite.Sprite):
    def __init__(self, pos, size):
     super().__init__()
     self.image = pygame.image.load('../graphics/block/dis_tile.png').convert_alpha()
     self.rect = self.image.get_rect(topleft = pos)
     self.direction = 1
     self.update_time = pygame.time.get_ticks()

    def update(self,x_shift):
        self.rect.x += x_shift
        current_time = pygame.time.get_ticks()
        if current_time - self.update_time >= 3000:
            self.direction *=-1
            self.update_time = current_time

        self.rect.x += self.direction