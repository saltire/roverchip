import math

from robot import Robot


class Tank(Robot):
    def __init__(self, level, pos, facing=0, follow=0):
        Robot.__init__(self, level, pos, facing, follow)
        
        self.tile = 4, 2
        self.speed = 500
        
    
    def check_collisions(self):
        """Kill the player if he is fully in the shooter's sightline."""
        x, y = self.pos
        # start from the cell the tank is rolling toward
        cell = (math.ceil(x) if self.facing == 1 else math.floor(x),
                math.ceil(y) if self.facing == 2 else math.floor(y))
        while True:
            cell = self.level.get_neighbour(cell, self.facing)
            if not cell or not self.level.object_can_enter(cell) or self.level.get_solid_sprites_in(cell):
                break

            for sprite in self.level.get_sprites_in(cell, True, 'Player'):
                sprite.kill()
