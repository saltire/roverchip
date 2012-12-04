import pygame

import cells
import sprites


class Level:
    def __init__(self, mapdata, spritedata):
        # init map
        self.cells = {}
        for pos, celldata in mapdata.items():
            self.cells[pos] = getattr(cells, celldata[0])(self, *celldata[1:])
        self.width = len(set(x for x, y in self.cells))
        self.height = len(set(y for x, y in self.cells))
                
        # init sprites and groups
        self.sprites = pygame.sprite.LayeredUpdates()
        
        self.player = sprites.Player(self, spritedata['player'][0])
        self.rover = sprites.Rover(self, spritedata['rover'][0])
        self.sprites.add(self.player, layer=1)
        self.sprites.add(self.rover, layer=1)
        
        for stype in ('ball', 'crate', 'door', 'key', 'laser', 'robot', 'mirror', 'shooter'):
            for attrs in spritedata.get(stype, []):
                sprite = getattr(sprites, stype.capitalize())(self, attrs[:2], *attrs[2:])
                self.sprites.add(sprite, layer=sprite.layer)
                
        # groups used for collisions
        self.destructibles = pygame.sprite.Group([sprite for sprite in self.sprites if sprite.is_destructible])
        self.enemies = pygame.sprite.Group([sprite for sprite in self.sprites if sprite.is_enemy])
        self.beams = pygame.sprite.Group()
        
        
    # cell data
    
    
    def get_cell(self, pos):
        return self.cells.get(pos)
    
    
    def player_can_enter(self, pos):
        return pos in self.cells and (
            self.cells[pos].player_can_enter 
            or (self.cells[pos].get_type() == 'Water'
                and self.get_sprites_in(pos, False, 'SunkenCrate')))
    
    
    def robot_can_enter(self, pos):
        return pos in self.cells and (
            self.cells[pos].robot_can_enter 
            or (self.cells[pos].get_type() == 'Water'
                and self.get_sprites_in(pos, False, 'SunkenCrate')))
    
    
    def object_can_enter(self, pos):
        return pos in self.cells and self.cells[pos].object_can_enter
    
    
    def get_neighbour(self, (x, y), ndir):
        neighbours = (x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)
        return neighbours[ndir] if neighbours[ndir] in self.cells else None
    
    
    def get_dir(self, (x1, y1), (x2, y2)):
        if (x1 != x1 and y1 != y2) or (x1 == x2 and y1 == y2):
            return False
        if y2 < y1:
            return 0
        if x2 > x1:
            return 1
        if y2 > y1:
            return 2
        if x2 < x1:
            return 3
        
        
    # sprite data
    
    
    def get_sprites(self, *types):
        return [sprite for sprite in self.sprites if sprite.get_type() in types or not types]
            
            
    def get_sprites_in(self, pos, inside=True, *types):
        return [sprite for sprite in self.sprites if (
                # test if object is entirely in cell, or just touching it, depending on inside flag
                (pos == sprite.pos if inside else pos in sprite.cells_in())
                # test if sprite is included in types array, if given
                and (sprite.get_type() in types or not types)
                )]
    
    
    def get_solid_sprites_in(self, pos, inside=True):
        return [sprite for sprite in self.get_sprites_in(pos, inside) if sprite.is_solid]
    
    
    def get_movables_in(self, pos, inside=True):
        return [sprite for sprite in self.get_sprites_in(pos, inside) if sprite.is_movable]
    
    
    def get_enemies_in(self, pos, inside=True):
        return [sprite for sprite in self.get_sprites_in(pos, inside) if sprite.is_enemy]
    
    
    def get_items_in(self, pos, inside=True):
        return [sprite for sprite in self.get_sprites_in(pos, inside) if sprite.is_item]
    
    
