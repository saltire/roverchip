import sprite

class Robot(sprite.Sprite):

    def __init__(self, map, pos, dir=0, follow=0):
        sprite.Sprite.__init__(self, map, pos, dir)
        self.colour = (255, 0, 0)
        self.speed = 1.5
        self.is_enemy = 1
        self.is_destructible = 1
        
        self.follow = follow # 0 = left wall, 1 = right wall
        
    
    def start_turn(self):
        if not self.to_move:
            for t in range(4):
                dir = (self.dir + ((1 - t) if self.follow else (t - 1))) % 4
                next = self.map.get_neighbour(self.pos, dir)
                if (self.map.can_robot_enter(next)
                    and not self.map.get_solid_objects_in(next)
                    and next not in [beam.pos for beam in self.map.beams]
                    ):
                    self.dir = dir
                    self.to_move = 1
                    break

