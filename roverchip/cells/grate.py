import cell


class Grate(cell.Cell):
    def __init__(self, level, pos):
        cell.Cell.__init__(self, level, pos)
        
        self.tile = 5, 0
        self.robot_can_enter = False