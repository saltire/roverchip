import sprite

class Door(sprite.Sprite):
    
    def __init__(self, map, pos, facing):
        sprite.Sprite.__init__(self, map, pos, facing)
        self.colour = (0, 255, 0)
        
        self.is_solid = 1