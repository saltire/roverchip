import cell


class Fire(cell.Cell):
    def __init__(self, level):
        cell.Cell.__init__(self, level)
        
        self.tile = 2, 0
        self.player_can_enter = False
        self.robot_can_enter = True
        