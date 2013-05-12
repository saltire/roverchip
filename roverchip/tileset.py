import pygame


class Tileset:
    def __init__(self, tilepath, tilesize):
        self.img = pygame.image.load(tilepath).convert_alpha()
        
        tw, th = tilesize
        self.dims = self.img.get_width() / tw, self.img.get_height() / th
        
    
    def init_tileset(self, cellsize):
        """Resize the tileset to fit the cell size."""
        size = [d * cellsize for d in self.dims]
        self.tileset = pygame.transform.scale(self.img, size)
        self.cellsize = cellsize
        
        
    def get_tile(self, (x, y), rotate=0):
        """Return a single tile surface based on coordinates and cell size."""
        tileimg = self.tileset.subsurface((x * self.cellsize, y * self.cellsize,
                                           self.cellsize, self.cellsize))
        if rotate != 0:
            tileimg = pygame.transform.rotate(tileimg, rotate * -90)
            
        return tileimg
