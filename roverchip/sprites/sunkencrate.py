import sprite

class SunkenCrate(sprite.Sprite):
    
    def __init__(self, level, pos):
        sprite.Sprite.__init__(self, level, pos)
        self.colour = (128, 128, 128, 128)
        self.speed = 2
        
        
    def after_move(self):
        dir = self.level.get_water_dir(self.pos)
        if dir is not None and not self.level.get_sprites_in(self.level.get_neighbour(self.pos, dir), 0, 'SunkenCrate'):
            self.dir = dir
            self.to_move = 1