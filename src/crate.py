import sprite

class Crate(sprite.Sprite):
    
    def __init__(self, map, pos):
        sprite.Sprite.__init__(self, map, pos)
        self.colour = (128, 128, 128)
        self.is_movable = 1
        self.is_solid = 1
        