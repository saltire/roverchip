class Cell:
    def __init__(self, level):
        self.level = level
        
        self.tile = 0, 0
        self.player_can_enter = True
        self.robot_can_enter = True
        self.object_can_enter = True
        
    
    def get_type(self):
        return self.__class__.__name__
    
