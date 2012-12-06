import cell


class Water(cell.Cell):
    def __init__(self, level, flow_dir=None):
        cell.Cell.__init__(self, level)
        
        self.tile = (3, 0) if flow_dir is None else (4, 0)
        self.player_can_enter = False
        self.robot_can_enter = False
        self.flow_dir = flow_dir


    def get_flow_dir(self):
        return self.flow_dir
