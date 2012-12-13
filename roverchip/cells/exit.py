from cell import Cell


class Exit(Cell):
    def __init__(self, level, pos):
        Cell.__init__(self, level, pos)
        
        self.tile = 6, 0
        