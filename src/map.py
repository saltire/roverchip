import pygame

import crate
import door
import key
import laser
import levels
import mirror
import player
import robot
import rover
import shooter

class Map:
    
    def __init__(self, num):
        level = levels.Levels()
        mapdata, objects = level.levels[num]

        self.height = len(mapdata)
        self.width = len(mapdata[0])
        
        self.exit = objects['exit']
        
        # init map
        self.map = {}
        self.colours = {}
        for y in range(self.height):
            for x in range(self.width):
                self.map[x, y] = int(mapdata[y][x])
                self.colours[x, y] = level.colours[int(mapdata[y][x])]

        # init sprites and groups
        self.sprites = pygame.sprite.LayeredUpdates()
        
        self.sprites.add(rover.Rover(self, objects['rover']))
        self.sprites.add(player.Player(self, objects['player']))
        for pos, facing, follow in objects['robots']:
            self.sprites.add(robot.Robot(self, pos, facing, follow))
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
    
    
    def can_player_enter(self, cell):
        return cell in self.map and (
            self.map[cell] in [0, 8]
            or self.map[cell] == 3 and self.get_objects_in(cell, 0, 'SunkenCrate')
            )
    
    
    def can_robot_enter(self, cell):
        return cell in self.map and self.map[cell] in [0]
    
    
    def can_object_enter(self, cell):
        return cell in self.map and self.map[cell] in [0, 2, 3, 4, 5, 6, 7, 8]
            
            
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


    def is_water(self, cell):
        return self.map[cell] in [3, 4, 5, 6, 7]


    def get_water_dir(self, cell):
        if self.map[cell] in [4, 5, 6, 7]:
            return self.map[cell] - 4
