import cell


class Exit(cell.Cell):
    def __init__(self, level, pos):
        cell.Cell.__init__(self, level, pos)
        
        self.tile = 6, 0
        