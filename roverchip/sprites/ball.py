import sprite

class Ball(sprite.Sprite):
    
    def __init__(self, level, pos):
        sprite.Sprite.__init__(self, level, pos)
        self.colour = (255, 128, 128)
        self.speed = 5
        self.is_movable = 1
        self.is_solid = 1
        
    
    def after_move(self):
        next = self.level.get_neighbour(self.pos, self.dir)

        if self.level.is_water(self.pos) and not self.level.get_sprites_in(self.pos, 0, 'SunkenCrate'):
            self.kill()
        
        elif self.level.can_object_enter(next) and not self.level.get_solid_sprites_in(next):
            self.to_move = 1
            