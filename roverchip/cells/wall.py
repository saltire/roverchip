import cell


class Wall(cell.Cell):
    def __init__(self, level):
        cell.Cell.__init__(self, level)
        
        self.colour = 0, 0, 0
        self.player_can_enter = False
        self.robot_can_enter = False
        self.object_can_enter = False
