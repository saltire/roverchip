import cell


class Mud(cell.Cell):
    def __init__(self, level):
        cell.Cell.__init__(self, level)
        
        self.tile = 8, 0
        self.robot_can_enter = False
        self.object_can_enter = False
        
        
    def player_inside(self, pos):
        self.level.set_cell(pos, 'Floor')
