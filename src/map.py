import pygame

import crate
import laser
import mirror
import player
import robot

class Map:
    
    def __init__(self):
        mapdata = ['00111001',
                   '00000000',
                   '10000000',
                   '11000000',
                   '00000000',
                   '00000000']
        self.objects = {
            'player': (7, 5),
            'robots': [],
            'crates': [(6, 3)],
            'lasers': [((3, 5), 0)],
            'mirrors': [((3, 1), 2), ((5, 1), 3)]
        }

        self.height = len(mapdata)
        self.width = len(mapdata[0])
                      
        # init map
        self.map = {}
        for y in range(self.height):
            for x in range(self.width):
                self.map[x, y] = int(mapdata[y][x])

        # init sprites and groups
        self.player = pygame.sprite.RenderUpdates()
        self.enemies = pygame.sprite.RenderUpdates()
        self.crates = pygame.sprite.RenderUpdates()
        self.lasers = pygame.sprite.RenderUpdates()
        self.mirrors = pygame.sprite.RenderUpdates()
        self.mobs = pygame.sprite.RenderUpdates()
        self.beams = pygame.sprite.RenderUpdates()
        
        self.player.add(player.Player(self, self.objects['player']))
        for pos in self.objects['robots']:
            self.enemies.add(robot.Robot(self, pos))
        for pos in self.objects['crates']:
            self.crates.add(crate.Crate(self, pos))
        for pos, dir in self.objects['lasers']:
            self.lasers.add(laser.Laser(self, pos, dir))
        for pos, dir in self.objects['mirrors']:
            self.mirrors.add(mirror.Mirror(self, pos, dir))
        self.mobs.add(self.player, self.enemies, self.crates, self.lasers, self.mirrors)
                
                
    def get_blocktype(self, pos):
        return self.map[(pos)] if pos in self.map else None

    
    def get_neighbour(self, (x, y), dir):
        neighbours = [(x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)]
        return neighbours[dir] if neighbours[dir] in self.map else None
    
    
    def is_empty(self, cell):
        return True if (
            cell in self.map
            and self.map[cell] == 0
            ) else False

    
    def get_mobs_in(self, cell, *types):
        return [mob for mob in self.mobs if cell == mob.pos and (mob.get_type() in types or not types)]
    
    
    def is_mob_type_in(self, cell, *types):
        types_in = [mob.get_type() for mob in self.get_mobs_in(cell)]
        return any(type in list(types) for type in types_in)


    def get_mobs_touching(self, cell, *types):
        return [mob for mob in self.mobs if cell in mob.cells_in() and (mob.get_type() in types or not types)]
    
    
    def is_mob_type_touching(self, cell, *types):
        types_touching = [mob.get_type() for mob in self.get_mobs_touching(cell)]
        return any(type in list(types) for type in types_touching)
