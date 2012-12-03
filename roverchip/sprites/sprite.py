import math

import pygame

class Sprite(pygame.sprite.Sprite):

    def __init__(self, level, pos=(0, 0), facing=0):
        pygame.sprite.Sprite.__init__(self)
        
        # initial values
        self.level = level
        self.pos = pos
        self.facing = facing
        self.to_move = 0
        self.dead = 0
        
        # defaults to override
        self.colour = (0, 0, 0)
        self.layer = 0
        self.size = 1
        self.speed = 1
        self.is_movable = 0         # can be pushed by player
        self.is_solid = 0           # will stop things from entering its square
        self.is_enemy = 0           # will kill player on touch
        self.is_item = 0            # can be picked up by player
        self.is_destructible = 0    # will be destroyed by laserbeams
        
        
    def get_type(self):
        return self.__class__.__name__
    
    
    def cells_in(self):
        x, y = self.pos
        return set([
            (math.floor(x), math.floor(y)),
            (math.ceil(x), math.ceil(y)),
            (math.floor(x), math.ceil(y)),
            (math.ceil(x), math.floor(y))
            ])
            
            
    def do_turn(self, elapsed=0):
        self.start_turn()

        if elapsed > 0 and self.to_move:
            distance = self.speed * elapsed
            dirx, diry = [(0, -1), (1, 0), (0, 1), (-1, 0)][self.facing]
            dx, dy = dirx * distance, diry * distance
            
            if abs(dx) > self.to_move:
                dx = self.to_move * cmp(dx, 0)
            if abs(dy) > self.to_move:
                dy = self.to_move * cmp(dy, 0)
                
            x, y = self.pos
            self.pos = round(x + dx, 5), round(y + dy, 5) # round to avoid floating-point errors
            self.to_move -= max(abs(dx), abs(dy))

            if not self.to_move:
                self.after_move()
        
        
    def update(self, tilesize, offset):
        # either initialize image and rect, or just update rect
        x, y = self.pos
        ox, oy = offset
        left = (x + (1 - self.size) / 2) * tilesize - ox
        top = (y + (1 - self.size) / 2) * tilesize - oy
        size = tilesize * self.size
        
        if not hasattr(self, 'image') or tilesize != self.image.get_width():
            self.image = pygame.Surface((size, size))
            if len(self.colour) > 3:
                self.image = self.image.convert_alpha()
            self.image.fill(self.colour)
            self.rect = pygame.Rect(left, top, size, size)
        else:
            self.rect.left, self.rect.top = left, top
            
            
    def start_turn(self):
        pass
        

    def after_move(self):
        pass
    
    
    def check_collisions(self):
        pass