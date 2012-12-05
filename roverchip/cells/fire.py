import cell


class Fire(cell.Cell):
    def __init__(self, level):
        cell.Cell.__init__(self, level)
        
        self.colour = 64, 64, 64
        self.player_can_enter = False
        self.robot_can_enter = True
        