class Cell:
    def __init__(self, level):
        self.level = level
        
        self.colour = 255, 255, 255
        self.player_can_enter = True
        self.robot_can_enter = True
        self.object_can_enter = True
        
    
    def get_type(self):
        return self.__class__.__name__
    
