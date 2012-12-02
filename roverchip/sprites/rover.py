import sprite

class Rover(sprite.Sprite):
    
    def __init__(self, map, pos, facing=0):
        sprite.Sprite.__init__(self, map, pos, facing)
        self.colour = (255, 255, 0)
        self.layer = 1
        self.is_destructible = 1
        