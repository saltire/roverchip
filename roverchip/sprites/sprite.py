import math

import pygame


class Sprite(pygame.sprite.Sprite):
    def __init__(self, level, pos, facing=0):
        pygame.sprite.Sprite.__init__(self)
        
        # initial values
        self.level = level              # reference to level
        self.pos = pos                  # sprite's coords on cell grid
        self.facing = facing            # direction sprite is facing
        self.tile_facing = facing       # direction tile is facing
        self.to_move = 0                # tiles left to move
        self.move_dir = 0               # direction to move
        self.new_cell = False           # true after moving to a new cell
        
        # defaults to override
        self.tile = 0, 0                # coords of sprite's tile in tileset
        self.layer = 0                  # layer the sprite is rendered on
        self.size = 1                   # size of sprite in cells
        self.speed = 250                # number of ms to move one cell
        self.rotate = False             # tile rotates according to self.facing
        
        
    def get_type(self):
        """Return the type of the sprite, i.e. its class name."""
        return self.__class__.__name__
    
    
    def cells_in(self):
        """Return all cells that the sprite is touching."""
        x, y = self.pos
        return set([
            (math.floor(x), math.floor(y)),
            (math.ceil(x), math.ceil(y)),
            (math.floor(x), math.ceil(y)),
            (math.ceil(x), math.floor(y))
            ])
            
            
    def do_move(self, elapsed=0):
        """Run any hooks at the start of an object's turn, do any movement,
        and run any hooks if it is finished moving."""
        if elapsed > 0 and self.to_move:
            distance = elapsed / self.speed
            dirx, diry = ((0, -1), (1, 0), (0, 1), (-1, 0))[self.move_dir]
            dx, dy = dirx * distance, diry * distance
            
            if abs(dx) > self.to_move:
                dx = self.to_move * cmp(dx, 0)
            if abs(dy) > self.to_move:
                dy = self.to_move * cmp(dy, 0)
                
            x, y = self.pos
            self.pos = round(x + dx, 5), round(y + dy, 5) # round to avoid floating-point errors
            self.to_move -= max(abs(dx), abs(dy))

            if not self.to_move:
                self.new_cell = True
        
        
    def update(self, cellsize, offset, tileset):
        """Draw the actual sprite."""
        # either initialize image and rect, or just update rect
        x, y = self.pos
        ox, oy = offset
        left = (x + (1 - self.size) / 2) * cellsize - ox
        top = (y + (1 - self.size) / 2) * cellsize - oy
        size = int(cellsize * self.size)
        
        if (not hasattr(self, 'image') or cellsize != self.image.get_width()
            or self.tile_facing != self.facing):
            
            # grab tile from tileset, rotate and scale
            tileimg = tileset.get_tile(self.tile, self.facing)
            self.tile_facing = self.facing
            
            if self.size != 1:
                tileimg = pygame.transform.scale(tileimg, (size, size))
            
            # draw a new surface for the sprite using the tile
            self.image = pygame.Surface((size, size), pygame.SRCALPHA)
            self.image.blit(tileimg, (0, 0))
            
            # set position
            self.rect = pygame.Rect(left, top, size, size)

        else:
            # just set position
            self.rect.left, self.rect.top = left, top
            
            
    def start_turn(self):
        """A hook that is run at the start of every turn."""
        pass
        

    def after_move(self):
        """A hook that is run as soon as the sprite arrives in a new cell."""
        pass
    
    
    def end_turn(self):
        """A hook that is run after the movement phase of every turn."""
        pass
        

    def check_collisions(self):
        """A hook run after the end of every turn, for collision-related actions."""
        pass
    
