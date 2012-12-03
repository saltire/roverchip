import cell


class Exit(cell.Cell):
    def __init__(self, level):
        cell.Cell.__init__(self, level)
        
        self.colour = 255, 255, 192
        