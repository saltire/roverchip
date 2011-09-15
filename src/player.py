import mob

class Player(mob.Mob):
    
    def __init__(self, map, pos, dir=0):
        mob.Mob.__init__(self, map, pos, dir)
        self.colour = (0, 0, 255)
        self.speed = 4
        

    def start_move(self, dir):
        if not self.to_move:
            self.dir = dir
            next = self.map.get_neighbour(self.pos, dir)
            if next:
                if self.map.is_empty(next):
                    pushables = [mob for mob in self.map.get_mobs_in(next) if mob.is_pushable]
                    if pushables:
                        next2 = self.map.get_neighbour(next, dir)
                        if self.map.is_empty(next2) and not [mob for mob in self.map.get_mobs_touching(next2) if mob.is_solid or mob.is_enemy]:
                            self.to_move = 1
                            pushables[0].speed = self.speed
                            pushables[0].dir = dir
                            pushables[0].to_move = 1
                        
                    elif not [mob for mob in self.map.get_mobs_in(next) if mob.is_solid and not mob.is_enemy]:
                        self.to_move = 1
    