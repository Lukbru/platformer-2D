from os import walk
import pygame

def import_folder(path):
    surface_list = []

    for _,__,img_filles in walk(path):
        for image in img_filles:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list