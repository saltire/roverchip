import pygame

from cells import celltypes
from sprites import spritetypes


class Level:
    def __init__(self, celldata, spritedata):
        """Initialize all the cells and sprites, and add them to groups."""
        self.redraw_cells = set()
        
        # init map cells
        self.cells = {}
        for pos, (ctype, cdata) in celldata.items():
            self.cells[pos] = celltypes[ctype](self, pos, *cdata)
        
        self.width = len(set(x for x, _ in self.cells))
        self.height = len(set(y for _, y in self.cells))
        
        # init sprites and groups
        self.sprites = pygame.sprite.LayeredUpdates()
        
        self.destructibles = pygame.sprite.Group()  # will be destroyed by laserbeams
        self.movables = pygame.sprite.Group()       # can be pushed by player
        self.enemies = pygame.sprite.Group()        # will kill player on entering his cell
        self.solids = pygame.sprite.Group()         # will stop things from entering its cell
        self.items = pygame.sprite.Group()          # can be picked up by player
        self.beams = pygame.sprite.Group()          # beams emitted by lasers
        
        for stype, pos, sdata in spritedata:
            sprite = spritetypes[stype](self, pos, *sdata)
            self.sprites.add(sprite, layer=sprite.layer)

            if stype == 'Player':
                self.player = sprite
                
        
    # cell data
    
    def get_cell(self, pos):
        """Return the cell at the given coords."""
        return self.cells.get(pos)
    
    
    def set_cell(self, pos, ctype, *opts):
        """Replace the cell at the given coords with a new one."""
        self.cells[pos] = celltypes[ctype](self, pos, *opts)
        self.redraw_cells.add(pos)
        
        
    def get_cells(self, *types):
        """Return all cells, optionally filtering by a cell type."""
        return [cell for cell in self.cells.values() if cell.get_type() in types or not types]
    
    
    def trigger_redraw(self, pos):
        self.redraw_cells.add(pos)
            
            
    def player_can_enter(self, pos):
        """Return true if the player can enter the given cell."""
        ctype = self.cells[pos].get_type()
        return pos in self.cells and (
            self.cells[pos].player_can_enter 
            or (ctype == 'Fire' and self.player.get_carried_items('Boots', 0))
            or (ctype == 'Water' and (self.get_sprites_in(pos, False, 'SunkenCrate')
                                      or self.player.get_carried_items('Boots', 1))))
    
    
    def robot_can_enter(self, pos):
        """Return true if a robot can enter the given cell."""
        return pos in self.cells and (
            self.cells[pos].robot_can_enter 
            or (self.cells[pos].get_type() == 'Water'
                and self.get_sprites_in(pos, False, 'SunkenCrate')))
    
    
    def object_can_enter(self, pos):
        """Return true if movable objects can enter the given cell."""
        return pos in self.cells and self.cells[pos].object_can_enter
    
    
    def get_neighbour(self, (x, y), ndir):
        """Return the cell in the given direction from the given cell.
        0 = north, 1 = east, 2 = south, 3 = west."""
        neighbours = (x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)
        return neighbours[ndir] if neighbours[ndir] in self.cells else None
    
    
    def get_dir(self, (x1, y1), (x2, y2)):
        """Return the direction the second cell is in, relative to the first."""
        if (x1 != x1 and y1 != y2) or (x1 == x2 and y1 == y2):
            return None
        return (y2 < y1, x2 > x1, y2 > y1, x2 < x1).index(True)
        
        
    # sprite data
    
    def get_sprites(self, *types):
        """Return all sprites, optionally filtering by a sprite type."""
        return [sprite for sprite in self.sprites if sprite.get_type() in types or not types]
            
            
    def get_sprites_in(self, pos, inside=True, *types):
        """Return all sprites at a given coordinate, optionally filtering by
        a type. If inside is true, return only the sprites that are entirely
        in that cell, rather than just touching it."""
        return [sprite for sprite in self.sprites
                if (pos == sprite.pos if inside else pos in sprite.cells_in())
                and (sprite.get_type() in types or not types)]
    
    
    def get_movables_in(self, pos, inside=True):
        """Return all movable object sprites in a cell."""
        return [sprite for sprite in self.get_sprites_in(pos, inside)
                if self.movables.has(sprite)]
    
    
    def get_enemies_in(self, pos, inside=True):
        """Return all enemy sprites in a cell."""
        return [sprite for sprite in self.get_sprites_in(pos, inside)
                if self.enemies.has(sprite)]
    
    
    def get_solid_sprites_in(self, pos, inside=True):
        """Return all solid sprites in a cell."""
        return [sprite for sprite in self.get_sprites_in(pos, inside)
                if self.solids.has(sprite)]
    
    
    def get_items_in(self, pos, inside=True):
        """Remove all item sprites in a cell."""
        return [sprite for sprite in self.get_sprites_in(pos, inside)
                if self.items.has(sprite)]
    
    
