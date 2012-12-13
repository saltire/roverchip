from movable import Movable


class Ball(Movable):
    def __init__(self, level, pos):
        Movable.__init__(self, level, pos)
        
        self.tile = 0, 1
        self.speed = 100

        self.moves_continuously = True
