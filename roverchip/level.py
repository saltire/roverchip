import pygame

import sprites


class Level:
    cells = [('floor',    (255, 255, 255)),    # 0 - floor
             ('wall',     (0, 0, 0)),          # 1 - wall
             ('fire',     (64, 64, 64)),       # 2 - fire
             ('water',    (0, 128, 255)),      # 3 - water
             ('water n',  (0, 128, 255)),      # 4 - water n
             ('water e',  (0, 128, 255)),      # 5 - water e
             ('water s',  (0, 128, 255)),      # 6 - water s
             ('water w',  (0, 128, 255)),      # 7 - water w
             ('grate',    (192, 192, 192)),    # 8 - grate
             ('exit',     (255, 255, 192)),    # 9 - exit
             ]

    
    def __init__(self, mapdata, spritedata):
        # init map
        self.map = mapdata
        self.width = len(set(x for x, y in self.map))
        self.height = len(set(y for x, y in self.map))
                
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
    
    
    def get_cell_type(self, (x, y)):
        return self.cells[self.map[x, y]][0]
    
    
    def get_cell_colour(self, (x, y)):
        return self.cells[self.map[x, y]][1]
        
        
    def get_neighbour(self, (x, y), *ndirs):
        neighbours = [(x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)]
        ndirs = ndirs or [0, 1, 2, 3]
        cells = [neighbours[ndir] for ndir in ndirs if neighbours[ndir] in self.map]
        return cells if len(cells) > 1 else cells[0] if len(cells) == 1 else None
    
    
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
            
            
    def get_sprites_in(self, cell, touching=0, *types):
        return [sprite for sprite in self.sprites if (
    
                    # test if object is touching cell, or entirely in it, depending on touching flag
                    ((cell in sprite.cells_in()) if touching else (cell == sprite.pos))
                    
                    # test if sprite is included in types array, if given
                    and (sprite.get_type() in types or not types)
                    )]
    
    
    def get_solid_sprites_in(self, cell, touching=0):
        return [sprite for sprite in self.get_sprites_in(cell, touching) if sprite.is_solid]
    
    
    def get_movables_in(self, cell, touching=0):
        return [sprite for sprite in self.get_sprites_in(cell, touching) if sprite.is_movable]
    
    
    def get_enemies_in(self, cell, touching=0):
        return [sprite for sprite in self.get_sprites_in(cell, touching) if sprite.is_enemy]
    
    
    def get_items_in(self, cell, touching=0):
        return [sprite for sprite in self.get_sprites_in(cell, touching) if sprite.is_item]
    
    
    # boolean tests
    
    
    def can_player_enter(self, cell):
        return cell in self.map and (
            self.get_cell_type(cell) in ['floor', 'grate', 'exit']
            or self.is_water(cell) and self.get_sprites_in(cell, 0, 'SunkenCrate')
            )
    
    
    def can_robot_enter(self, cell):
        return cell in self.map and (
            self.map[cell] == 0
            or self.is_water(cell) and self.get_sprites_in(cell, 0, 'SunkenCrate')
            )
    
    
    def can_object_enter(self, cell):
        return cell in self.map and self.get_cell_type(cell) != 'wall'
    
    
    def is_type(self, cell, ctype):
        return cell in self.map and self.get_cell_type(cell) == ctype
            
            
    def is_water(self, cell):
        return cell in self.map and self.get_cell_type(cell)[:5] == 'water'


    def get_water_dir(self, cell):
        if cell in self.map and self.get_cell_type(cell)[:6] == 'water ':
            return self.map[cell] - 4
