import sunkencrate
import sprite

class Crate(sprite.Sprite):
    
    def __init__(self, map, pos):
        sprite.Sprite.__init__(self, map, pos)
        self.colour = (128, 128, 128)
        self.is_movable = 1
        self.is_solid = 1
        
        
    def after_move(self):
        if self.map.is_water(self.pos):
            self.kill()
            sunken = sunkencrate.SunkenCrate(self.map, self.pos)
            self.map.sprites.add(sunken)
            sunken.after_move()