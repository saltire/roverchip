from cell import Cell


class Fire(Cell):
    def __init__(self, level, pos):
        Cell.__init__(self, level, pos)
        
        self.tile = 2, 0
        self.player_can_enter = False
        self.robot_can_enter = True
        