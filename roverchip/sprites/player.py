import pygame

import sprite


class Player(sprite.Sprite):   
    def __init__(self, level, pos, facing=0):
        sprite.Sprite.__init__(self, level, pos, facing)
        
        self.tile = 0, 2
        self.facing = 2
        self.layer = 1
        self.speed = 250
        self.rotate = True
        self.is_destructible = True
        
        self.move_key = None
        self.following = pygame.sprite.Group()
        self.pushing = pygame.sprite.Group()
        self.inv = pygame.sprite.Group()
        
        
    def move_key_down(self, move_key):
        """When a movement key is pressed, start moving the player
        if he isn't already."""
        if self.move_key is None:
            self.move_key = move_key
        
        
    def move_key_up(self, move_key):
        """When a movement key is released, stop moving the player
        if he is moving in that direction."""
        if move_key == self.move_key:
            self.move_key = None
        
        
    def start_turn(self):
        """Check if movement is possible in the given direction, and if so,
        initiate movement."""
        if self.move_key is not None and not self.to_move:
            self.facing = self.move_key
            self.move_dir = self.move_key
            nextcell = self.level.get_neighbour(self.pos, self.move_dir)
            
            # check if the cell to move to exists and can be moved into
            if nextcell and self.level.player_can_enter(nextcell):
                
                # remove chipdoor if all chips have been collected
                chipdoor = self.level.get_sprites_in(nextcell, False, 'ChipDoor')
                if chipdoor and not self.level.get_sprites('Chip'):
                    chipdoor[0].kill()
                
                # remove door if carrying the matching key
                door = self.level.get_sprites_in(nextcell, False, 'Door')
                if door:
                    key = [key for key in self.get_carried_items('Key')
                           if key.colour == door[0].colour]
                    if key:
                        door[0].kill()
                        if key[0].colour != 0:
                            key[0].kill()
                
                # check if the cell contains a movable object and if there is room to push it
                movables = self.level.get_movables_in(nextcell)
                if movables:
                    nextcell2 = self.level.get_neighbour(nextcell, self.move_dir)
                    if (nextcell2 and self.level.object_can_enter(nextcell2)
                        and not self.level.get_solid_sprites_in(nextcell2, False)
                        and not self.level.get_enemies_in(nextcell2, False)
                        ):
                        self.pushing.add(movables)
                        self.start_move()
                        
                # check that the cell does not contain any immovable objects
                elif not any(sprite.get_type() != 'Rover'
                             for sprite in self.level.get_solid_sprites_in(nextcell, False)):
                    self.start_move()
                    
                    
    def start_move(self):
        """Start the player moving one square in the facing direction."""
        self.last_pos = self.pos
        self.to_move = 1
        
        # also move items in inventory
        for item in set(self.pushing.sprites() + self.inv.sprites()):
            item.speed = min(item.speed, self.speed)
            item.move_dir = self.move_dir
            item.to_move = 1
            
        # move rover
        for follower in self.following.sprites():
            move_dir = self.level.get_dir(follower.pos, self.pos)
            follower.facing = move_dir
            follower.move_dir = move_dir
            follower.speed = self.speed
            follower.to_move = 1
    
    
    def after_move(self):
        """Run checks for items in the new square, and clean up movement actions."""
        # trigger player enter hook
        self.level.get_cell(self.pos).player_inside()
        
        # pick up items
        for item in self.level.get_items_in(self.pos):
            if item.get_type() == 'Chip':
                item.kill()
                
            elif not self.inv.has(item):
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
                and all(self.following.has(rover) for rover in self.level.get_sprites('Rover'))
                and not self.level.get_sprites('Chip'))
        
        
    def get_carried_items(self, itype):
        """Return all items that the player is carrying."""
        return [item for item in self.inv if item.get_type() == itype]
            
            
    def check_collisions(self):
        """Kill the player if he is touching any enemies."""
        if pygame.sprite.spritecollideany(self, self.level.enemies):
            self.kill()
            
