import pygame
from support import import_folder
from Settings import screen_height

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,surface,create_jump_particle):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)

        self.import_particle()
        self.particle_frame_index = 0
        self.particle_animation_speed = 0.15
        self.display_surface = surface
        self.create_jump_particle = create_jump_particle

        self.direction = pygame.math.Vector2(0,0)
        self.speed = 5 # Player speed
        self.gravity = 0.5
        self.jump_speed = -12

        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
        self.on_left = False
        self.on_right = False
        self.on_ceiling = False


    def import_character_assets(self):
        character_path = '../graphics/'
        self.animations = {'idle':[],'run':[],'jump':[],'fall':[]}

        for animation in self.animations.keys():
            full_path = character_path + animation # '../graphics' + 'idle' (itd.)
            self.animations[animation] = import_folder(full_path)

    def import_particle(self):
        self.particle_run = import_folder('../graphics/particles/run')
    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]
        if self.facing_right:
         self.image = image
        else :
            flipped_image = pygame.transform.flip(image,True,False)
            self.image = flipped_image

        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright = self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft = self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop = self.rect.midtop)

    def run_particle_animation(self):
        if self.status == 'run' and self.on_ground:
            self.particle_frame_index += self.particle_animation_speed
            if self.particle_frame_index >= len(self.particle_run):
                self.particle_frame_index = 0
            dust_particle = self.particle_run[int(self.particle_frame_index)]

            if self.facing_right:
                pos = self.rect.bottomleft - pygame.math.Vector2(30,32)
                self.display_surface.blit(dust_particle,pos)
            else:
                pos = self.rect.bottomright - pygame.math.Vector2(0,32)
                flipped_dust_particle = pygame.transform.flip(dust_particle,True,False)
                self.display_surface.blit(flipped_dust_particle,pos)



    def get_input(self):
     keys = pygame.key.get_pressed()

     if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        self.direction.x = 1
        self.facing_right = True
     elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
        self.direction.x = -1
        self.facing_right = False
     else:
        self.direction.x = 0 

     if keys[pygame.K_SPACE] and self.on_ground:
         self.jump()
         self.create_jump_particle(self.rect.midbottom)

    def get_status(self):
     if self.direction.y < 0:
         self.status = 'jump'
     elif self.direction.y > 1:
         self.status = 'fall'
     else:
         if self.direction.x != 0:
             self.status = 'run'
         else:
             self.status = 'idle'

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y
        if self.rect.y > screen_height:
            self.rect.y = -64
            self.direction.y = -5

    def jump(self):
        self.direction.y = self.jump_speed
   

    def update(self):
        self.get_input()
        self.get_status()
        self.animate()
        self.run_particle_animation()
