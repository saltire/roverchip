from cell import Cell


class Mud(Cell):
    def __init__(self, level, pos):
        Cell.__init__(self, level, pos)
        
        self.tile = 8, 0
        self.robot_can_enter = False
        self.object_can_enter = False
        
        
    def player_inside(self):
        self.level.set_cell(self.pos, 'Floor')
