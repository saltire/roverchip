import sprite

class SunkenCrate(sprite.Sprite):
    
    def __init__(self, map, pos):
        sprite.Sprite.__init__(self, map, pos)
        self.colour = (128, 128, 128, 128)
        self.speed = 2
        
        
    def after_move(self):
        dir = self.map.get_water_dir(self.pos)
        if dir is not None and not self.map.get_sprites_in(self.map.get_neighbour(self.pos, dir), 0, 'SunkenCrate'):
            self.dir = dir
            self.to_move = 1