import mob

class Crate(mob.Mob):
    
    def __init__(self, map, pos):
        mob.Mob.__init__(self, map, pos)
        self.colour = (128, 128, 128)
        self.is_pushable = 1
        self.is_solid = 1
        