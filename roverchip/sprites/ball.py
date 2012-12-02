import sprite

class Ball(sprite.Sprite):
    
    def __init__(self, map, pos):
        sprite.Sprite.__init__(self, map, pos)
        self.colour = (255, 128, 128)
        self.speed = 5
        self.is_movable = 1
        self.is_solid = 1
        
    
    def after_move(self):
        next = self.map.get_neighbour(self.pos, self.dir)

        if self.map.is_water(self.pos) and not self.map.get_sprites_in(self.pos, 0, 'SunkenCrate'):
            self.kill()
        
        elif self.map.can_sprite_enter(next) and not self.map.get_solid_sprites_in(next):
            self.to_move = 1
            