from item import Item


class Boots(Item):
    def __init__(self, level, pos, colour):
        Item.__init__(self, level, pos)
        
        self.tile = 8, colour + 2
        self.size = 0.75
        
        self.colour = colour
