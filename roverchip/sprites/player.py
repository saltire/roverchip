import pygame

import sprite

class Player(sprite.Sprite):
    
    def __init__(self, level, pos, facing=0):
        sprite.Sprite.__init__(self, level, pos, facing)
        self.colour = (0, 0, 255)
        self.layer = 1
        self.speed = 4
        self.is_destructible = 1
        
        self.following = pygame.sprite.Group()
        self.pushing = pygame.sprite.Group()
        self.inv = pygame.sprite.Group()
        

    def try_move(self, movedir):
        if not self.to_move:
            self.facing = movedir
            nextcell = self.level.get_neighbour(self.pos, movedir)
            # check if the sqaure to move to exists and can be moved into
            if nextcell and self.level.can_player_enter(nextcell):
                door = self.level.get_sprites_in(nextcell, 0, 'Door')
                key = self.in_inventory('Key')
                if door and key:
                    door[0].kill()
                    key[0].kill()
                
                # check if the square contains a movable object and if there is room to push it
                movables = self.level.get_movables_in(nextcell)
                nextcell2 = self.level.get_neighbour(nextcell, movedir)
                if movables and self.level.can_object_enter(nextcell2) and not self.level.get_solid_sprites_in(nextcell2, 1) and not self.level.get_enemies_in(nextcell2, 1):
                    self.pushing.add(movables)
                    self.start_move()
                        
                # check that the square does not contain any immovable objects
                elif not self.level.get_solid_sprites_in(nextcell):
                    self.start_move()
                    
                    
    def start_move(self):
        self.last_pos = self.pos
        self.to_move = 1
        
        # also move items in inventory
        for item in set(self.pushing.sprites() + self.inv.sprites()):
            item.speed = max(item.speed, self.speed)
            item.dir = self.dir
            item.to_move = 1
            
        # move rover
        for follower in self.following.sprites():
            follower.speed = self.speed
            follower.dir = self.level.get_dir(follower.pos, self.pos)
            follower.to_move = 1
    
    
    def after_move(self):
        # pick up items
        for item in self.level.get_items_in(self.pos):
            if not self.inv.has(item):
                self.inv.add(item)
            
        # stop pushing objects
        self.pushing.empty()
        
        # check for rover
        for direction in range(4):
            rover = self.level.get_sprites_in(self.level.get_neighbour(self.pos, direction), 0, 'Rover')
            if rover:
                self.following.add(rover)
                
                    
    def done_level(self):
        return True if (self.level.is_type(self.pos, 'exit') and
                        any(follower.get_type() == 'Rover' for follower in self.following)
                        ) else False
        
        
    def in_inventory(self, itype):
        return [item for item in self.inv if item.get_type() == itype]
            
            
    def check_collisions(self):
        if self.pos in [pos for shooter in self.level.get_sprites('Shooter') for pos in shooter.path]:
            self.kill()

        if pygame.sprite.spritecollideany(self, self.level.enemies):
            self.kill()
            
