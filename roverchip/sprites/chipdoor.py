import sprite


class ChipDoor(sprite.Sprite):
    def __init__(self, level, pos, facing):
        sprite.Sprite.__init__(self, level, pos, facing)
        
        self.tile = 7, 3
        self.rotate = True
        self.is_solid = True
        