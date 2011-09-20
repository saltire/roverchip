import pygame

import crate
import door
import key
import laser
import mirror
import player
import robot
import rover
import shooter

class Map:
    
    def __init__(self):
        mapdata = ['00111001',
                   '00000101',
                   '10000000',
                   '11000000',
                   '00000000',
                   '00000000']
        self.objects = {
            'player': (7, 5),
            'rover': (5, 0),
            'robots': [((0, 0), 0)],
            'shooters': [((4, 1), 2)],
            'crates': [(5, 3)],
            'lasers': [((0, 5), 1)],
            'mirrors': [((5, 5), 0)],
            'keys': [(1, 4)],
            'doors': [((6, 1), 2)]
        }

        self.height = len(mapdata)
        self.width = len(mapdata[0])
                      
        # init map
        self.map = {}
        for y in range(self.height):
            for x in range(self.width):
                self.map[x, y] = int(mapdata[y][x])

        # init sprites and groups
        self.sprites = pygame.sprite.LayeredUpdates()
        
        self.sprites.add(rover.Rover(self, self.objects['rover']))
        self.sprites.add(player.Player(self, self.objects['player']))
        for pos, facing in self.objects['robots']:
            self.sprites.add(robot.Robot(self, pos, facing))
        for pos, facing in self.objects['shooters']:
            self.sprites.add(shooter.Shooter(self, pos, facing))
        for pos in self.objects['crates']:
            self.sprites.add(crate.Crate(self, pos))
        for pos, facing in self.objects['lasers']:
            self.sprites.add(laser.Laser(self, pos, facing), layer='lasers')
        for pos, facing in self.objects['mirrors']:
            self.sprites.add(mirror.Mirror(self, pos, facing))
        for pos in self.objects['keys']:
            self.sprites.add(key.Key(self, pos))
        for pos, facing in self.objects['doors']:
            self.sprites.add(door.Door(self, pos, facing))
            
        self.solid_objects = pygame.sprite.Group([sprite for sprite in self.sprites if sprite.is_solid])
        self.movables = pygame.sprite.Group([sprite for sprite in self.sprites if sprite.is_movable])
        self.items = pygame.sprite.Group([sprite for sprite in self.sprites if sprite.is_item])
        self.enemies = pygame.sprite.Group([sprite for sprite in self.sprites if sprite.is_enemy])
        self.beams = pygame.sprite.Group()
        
        
    def get_blocktype(self, pos):
        return self.map[(pos)] if pos in self.map else None

    
    def get_neighbour(self, (x, y), *dirs):
        neighbours = [(x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)]
        dirs = dirs or [0, 1, 2, 3]
        cells = [neighbours[dir] for dir in dirs if neighbours[dir] in self.map]
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
    
    
    def is_open(self, cell):
        return True if (
            cell in self.map
            and self.map[cell] == 0
            ) else False
            
            
    def get_objects(self, *types):
        return [sprite for sprite in self.sprites if sprite.get_type() in types or not types]
            
            
    def get_objects_in(self, cell, touching=0, *types):
        return [sprite for sprite in self.sprites if (
    
                    # test if object is touching cell, or entirely in it, depending on touching flag
                    ((cell in sprite.cells_in()) if touching else (cell == sprite.pos))
                    
                    # test if sprite is included in types array, if given
                    and (sprite.get_type() in types or not types)
                    )]
    
    
    def get_solid_objects_in(self, cell, touching=0):
        return [sprite for sprite in self.get_objects_in(cell, touching) if sprite.is_solid]
    
    
    def get_movables_in(self, cell, touching=0):
        return [sprite for sprite in self.get_objects_in(cell, touching) if sprite.is_movable]
    
    
    def get_enemies_in(self, cell, touching=0):
        return [sprite for sprite in self.get_objects_in(cell, touching) if sprite.is_enemy]
    
    
    def get_items_in(self, cell, touching=0):
        return [sprite for sprite in self.get_objects_in(cell, touching) if sprite.is_item]
    
    
    def get_beams(self):
        return [beam.pos for beam in self.beams]

