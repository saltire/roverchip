class Cell:
    def __init__(self, level):
        self.level = level
        
        self.tile = 0, 0                # tile coords in the tileset
        self.rotate = 0                 # rotation of the tile
        self.player_can_enter = True    # player can enter this cell
        self.robot_can_enter = True     # robots can enter this cell
        self.object_can_enter = True    # movable objects can enter this cell
        
    
    def get_type(self):
        return self.__class__.__name__
    
