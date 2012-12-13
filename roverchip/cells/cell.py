import pygame


class Cell:
    def __init__(self, level, pos):
        self.level = level
        self.pos = pos
        
        self.tile = 0, 0                # tile coords in the tileset
        self.rotate = 0                 # rotation of the tile
        self.player_can_enter = True    # player can enter this cell
        self.robot_can_enter = True     # robots can enter this cell
        self.object_can_enter = True    # movable objects can enter this cell
        
    
    def get_type(self):
        """Return the type of the cell, i.e. the class name."""
        return self.__class__.__name__
    
    
    def draw(self, cellsize, tileset):
        """Draw the cell."""
        tx, ty = self.tile
        tileimg = tileset.subsurface((tx * cellsize, ty * cellsize, cellsize, cellsize))
        if self.rotate != 0:
            tileimg = pygame.transform.rotate(tileimg, self.rotate * -90)
        return tileimg
    

    def player_inside(self):
        """A hook that runs after the player fully enters the cell."""
        pass
    
    
    def enemy_inside(self):
        """A hook that runs after an enemy fully enters the cell."""
        pass


    def object_inside(self):
        """A hook that runs after an object fully enters the cell."""
        pass
