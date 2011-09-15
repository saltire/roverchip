import mob

class Robot(mob.Mob):

    def __init__(self, map, pos, dir=0):
        mob.Mob.__init__(self, map, pos, dir)
        self.colour = (255, 0, 0)
        self.speed = 1.5
        
        self.is_solid = 1
        
    
    def start_move(self):
        if not self.to_move:
            for t in range(4):
                dir = (self.dir - 1 + t) % 4
                next = self.map.get_neighbour(self.pos, dir)
                if self.map.is_empty(next) and not [mob for mob in self.map.get_mobs_touching(next) if mob.is_solid]:
                    self.dir = dir
                    self.to_move = 1
                    break
                           