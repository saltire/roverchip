import sprite

class Shooter(sprite.Sprite):
    
    def __init__(self, level, pos, facing):
        sprite.Sprite.__init__(self, level, pos, facing)
        self.colour = (255, 128, 0)
        
        self.is_solid = 1
        self.is_destructible = 1
        
    
    def start_turn(self):
        self.path = []
        cell = self.pos
        while 1:
            cell = self.level.get_neighbour(cell, self.facing)
            if not cell or not self.level.can_object_enter(cell) or self.level.get_solid_sprites_in(cell):
                break
            self.path.append(cell)

