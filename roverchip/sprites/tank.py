import math

import sprite


class Tank(sprite.Sprite):
    def __init__(self, level, pos, facing=0, follow=0):
        sprite.Sprite.__init__(self, level, pos, facing)
        self.colour = 128, 0, 128
        self.speed = 1.5
        self.is_solid = True
        self.is_enemy = True
        self.is_destructible = True
        
        self.follow = follow # 0 = left wall, 1 = right wall
        
    
    def start_turn(self):
        if not self.to_move:
            for t in range(4):
                movedir = (self.facing + ((1 - t) if self.follow else (t - 1))) % 4
                nextcell = self.level.get_neighbour(self.pos, movedir)
                if (self.level.robot_can_enter(nextcell)
                    and not self.level.get_solid_sprites_in(nextcell)
                    and nextcell not in (beam.pos for beam in self.level.beams)
                    ):
                    self.facing = movedir
                    self.to_move = 1
                    break


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