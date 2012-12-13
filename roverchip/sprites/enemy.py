from sprite import Sprite


class Enemy(Sprite):
    def __init__(self, level, pos, facing):
        Sprite.__init__(self, level, pos, facing)
        
        level.destructibles.add(self)
        level.enemies.add(self)
        level.solids.add(self)
        
        self.layer = 1
        self.speed = 250
        self.rotate = True


    def after_move(self):
        # trigger enemy enter hook
        self.level.get_cell(self.pos).enemy_inside()
