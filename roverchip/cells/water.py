import cell


class Water(cell.Cell):
    def __init__(self, level, flow_dir=None):
        cell.Cell.__init__(self, level)
        
        self.colour = 0, 128, 255
        self.player_can_enter = False
        self.robot_can_enter = False
        self.flow_dir = flow_dir


    def get_flow_dir(self):
        return self.flow_dir