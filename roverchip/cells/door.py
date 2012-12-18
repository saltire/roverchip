import pygame

from cell import Cell


class Door(Cell):
    def __init__(self, level, pos, facing, colour):
        Cell.__init__(self, level, pos)
        
        self.tile = 5, 2 + colour
        self.rotate = facing
        self.player_can_enter = False
        self.robot_can_enter = False
        self.object_can_enter = False
        
        self.floor_tile = 0, 0
        self.colour = colour


    def draw(self, cellsize, tileset):
        """Draw the ice tile, then draw the rotated corner on top of it."""
        tx, ty = self.floor_tile
        tileimg = tileset.subsurface((tx * cellsize, ty * cellsize, cellsize, cellsize)).copy()
        
        tx, ty = self.tile
        doorimg = tileset.subsurface((tx * cellsize, ty * cellsize, cellsize, cellsize))
        doorimg = pygame.transform.rotate(doorimg, self.rotate * -90)              
        tileimg.blit(doorimg, (0, 0))
        
        return tileimg
