import pygame
from pygame.locals import *

#import mob

class Laserbeam(pygame.sprite.Sprite):
    
    def __init__(self, pos, dirs):
        pygame.sprite.Sprite.__init__(self)
        
        self.pos = pos
        self.dirs = dirs
        

    def update(self, tilesize):
        self.image = pygame.Surface((tilesize, tilesize)).convert_alpha()
        self.image.fill((192, 64, 0, 128))
        x, y = self.pos
        self.rect = pygame.Rect(x * tilesize, y * tilesize, tilesize, tilesize)
        