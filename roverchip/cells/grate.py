from cell import Cell


class Grate(Cell):
    def __init__(self, level, pos):
        Cell.__init__(self, level, pos)
        
        self.tile = 5, 0
        self.robot_can_enter = False