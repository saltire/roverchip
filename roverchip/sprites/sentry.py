import sprite


class Sentry(sprite.Sprite):
    def __init__(self, level, pos, facing=0):
        sprite.Sprite.__init__(self, level, pos, facing)
        
        self.tile = 3, 2
        self.layer = 1
        self.speed = 250
        self.rotate = True
        self.is_solid = True
        self.is_enemy = True
        self.is_destructible = True
        
    
    def after_move(self):
        # trigger enemy enter hook
        self.level.get_cell(self.pos).enemy_inside()

        nextcell = self.level.get_neighbour(self.pos, self.move_dir)
        if self.level.object_can_enter(nextcell) and not self.level.get_solid_sprites_in(nextcell):
            self.to_move = 1
