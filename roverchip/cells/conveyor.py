from cell import Cell


class Conveyor(Cell):
    def __init__(self, level, pos, flow_dir):
        Cell.__init__(self, level, pos)
        
        self.tile = 7, 0
        self.rotate = flow_dir
        self.robot_can_enter = False


    def get_out_dir(self, move_dir):
        return self.rotate
