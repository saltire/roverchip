import cell


class Mud(cell.Cell):
    def __init__(self, level, pos):
        cell.Cell.__init__(self, level, pos)
        
        self.tile = 8, 0
        self.robot_can_enter = False
        self.object_can_enter = False
        
        
    def player_inside(self):
        self.level.set_cell(self.pos, 'Floor')
