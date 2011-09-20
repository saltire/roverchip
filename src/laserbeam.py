import sprite

class Laserbeam(sprite.Sprite):
    
    def __init__(self, map, pos, dirs):
        sprite.Sprite.__init__(self, map, pos)
        self.colour = (192, 64, 0, 128)
        self.layer = 2

        self.dirs = dirs
        
        