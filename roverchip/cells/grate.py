import cell


class Grate(cell.Cell):
    def __init__(self, level):
        cell.Cell.__init__(self, level)
        
        self.colour = 192, 192, 192
        self.robot_can_enter = False