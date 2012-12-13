from sprite import Sprite


class Enemy(Sprite):
    def __init__(self, level, pos, facing):
        Sprite.__init__(self, level, pos, facing)
        
        self.layer = 1
        self.speed = 250
        self.rotate = True
        self.is_solid = True
        self.is_enemy = True
        self.is_destructible = True


    def after_move(self):
        # trigger enemy enter hook
        self.level.get_cell(self.pos).enemy_inside()
