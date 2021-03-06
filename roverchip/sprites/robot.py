from enemy import Enemy


class Robot(Enemy):
    def __init__(self, level, pos, facing=0, follow=0):
        Enemy.__init__(self, level, pos, facing)
        
        self.tile = 3, 2
        
        self.follow = follow # 0 = left wall, 1 = right wall
        
    
    def start_turn(self):
        # decide movement direction and start movement
        if not self.to_move:
            for t in range(4):
                # starting from side set in self.follow,
                # try each direction until it finds a cell it can enter
                move_dir = (self.facing + ((1 - t) if self.follow else (t - 1))) % 4
                nextcell = self.level.get_neighbour(self.pos, move_dir)
                if (self.level.robot_can_enter(nextcell)
                    and not self.level.get_solid_sprites_in(nextcell)
                    and nextcell not in (beam.pos for beam in self.level.beams)
                    ):
                    self.facing = move_dir
                    self.move_dir = move_dir
                    self.to_move = 1
                    break
