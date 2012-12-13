from cell import Cell


class Wall(Cell):
    def __init__(self, level, pos):
        Cell.__init__(self, level, pos)
        
        self.tile = 1, 0
        self.player_can_enter = False
        self.robot_can_enter = False
        self.object_can_enter = False
