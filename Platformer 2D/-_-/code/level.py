import pygame
from tiles import Tile
from Settings import tile_size ,screen_width ,screen_height
from player import Player
from particle import particle_effect
class Level:
    def __init__(self,level_data,surface):

        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift = 0 # przesuwanie-level
        self.touching_wall_x = 0

        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_to_ground = False

    def create_jump_particle(self,pos):
        if self.player.sprite.facing_right:
            pos -= pygame.math.Vector2(1,5)
        else:
            pos += pygame.math.Vector2(1,-5)
        jump_particle_sprite = particle_effect(pos,'jump')
        self.dust_sprite.add(jump_particle_sprite)

    def player_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_to_ground = True
        else:
            self.player_to_ground = False

    def create_land_particle(self):
        if not self.player_to_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
            if self.player.sprite.facing_right:
                offset = pygame.math.Vector2(20, 15)
            else:
                offset = pygame.math.Vector2(-20, 15)
            fall_partice = particle_effect(self.player.sprite.rect.midbottom - offset,'land')
            self.dust_sprite.add(fall_partice)
    def setup_level(self,layout): # tworzenie-level
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        for row_index,row in enumerate(layout):
            for col_index,cell in enumerate(row):

                x = col_index * tile_size
                y = row_index * tile_size

                if cell == 'X':
                    tile = Tile((x,y),tile_size)
                    self.tiles.add(tile)
                if cell == 'P':
                    player_sprite = Player((x,y),self.display_surface,self.create_jump_particle)
                    self.player.add(player_sprite)

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width / 4 and direction_x < 0 :
            self.world_shift = 5
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0 :
            self.world_shift = -5
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 5

    def horisontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed 

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
               if player.direction.x < 0:
                   player.rect.left = sprite.rect.right
                   player.on_left = True
                   self.touching_wall_x = player.rect.left
               elif player.direction.x > 0:
                   player.rect.right = sprite.rect.left
                   player.on_right = True
                   self.touching_wall_x = player.rect.right

            if player.on_left and (player.rect.left < self.touching_wall_x or player.direction.x >= 0 ):
                player.on_left = False
            if player.on_right and (player.rect.right > self.touching_wall_x or player.direction.x <= 0):
                player.on_right = False
    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
       
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
               if player.direction.y > 0:
                   player.rect.bottom = sprite.rect.top
                   player.direction.y = 0
                   player.on_ground = True
               elif player.direction.y < 0:
                   player.rect.top = sprite.rect.bottom
                   player.direction.y = 0
                   player.on_ceiling = True

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False

    def run(self):

        self.dust_sprite.update(self.world_shift)  # particle
        self.dust_sprite.draw(self.display_surface)

        self.tiles.update(self.world_shift) # bloki
        self.tiles.draw(self.display_surface)
        self.scroll_x()

        self.player.update()  # gracz
        self.horisontal_movement_collision()
        self.player_on_ground()
        self.vertical_movement_collision()
        self.create_land_particle()
        self.player.draw(self.display_surface)