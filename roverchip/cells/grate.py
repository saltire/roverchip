import cell


class Grate(cell.Cell):
    def __init__(self, level):
        cell.Cell.__init__(self, level)
        
        self.tile = 5, 0
        self.robot_can_enter = False