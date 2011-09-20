import sys

import pygame

import sprite

class Player(sprite.Sprite):
    
    def __init__(self, map, pos, facing=0):
        sprite.Sprite.__init__(self, map, pos, facing)
        self.colour = (0, 0, 255)
        self.speed = 4
        
        self.following = pygame.sprite.Group()
        self.pushing = pygame.sprite.Group()
        self.inv = pygame.sprite.Group()
        

    def try_move(self, dir):
        if not self.to_move:
            self.dir = dir
            next = self.map.get_neighbour(self.pos, dir)
            # check if the sqaure to move to exists and can be moved into
            if next and self.map.is_open(next):
                door = self.map.get_objects_in(next, 0, 'Door')
                key = self.in_inventory('Key')
                if door and key:
                    door[0].kill()
                    key[0].kill()
                
                # check if the square contains a movable object and if there is room to push it
                movables = self.map.get_movables_in(next)
                next2 = self.map.get_neighbour(next, dir)
                if movables and self.map.is_open(next2) and not self.map.get_solid_objects_in(next2, 1) and not self.map.get_enemies_in(next2, 1):
                    self.pushing.add(movables)
                    self.start_move()
                        
                # check that the square does not contain any immovable objects
                elif not self.map.get_solid_objects_in(next):
                    self.start_move()
                    
                    
    def start_move(self):
        self.last_pos = self.pos
        self.to_move = 1
        
        # also move items in inventory
        for item in set(self.pushing.sprites() + self.inv.sprites()):
            item.speed = self.speed
            item.dir = self.dir
            item.to_move = 1
            
        # move rover
        for follower in self.following.sprites():
            follower.speed = self.speed
            follower.dir = self.map.get_dir(follower.pos, self.pos)
            follower.to_move = 1
    
    
    def after_move(self):
        # pick up items
        for item in self.map.get_items_in(self.pos):
            if not self.inv.has(item):
                self.inv.add(item)
            
        # stop pushing objects
        self.pushing.empty()
        
        # check for rover
        for dir in range(4):
            rover = self.map.get_objects_in(self.map.get_neighbour(self.pos, dir), 0, 'Rover')
            if rover:
                self.following.add(rover)
                
        # check win condition
        if self.pos == self.map.exit:
            for follower in self.following:
                if follower.get_type() == 'Rover':
                    sys.exit('Yay!')
        
        
    def in_inventory(self, type):
        return [item for item in self.inv if item.get_type() == type]
            
            
    def check_collisions(self):
        if self.pos in [pos for shooter in self.map.get_objects('Shooter') for pos in shooter.path]:
            self.kill()

        if pygame.sprite.spritecollideany(self, self.map.beams) or pygame.sprite.spritecollideany(self, self.map.enemies):
            self.kill()
            
        if not self.alive():
            sys.exit()
            
