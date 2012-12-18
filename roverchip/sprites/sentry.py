from enemy import Enemy


class Sentry(Enemy):
    def __init__(self, level, pos, facing=0):
        Enemy.__init__(self, level, pos, facing)
        
        self.tile = 3, 3
        
    
    def after_move(self):
        Enemy.after_move()

        nextcell = self.level.get_neighbour(self.pos, self.move_dir)
        if self.level.object_can_enter(nextcell) and not self.level.get_solid_sprites_in(nextcell):
            self.to_move = 1
