from movable import Movable


class Cart(Movable):   
    def __init__(self, level, pos):
        Movable.__init__(self, level, pos)
        
        self.tile = 1, 1
        self.speed = 100
        
        self.is_sinkable = False
        self.moves_continuously = True
