import sprite


class Shooter(sprite.Sprite):
    def __init__(self, level, pos, facing):
        sprite.Sprite.__init__(self, level, pos, facing)
        self.colour = 255, 128, 0
        
        self.is_solid = True
        self.is_destructible = True
        
    
    def start_turn(self):
        """Calculate the shooter's sight line."""
        self.path = []
        cell = self.pos
        while True:
            cell = self.level.get_neighbour(cell, self.facing)
            if not cell or not self.level.object_can_enter(cell) or self.level.get_solid_sprites_in(cell):
                break
            self.path.append(cell)
            
            
    def check_collisions(self):
        """Kill the player or Rover if they are fully in the shooter's sightline."""
        for pos in self.path:
            for sprite in self.level.get_sprites_in(pos, True, 'Player', 'Rover'):
                sprite.kill()
