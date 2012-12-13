import pygame

import cell


class Ice(cell.Cell):
    def __init__(self, level, pos, facing=None):
        cell.Cell.__init__(self, level, pos)
        
        self.tile = 9, 0
        self.facing = facing
        self.robot_can_enter = False
        
        self.corner_tile = 10, 0

        # diagonal dir the corner is facing, clockwise from northeast (optional)
        self.facing = facing
        
        
    def draw(self, cellsize, tileset):
        """Draw the ice tile, then draw the rotated corner on top of it."""
        tx, ty = self.tile
        tileimg = tileset.subsurface((tx * cellsize, ty * cellsize, cellsize, cellsize)).copy()
        if self.facing is not None:
            # draw corner tile on top of ice tile
            tx, ty = self.corner_tile
            cornerimg = tileset.subsurface((tx * cellsize, ty * cellsize, cellsize, cellsize))
            cornerimg = pygame.transform.rotate(cornerimg, self.facing * -90)              
            tileimg.blit(cornerimg, (0, 0))
        return tileimg
        

    def get_out_dir(self, in_dir):
        """Given a sprite's movement direction, return the direction the sprite
        will exit the cell."""
        if self.facing is None:
            return in_dir
        
        # reverse in_dir to get from_dir
        # if from_dir is one of the facing dirs, return the other one
        from_dir = (in_dir + 2) % 4
        out_dirs = self.facing, (self.facing + 1) % 4
        return (out_dirs[(out_dirs.index(from_dir) + 1) % 2]
                if from_dir in out_dirs else None)
    
