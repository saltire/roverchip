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
        mapdata = ['0000000000000000000000',
                   '0111111111111111110000',
                   '0122210000000000010000',
                   '0122210000000000000000',
                   '0122000000000000010000',
                   '0100010000000000010000',
                   '0102210000000000010000',
                   '0111111111111111112000',
                   '0000000000000000000000']
        
        objects = {
            'exit': (0, 8),
            'player': (0, 8),
            'rover': (2, 6),
            'robots': [],
            'shooters': [((9, 6), 0), ((10, 6), 0), ((11, 6), 0), ((12, 6), 0), ((13, 6), 0), ((14, 6), 0), ((15, 6), 0), ((16, 4), 3), ((16, 5), 3), ((21, 6), 3)],
            'crates': [],
            'lasers': [((7, 6), 0)],
            'mirrors': [((7, 3), 2), ((20, 1), 3), ((19, 7), 1)],
            'keys': [(18, 6)],
            'doors': [((5, 4), 1)]
        }

        self.height = len(mapdata)
        self.width = len(mapdata[0])
        
        self.exit = objects['exit']
        
        colours = [
            (255, 255, 255),
            (0, 0, 0),
            (64, 64, 64)
            ]
        
        # init map
        self.map = {}
        self.colours = {}
        for y in range(self.height):
            for x in range(self.width):
                self.map[x, y] = int(mapdata[y][x])
                self.colours[x, y] = colours[int(mapdata[y][x])]

        # init sprites and groups
        self.sprites = pygame.sprite.LayeredUpdates()
        
        self.sprites.add(rover.Rover(self, objects['rover']))
        self.sprites.add(player.Player(self, objects['player']))
        for pos, facing in objects['robots']:
            self.sprites.add(robot.Robot(self, pos, facing))
        for pos, facing in objects['shooters']:
            self.sprites.add(shooter.Shooter(self, pos, facing))
        for pos in objects['crates']:
            self.sprites.add(crate.Crate(self, pos))
        for pos, facing in objects['lasers']:
            self.sprites.add(laser.Laser(self, pos, facing), layer='lasers')
        for pos, facing in objects['mirrors']:
            self.sprites.add(mirror.Mirror(self, pos, facing))
        for pos in objects['keys']:
            self.sprites.add(key.Key(self, pos))
        for pos, facing in objects['doors']:
            self.sprites.add(door.Door(self, pos, facing))
            
        self.solid_objects = pygame.sprite.Group([sprite for sprite in self.sprites if sprite.is_solid])
        self.movables = pygame.sprite.Group([sprite for sprite in self.sprites if sprite.is_movable])
        self.items = pygame.sprite.Group([sprite for sprite in self.sprites if sprite.is_item])
        self.enemies = pygame.sprite.Group([sprite for sprite in self.sprites if sprite.is_enemy])
        self.beams = pygame.sprite.Group()
        
        
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

