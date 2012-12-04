import pygame

import sprite


class Player(sprite.Sprite):   
    def __init__(self, level, pos, facing=0):
        sprite.Sprite.__init__(self, level, pos, facing)
        self.colour = 0, 0, 255
        self.layer = 1
        self.speed = 4
        self.is_destructible = True
        
        self.following = pygame.sprite.Group()
        self.pushing = pygame.sprite.Group()
        self.inv = pygame.sprite.Group()
        

    def try_move(self, movedir):
        """Check if movement is possible in the given direction, and if so,
        initiate movement."""
        if not self.to_move:
            self.facing = movedir
            nextcell = self.level.get_neighbour(self.pos, movedir)
            # check if the square to move to exists and can be moved into
            if nextcell and self.level.player_can_enter(nextcell):
                try:
                    door = next(self.level.get_sprites_in(nextcell, False, 'Door'))
                    key = next(self.get_carried_items('Key'))
                    door.kill()
                    key.kill()
                except StopIteration:
                    pass
                
                # check if the square contains a movable object and if there is room to push it
                movables = self.level.get_movables_in(nextcell)
                if movables:
                    nextcell2 = self.level.get_neighbour(nextcell, movedir)
                    if (nextcell2 and self.level.object_can_enter(nextcell2)
                        and not self.level.get_solid_sprites_in(nextcell2, False)
                        and not self.level.get_enemies_in(nextcell2, False)
                        ):
                        self.pushing.add(movables)
                        self.start_move()
                        
                # check that the square does not contain any immovable objects
                elif not self.level.get_solid_sprites_in(nextcell):
                    self.start_move()
                    
                    
    def start_move(self):
        """Start the player moving one square in the facing direction."""
        self.last_pos = self.pos
        self.to_move = 1
        
        # also move items in inventory
        for item in set(self.pushing.sprites() + self.inv.sprites()):
            item.speed = max(item.speed, self.speed)
            item.facing = self.facing
            item.to_move = 1
            
        # move rover
        for follower in self.following.sprites():
            follower.speed = self.speed
            follower.facing = self.level.get_dir(follower.pos, self.pos)
            follower.to_move = 1
    
    
    def after_move(self):
        """Run checks for items in the new square, and clean up movement actions."""
        # pick up items
        for item in self.level.get_items_in(self.pos):
            if not self.inv.has(item):
                self.inv.add(item)
            
        # stop pushing objects
        self.pushing.empty()
        
        # check for rover
        for direction in range(4):
            rover = self.level.get_sprites_in(self.level.get_neighbour(self.pos, direction), False, 'Rover')
            if rover:
                self.following.add(rover)
                
                    
    def done_level(self):
        """Check to see if the level has been completed."""
        return (len(self.cells_in()) == 1
                and self.level.get_cell(self.pos).get_type() == 'Exit'
                and any(follower.get_type() == 'Rover' for follower in self.following))
        
        
    def get_carried_items(self, itype):
        """Return all items that the player is carrying."""
        return (item for item in self.inv if item.get_type() == itype)
            
            
    def check_collisions(self):
        """Kill the player if he is touching any enemies or is in the path
        of any shooters."""
        if self.pos in (pos for shooter in self.level.get_sprites('Shooter') for pos in shooter.path):
            self.kill()

        if pygame.sprite.spritecollideany(self, self.level.enemies):
            self.kill()
            
