from sprite import Sprite


class Shooter(Sprite):
    def __init__(self, level, pos, facing):
        Sprite.__init__(self, level, pos, facing)
        
        self.tile = 2, 2
        self.rotate = True
        self.is_solid = True
        self.is_destructible = True
        
    
    def check_collisions(self):
        """Kill the player if he is fully in the shooter's sightline."""
        cell = self.pos
        while True:
            cell = self.level.get_neighbour(cell, self.facing)
            if not cell or not self.level.object_can_enter(cell) or self.level.get_solid_sprites_in(cell):
                break

            for sprite in self.level.get_sprites_in(cell, True, 'Player'):
                sprite.kill()
